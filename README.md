# Inference Performance Engineering Project

Optimize an existing LLM inference stack across three layers:

1. vLLM engine tuning
2. System/runtime optimization
3. GPU kernel optimization using Triton/CUDA

## Architecture

- Local Ubuntu + VS Code: source code, scripts, configs and reports.
- Google Colab T4: vLLM serving, benchmarking, profiling and GPU kernel execution.
- AnythingLLM: end-to-end application validation.
- GuideLLM: controlled load generation and inference benchmarking.

## Experiment policy

- Capture a baseline before changing anything.
- Change one optimization variable at a time.
- Keep model, GPU, workload and measurement conditions consistent.
- Run GuideLLM independently from AnythingLLM during controlled benchmarks.
- Validate correctness before accepting any kernel optimization.
- Record individual and combined optimization results.

## Setup

Create a local Python environment:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements-local.txt

Colab dependencies and server setup will be handled in the notebooks
and scripts as the environment is verified.

## Security

Never commit API keys, tunnel tokens, credentials or private documents.
Use `.env` for local secrets; `.env` is ignored by Git.
