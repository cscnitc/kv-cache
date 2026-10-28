# Infrastructure

The goal here is to have a vLLM server running a small LLM with prefix caching enabled set up, along with a reusable function that measures Time-To-First-Token (TTFT) reliably.

Repeated prompts (cache hits) and new prompts (cache misses) should produce clearly separable TTFT distributions repeatably.

## GPU

We'll have to move to using lab GPUs, so start talking with staff about it. Shouldn't be too hard to get it.

For now, ensure that the harness works with Colab or Kaggle free tiers. This isn't suitable for the actual experiment cause of session timeouts and disconnects, but we can validate the harness with it.

One possibility is CPU-only as well, it's an interesting direction to take. Keep this as an option in the code. The risk here is OS scheduling messing stuff up, so we'll have to check if the calibration gap shows up here. Interesting direction though, look into research regarding this.

## Environment

Use vLLM's official Docker image, dont try to custom build one. Check for Nvidia Container Toolkit.

Linux is needed for GPU-backed vLLM since Windows isn't supported. 

Use `uv` for venv management instead of `pip`, it's a lot cleaner.

Confirm `nvidia-smi` shows the GPU and driver before installing vLLM though. This can cause a lot of issues.

Choose a small model of around one to three billion parameters, maybe Qwen2.5-1.5B.

Can't really think of anything else right now.

## Files

`config.py`: this should centralise every setting the other files need.

Stuff we need here:
- Model name and identifier
- Server host and port
- Streaming completion endpoint URL?
- Put a default number of measurements as well, around 20
- Maybe prompt length limits and other default values

`server_setup.sh`: a record of how exactly to setup the server.

- GPU in-container check.
- docker compose pull to fetch image, and compose up to launch server.
- curl to check health `--enable-prefix-caching` as arg and point to model.
- Any other related stuff

A `docker-compose.yml` file with the setup.

`harness.py`: Two functions need to be here.

- A function that sends a prompt to the server's streaming endpoint and returns TTFT.
- A functions that calls the above N times and returns the complete list of TTFT samples.

This is the function that all other files will call, so important.

`calibration.py`: a sanity check of sorts to make sure harness works.

- Define a repeated prompted that will work for cache hits, and a fresh prompt, one that will be new each session for cache misses.
- Loop over many trials and collect TTFT samples.
- Summary statistics, detailed data
- Save to an `eval/` folder.

## Stuff to look out for

- Make sure the hit and miss prompts differ only in cache status, not in length or complexity. The measured gap should be due to cache, not anything else.
- Background noise like other processes contaminating data. Keep rerunning calibration check all the time.
- Don't do concurrent requests, serialise it. vLLM;s continuous batching means that concurrent requests can mess with the individual TTFT readings.