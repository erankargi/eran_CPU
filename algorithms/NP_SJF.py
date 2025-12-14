
from __future__ import annotations
from typing import List, Dict, Tuple, Any

def sjf_non_preemptive(
    processes: List[Dict[str, Any]],
    context_switch_overhead: float = 0.0
):

    if not processes:
        empty_metrics = {
            "throughput": {},
            "cpu_efficiency_percent": 0.0,
            "busy_time": 0.0,
            "idle_time": 0.0,
            "context_overhead_time": 0.0,
            "total_time": 0.0,
            "context_switches": 0
        }
        return [], [], empty_metrics

    procs = [
        {"pid": p["pid"], "arrival": int(p["arrival"]), "burst": int(p["burst"]), "priority": p.get("priority")}
        for p in processes
    ]

    procs.sort(key=lambda x: (x["arrival"], x["pid"]))

    timeline: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []

    t: float = 0.0
    i = 0 
    n = len(procs)

    ready: List[Dict[str, Any]] = []
    completed = 0

    busy_time = 0.0
    idle_time = 0.0
    context_overhead_time = 0.0
    context_switches = 0

    
    throughput: Dict[int, int] = {}

    last_pid = None

    while completed < n:
        
        while i < n and procs[i]["arrival"] <= t:
            ready.append(procs[i])
            i += 1

        if not ready:
            
            next_arrival = procs[i]["arrival"] 
            if next_arrival > t:
                
                timeline.append({"pid": "IDLE", "start": t, "end": next_arrival})
                idle_time += (next_arrival - t)
                t = float(next_arrival)
            continue

        
        ready.sort(key=lambda x: (x["burst"], x["arrival"], x["pid"]))
        p = ready.pop(0)

        
        if last_pid is not None:
            context_switches += 1
            if context_switch_overhead > 0:
                timeline.append({"pid": "CS", "start": t, "end": t + context_switch_overhead})
                context_overhead_time += context_switch_overhead
                t += context_switch_overhead

        start = t
        end = t + p["burst"]

        timeline.append({"pid": p["pid"], "start": start, "end": end})
        busy_time += p["burst"]

        waiting = start - p["arrival"]
        turnaround = end - p["arrival"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "start": start,
            "finish": end,
            "waiting": waiting,
            "turnaround": turnaround
        })

        t = end
        last_pid = p["pid"]
        completed += 1

        throughput[int(t)] = completed  

    total_time = busy_time + idle_time + context_overhead_time
    cpu_eff = (busy_time / total_time * 100.0) if total_time > 0 else 0.0

    metrics = {
        "throughput": throughput,
        "cpu_efficiency_percent": cpu_eff,
        "busy_time": busy_time,
        "idle_time": idle_time,
        "context_overhead_time": context_overhead_time,
        "total_time": total_time,
        "context_switches": context_switches
    }

    return timeline, results, metrics
