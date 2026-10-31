"""TTFT measurement. Everything else calls these two functions."""
import json
import time

import httpx

import config

_client = httpx.Client(timeout=120, trust_env=False)  # one persistent connection


def measure_ttft(prompt):
    """Send one streaming request; return seconds until the first token arrives.

    prompt: str or list of token ids.
    """
    payload = {
        "model": config.SERVED_MODEL_NAME,
        "prompt": prompt,
        "max_tokens": config.MAX_OUTPUT_TOKENS,
        "temperature": 0,
        "stream": True,
    }
    ttft = None
    start = time.perf_counter()
    with _client.stream("POST", config.COMPLETIONS_URL, json=payload) as r:
        r.raise_for_status()
        for line in r.iter_lines():  # read to the end so requests never overlap
            if ttft is None and line.startswith("data:") and "[DONE]" not in line:
                ttft = time.perf_counter() - start
    if ttft is None:
        raise RuntimeError("no token received")
    return ttft


def measure_ttft_many(prompt, n=config.N_MEASUREMENTS):
    """Call measure_ttft n times, one at a time. Return list of TTFTs (seconds).

    prompt may be a callable returning a prompt, so each call gets a fresh one (cache misses).
    """
    return [measure_ttft(prompt() if callable(prompt) else prompt) for _ in range(n)]
