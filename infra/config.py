"""All settings in one place. (docker-compose.yml repeats model/port: keep in sync.)"""

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
SERVED_MODEL_NAME = "qwen2.5-1.5b"  # id used in API requests

HOST = "127.0.0.1"
PORT = 8000
COMPLETIONS_URL = f"http://{HOST}:{PORT}/v1/completions"  # streaming endpoint
HEALTH_URL = f"http://{HOST}:{PORT}/health"

N_MEASUREMENTS = 20   # default samples per condition
WARMUP = 5            # discarded requests before measuring
MAX_OUTPUT_TOKENS = 1  # only the first token matters

PROMPT_TOKENS = 1024   # long enough to span many 16-token cache blocks
MAX_MODEL_LEN = 4096   # server limit; PROMPT_TOKENS must stay below this

EVAL_DIR = "eval"
