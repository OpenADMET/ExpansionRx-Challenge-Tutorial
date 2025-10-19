
import pandas as pd
import numpy as np
from typing import Tuple

from .about import METRICS


def clip_and_log_transform(y: np.ndarray):
    """
    Clip to a detection limit and transform to log10 scale.

    Parameters
    ----------
    y : np.ndarray
        The array to be clipped and transformed.
    """
    y = np.clip(y, a_min=0, a_max=None)
    return np.log10(y + 1)


def bootstrap_sampling(size: int, n_samples: int) -> np.ndarray:
    """
    Generate bootstrap samples for a given size and number of samples.
    Parameters
    ----------
    size : int
        The size of the data.
    n_samples : int
        The number of samples to generate.
    Returns
    -------
    np.ndarray
        Returns a numpy array of the bootstrap samples.
    """
    rng = np.random.default_rng(0)
    return rng.choice(size, size=(n_samples, size), replace=True)


def metrics_per_ep(pred: np.ndarray, 
                   true: np.ndarray
    )->Tuple[float, float, float, float]:
    """Predict evaluation metrics for a single sample
    Parameters
    ----------
    pred : np.ndarray
        Array with predictions
    true : np.ndarray
        Array with actual values
    Returns
    -------
    Tuple[float, float, float, float]
        Resulting metrics: (MAE, RAE, R2, Spearman R, Kendall's Tau)
    """
    from scipy.stats import spearmanr, kendalltau
    from sklearn.metrics import mean_absolute_error, r2_score
    mae = mean_absolute_error(true, pred)
    rae = mae / np.mean(np.abs(true - np.mean(true)))
    if np.nanstd(true) == 0:
        r2=np.nan
    else:
        r2 = r2_score(true, pred)
    spr = spearmanr(true, pred).statistic
    ktau = kendalltau(true, pred).statistic

    return mae, rae, r2, spr, ktau

def bootstrap_metrics(pred: np.ndarray, 
                      true: np.ndarray,
                      endpoint: str,
                      n_bootstrap_samples=1000
    )->pd.DataFrame:
    """Calculate bootstrap metrics given predicted and true values
    Parameters
    ----------
    pred : np.ndarray
        Predicted endpoints
    true : np.ndarray
        Actual endpoint values
    endpoint : str
        String with endpoint
    n_bootstrap_samples : int, optional
        Size of bootstrapsample, by default 1000
    Returns
    -------
    pd.DataFrame
        Dataframe with estimated metric per bootstrap sample for the given endpoint
    """
    cols = ["Sample", "Endpoint", "Metric", "Value"]
    bootstrap_results = pd.DataFrame(columns=cols) 
    for i, indx in enumerate(
        bootstrap_sampling(true.shape[0], n_bootstrap_samples)
    ):
        mae, rae, r2, spr, ktau = metrics_per_ep(pred[indx], true[indx])
        scores = pd.DataFrame(
            [
                [i, endpoint, "MAE", mae],
                [i, endpoint, "RAE", rae],
                [i, endpoint, "R2", r2],
                [i, endpoint, "Spearman R", spr],
                [i, endpoint, "Kendall's Tau", ktau]
            ],
            columns=cols
        )
        bootstrap_results = pd.concat([bootstrap_results, scores])
    return bootstrap_results

def map_metric_to_stats(df: pd.DataFrame, average=False) -> pd.DataFrame: 
    """Map mean and std to 'mean +/- std' string for each metric
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to modify
    average : bool, optional
        Whether the dataframe contains average info, by default False
    Returns
    -------
    pd.DataFrame
        Modified dataframe
    """
    metric_cols = METRICS[:] 
    if average:
        metric_cols[1] = "MA-RAE" 
    cols_drop = []
    for col in metric_cols:
        mean_col = f"mean_{col}"
        std_col = f"std_{col}"
        df[col] = df.apply(
            lambda row: f"{row[mean_col]:.2f} +/- {row[std_col]:.2f}", 
            axis=1
        )
        cols_drop.extend([mean_col, std_col])
    df = df.drop(columns=cols_drop)
    return df