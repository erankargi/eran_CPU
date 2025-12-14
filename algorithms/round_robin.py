
from typing import List, Dict, Any, Tuple

def round_robin(
    processes: List[Dict[str, Any]],
    time_quantum: int = 4,
    context_switch_overhead: float = 0.0
):
    
    if not processes:
        return [], [], {"throughput": {}, "cpu_efficiency_percent": 0.0, "busy_time": 0.0, "idle_time": 0.0, "context_overhead_time": 0.0, "total_time": 0.0, "context_switches": 0}

    
    procs = [{"pid": p["pid"], "arrival": int(p["arrival"]), "burst": int(p["burst"]), "remaining": int(p["burst"])} for p in processes]

    
    procs.sort(key=lambda x: x["arrival"])

    timeline = []  
    results = []   
    t = 0          
    i = 0          
    completed = 0   
    n = len(procs) 
    ready_queue = []  
    context_switches = 0
    busy_time = 0.0
    idle_time = 0.0
    context_overhead_time = 0.0
    last_pid = None
    throughput = {}

    while completed < n:
        
        while i < n and procs[i]["arrival"] <= t:
            ready_queue.append(procs[i])
            i += 1
        
        if not ready_queue:
            
            next_arrival = procs[i]["arrival"] 
            timeline.append({"pid": "IDLE", "start": t, "end": next_arrival})
            idle_time += (next_arrival - t)
            t = next_arrival
            continue

        
        p = ready_queue.pop(0)

        
        if last_pid is not None:
            context_switches += 1
            if context_switch_overhead > 0:
                timeline.append({"pid": "CS", "start": t, "end": t + context_switch_overhead})
                context_overhead_time += context_switch_overhead
                t += context_switch_overhead

        
        start = t
        if p["remaining"] <= time_quantum:
            
            end = t + p["remaining"]
            p["remaining"] = 0
            completed += 1
        else:
            
            end = t + time_quantum
            p["remaining"] -= time_quantum
            ready_queue.append(p)

        timeline.append({"pid": p["pid"], "start": start, "end": end})
        busy_time += (end - start)

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
