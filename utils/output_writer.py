from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Tuple


def timeline_to_str(algo_name: str, timeline: List[Dict[str, Any]]):
    out = []
    out.append(f"ZAMAN TABLOSU ({algo_name})")
    for t in timeline:
        out.append(f"[ {t['start']} ] -- {t['pid']} -- [ {t['end']} ]")
    return "\n".join(out)


def stats_to_str(results: List[Dict[str, Any]]):
    waiting_times = [r["waiting"] for r in results]
    turnaround_times = [r["turnaround"] for r in results]

    out = []
    out.append("İSTATİSTİKLER")
    out.append(f"Ortalama Bekleme Süresi     : {sum(waiting_times)/len(waiting_times):.2f}")
    out.append(f"Maksimum Bekleme Süresi     : {max(waiting_times)}")
    out.append(f"Ortalama Turnaround Süresi  : {sum(turnaround_times)/len(turnaround_times):.2f}")
    out.append(f"Maksimum Turnaround Süresi  : {max(turnaround_times)}")
    return "\n".join(out)


def metrics_to_str(metrics: Dict[str, Any]):
    out = []
    out.append("METRICS")
    out.append("Throughput (tamamlanan iş sayısı):")
    for T, count in metrics["throughput"].items():
        out.append(f"  T={T}: {count}")

    out.append(f"CPU Verimliliği (%): {metrics['cpu_efficiency_percent']:.2f}")
    out.append(
        f"Busy={metrics['busy_time']}, Idle={metrics['idle_time']}, "
        f"ContextOverhead={metrics['context_overhead_time']:.3f}, Total={metrics['total_time']:.3f}"
    )
    out.append(f"Toplam Context Switch: {metrics['context_switches']}")
    return "\n".join(out)


def _safe_name(name: str):
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)


def write_algo_output(
    outputs_dir: Path,
    case_name: str,
    algo_name: str,
    timeline: List[Dict[str, Any]],
    results: List[Dict[str, Any]],
    metrics: Dict[str, Any],
):
    """
    Tek bir algoritmanın çıktısını outputs_dir altına yazar ve dosya yolunu döner.
    """
    outputs_dir.mkdir(parents=True, exist_ok=True)

    safe_algo = _safe_name(algo_name)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = outputs_dir / f"{case_name}__{safe_algo}__{ts}.txt"

    content = []
    content.append(f"CASE: {case_name}")
    content.append(f"ALGORITHM: {algo_name}")
    content.append("")
    content.append(timeline_to_str(algo_name, timeline))
    content.append("")
    content.append(stats_to_str(results))
    content.append("")
    content.append(metrics_to_str(metrics))
    content.append("")

    out_path.write_text("\n".join(content), encoding="utf-8")
    return out_path


def write_all_outputs(
    outputs_dir: str | Path,
    case_name: str,
    algo_runs: List[Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]],
):
    """
    algo_runs: [(algo_name, timeline, results, metrics), ...]
    Dönüş: [(algo_name, written_path), ...]
    """
    out_dir = Path(outputs_dir)
    written_files: List[Tuple[str, Path]] = []

    for algo_name, timeline, results, metrics in algo_runs:
        path = write_algo_output(out_dir, case_name, algo_name, timeline, results, metrics)
        written_files.append((algo_name, path))

    written_files.sort(key=lambda x: x[0])
    return written_files
