def fcfs(processes, context_switch_cost=0.001, throughput_T=(50, 100, 150, 200)):
    
    processes = sorted(processes, key=lambda x: x["arrival"])

    current_time = 0
    timeline = []      
    results = []       
    context_switches = 0
    last_pid = None

    for p in processes:

        
        if current_time < p["arrival"]:
            timeline.append({
                "pid": "IDLE",
                "start": current_time,
                "end": p["arrival"]
            })
            current_time = p["arrival"]
            

       
        if last_pid is not None:
            context_switches += 1

        start_time = current_time
        finish_time = start_time + p["burst"]

        timeline.append({
            "pid": p["pid"],
            "start": start_time,
            "end": finish_time
        })

        waiting_time = start_time - p["arrival"]
        turnaround_time = finish_time - p["arrival"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "start": start_time,
            "finish": finish_time,
            "waiting": waiting_time,
            "turnaround": turnaround_time
        })

        current_time = finish_time
        last_pid = p["pid"]

   
    throughput = {}
    for T in throughput_T:
        throughput[T] = sum(1 for r in results if r["finish"] <= T)

   
    busy_time = sum(r["burst"] for r in results)
    idle_time = sum(seg["end"] - seg["start"] for seg in timeline if seg["pid"] == "IDLE")
    overhead_time = context_switches * context_switch_cost

    total_time = busy_time + idle_time + overhead_time
    cpu_efficiency = (busy_time / total_time * 100) if total_time > 0 else 0.0

    metrics = {
        "throughput": throughput,                 
        "cpu_efficiency_percent": cpu_efficiency, 
        "busy_time": busy_time,
        "idle_time": idle_time,
        "context_switches": context_switches,
        "context_overhead_time": overhead_time,
        "total_time": total_time
    }

    return timeline, results, metrics
