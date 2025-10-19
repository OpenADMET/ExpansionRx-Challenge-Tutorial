import os
from huggingface_hub import HfApi

ENDPOINTS = ["LogD",
             "KSOL",
             "MLM CLint",
             "HLM CLint",
             "Caco-2 Permeability Efflux",
             "Caco-2 Permeability Papp A>B",
             "MPPB",
             "MBPB",
             "MGMB"]

STANDARD_COLS = ["Endpoint", "user", "submission_time", "model_report"]
METRICS = ["MAE", "RAE", "R2", "Spearman R", "Kendall's Tau"]
# Final columns
LB_COLS = ["user", "MAE", "R2", "Spearman R", "Kendall's Tau", "submission time", "model details"]
LB_AVG = ["user", "MA-RAE", "R2", "Spearman R", "Kendall's Tau", "submission time", "model details"] # Delete some columns for overall LB?
LB_DTYPES = ['markdown', 'number', 'number', 'number', 'number', 'str', 'markdown', 'number']

TOKEN = os.environ.get("HF_TOKEN")
CACHE_PATH=os.getenv("HF_HOME", ".")
API = HfApi(token=TOKEN)
organization="OpenADMET"
submissions_repo = f'{organization}/openadmet-expansionrx-challenge-submissions' # private
results_repo = f'{organization}/openadmet-expansionrx-challenge-results' # public
test_repo = f'{organization}/openadmet-expansionrx-challenge-test-data' # private