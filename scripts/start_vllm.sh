
#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-Qwen/Qwen3-0.6B}"

echo "=========================================="
echo " HIGH PERFORMANCE INFERENCE"
echo " BASELINE: DEFAULT VLLM"
echo "=========================================="

echo "Model: ${MODEL}"
echo "No custom performance flags."

exec vllm serve "${MODEL}"
