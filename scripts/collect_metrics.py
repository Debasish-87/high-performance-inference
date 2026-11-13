
import argparse
import csv
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path


def percentile(values, p):
    """Calculate percentile using linear interpolation."""
    if not values:
        return None

    values = sorted(values)

    if len(values) == 1:
        return values[0]

    position = (len(values) - 1) * p
    lower = math.floor(position)
    upper = math.ceil(position)

    if lower == upper:
        return values[lower]

    fraction = position - lower

    return (
        values[lower] * (1 - fraction)
        + values[upper] * fraction
    )


def collect_metrics(input_file, output_dir, duration=None):
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with input_file.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError("Input JSON must contain a non-empty list.")

    latencies = []
    successful = 0
    failed = 0

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} must be a JSON object.")

        status = record.get("status", "success")

        if status == "success":
            successful += 1

            latency = record.get("latency_seconds")

            if latency is None:
                raise ValueError(
                    f"Record {index} is missing latency_seconds."
                )

            latency = float(latency)

            if not math.isfinite(latency) or latency < 0:
                raise ValueError(
                    f"Record {index} has invalid latency_seconds."
                )

            latencies.append(latency)

        elif status == "error":
            failed += 1

        else:
            raise ValueError(
                f"Record {index} has unsupported status: {status}"
            )

    total = successful + failed
    error_rate = failed / total * 100

    if duration is not None and duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_requests": total,
        "successful_requests": successful,
        "failed_requests": failed,
        "error_rate_percent": error_rate,
        "latency_seconds": {
            "mean": statistics.mean(latencies) if latencies else None,
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
        },
        "request_throughput_rps": (
            total / duration if duration is not None else None
        ),
        "throughput_duration_seconds": duration,
    }

    json_path = output_dir / "metrics.json"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    csv_path = output_dir / "metrics.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "total_requests",
                "successful_requests",
                "failed_requests",
                "error_rate_percent",
                "mean_latency_seconds",
                "p50_latency_seconds",
                "p95_latency_seconds",
                "p99_latency_seconds",
                "request_throughput_rps",
            ],
        )

        writer.writeheader()
        writer.writerow({
            "total_requests": total,
            "successful_requests": successful,
            "failed_requests": failed,
            "error_rate_percent": error_rate,
            "mean_latency_seconds": metrics["latency_seconds"]["mean"],
            "p50_latency_seconds": metrics["latency_seconds"]["p50"],
            "p95_latency_seconds": metrics["latency_seconds"]["p95"],
            "p99_latency_seconds": metrics["latency_seconds"]["p99"],
            "request_throughput_rps": metrics[
                "request_throughput_rps"
            ],
        })

    print(json.dumps(metrics, indent=4))
    print(f"\nSaved: {json_path}")
    print(f"Saved: {csv_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Collect request-level inference metrics."
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--duration", type=float, default=None)

    args = parser.parse_args()

    collect_metrics(
        input_file=args.input,
        output_dir=args.output,
        duration=args.duration,
    )


if __name__ == "__main__":
    main()
