import gradio as gr
import pandas as pd
from pathlib import Path
from typing import Optional
from .about import ENDPOINTS
from .utils import bootstrap_metrics, clip_and_log_transform


def _check_required_columns(df: pd.DataFrame, name: str, cols: list[str]):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")

def calculate_metrics(
        results_dataframe: pd.DataFrame,
        test_dataframe: pd.DataFrame
    ):
    import numpy as np
    
    # Do some checks

    # 1) Check all columns are present
    _check_required_columns(results_dataframe, "Results file", ["Molecule Name"] + ENDPOINTS)
    _check_required_columns(test_dataframe, "Test file", ["Molecule Name"] + ENDPOINTS)
    
    
    # 2) Check all Molecules in the test set are present in the predictions
    if not (results_dataframe['Molecule Name'].isin(test_dataframe['Molecule Name'])).all():
        raise gr.Error("The predictions file is missing some molecules present in the test set. Please ensure all molecules are included.")


    # 3) check no duplicated molecules in the predictions file
    if results_dataframe['Molecule Name'].duplicated().any():
        raise gr.Error("The predictions file contains duplicated molecules. Please ensure each molecule is only listed once.")
    
    # 4) Merge dataframes to ensure alignment
    merged_df = results_dataframe.merge(
        test_dataframe,
        on="Molecule Name",
        suffixes=('_pred', '_true'),
        how="inner"
    )
    merged_df = merged_df.sort_values("Molecule Name")

    # 5) loop over endpoints 

    final_cols = ["MAE", "RAE", "R2", "Spearman R", "Kendall's Tau"]
    all_endpoint_results = []

    for ept in ENDPOINTS:
        pred_col = f"{ept}_pred"
        true_col = f"{ept}_true"

        # cast to numeric, coerce errors to NaN
        merged_df[pred_col] = pd.to_numeric(merged_df[pred_col], errors="coerce")
        merged_df[true_col] = pd.to_numeric(merged_df[true_col], errors="coerce")

        if merged_df[pred_col].isnull().all():
            raise gr.Error(f"All predictions are missing for endpoint {ept}. Please provide valid predictions.")
        
        # subset and drop NaNs
        subset = merged_df[[pred_col, true_col]].dropna()
        if subset.empty:
            raise gr.Error(f"No valid data available for endpoint {ept} after removing NaNs.")
        
        # extract numpy arrays
        y_pred = subset[pred_col].to_numpy()
        y_true = subset[true_col].to_numpy()

        # apply log10 + 1 transform except for logD
        if ept.lower() not in ['logd']:
            y_true_log = clip_and_log_transform(y_true)
            y_pred_log = clip_and_log_transform(y_pred)

        else:
            y_true_log = y_true
            y_pred_log = y_pred

        # calculate metrics with bootstrapping
        bootstrap_df = bootstrap_metrics(y_pred_log, y_true_log, ept, n_bootstrap_samples=1000)
        df_endpoint = bootstrap_df.pivot_table(
            index=["Endpoint"],
            columns="Metric", 
            values="Value", 
            aggfunc=["mean", "std"]
        ).reset_index()

        # Get a df with columns 'mean_MAE', 'std_MAE', ...
        df_endpoint.columns = [
            f'{i}_{j}' if i != '' else j for i, j in df_endpoint.columns
        ]

        df_endpoint.rename(columns={'Endpoint_': 'Endpoint'}, inplace=True)
        all_endpoint_results.append(df_endpoint)

    df_results = pd.concat(all_endpoint_results, ignore_index=True)
    mean_cols = [f'mean_{m}' for m in final_cols]
    std_cols = [f'std_{m}' for m in final_cols]
    # Average results
    macro_means = df_results[mean_cols].mean()
    macro_stds = df_results[std_cols].mean()
    avg_row = {"Endpoint": "Macro Average"}
    avg_row.update(macro_means.to_dict())
    avg_row.update(macro_stds.to_dict())    
    df_with_average = pd.concat([df_results, pd.DataFrame([avg_row])], ignore_index=True)
    # Fix order of columns
    df_with_average = df_with_average[["Endpoint"]+mean_cols+std_cols]
    return df_with_average