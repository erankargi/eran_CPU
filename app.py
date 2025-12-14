from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

from utils.csv_reader import read_processes_from_csv
from utils.output_writer import write_all_outputs

from algorithms.FCFS import fcfs
from algorithms.NP_SJF import sjf_non_preemptive  
from algorithms.round_robin import round_robin  
from algorithms.NP_Priority import priority_non_preemptive
from select import select_csv_file



def run_algo(name, fn, processes):
    procs_copy = [p.copy() for p in processes]  
    timeline, results, metrics = fn(procs_copy)
    return name, timeline, results, metrics


if __name__ == "__main__":
    csv_file = select_csv_file("data")  
    case_name = Path(csv_file).stem  

    processes = read_processes_from_csv(csv_file)

    algorithms = [
        ("FCFS", fcfs),
        ("SJF_NP", sjf_non_preemptive),
        ("RR", round_robin),  
        ("PRIORITY_NP", priority_non_preemptive),
    ]

    
    algo_runs = []
    with ThreadPoolExecutor(max_workers=len(algorithms)) as executor:
        futures = [executor.submit(run_algo, name, fn, processes) for name, fn in algorithms]
        for fut in as_completed(futures):
            algo_runs.append(fut.result())

    
    written_files = write_all_outputs("outputs", case_name, algo_runs)

    
    print("\nOUTPUT DOSYALARI OLUŞTURULDU:")
    for algo_name, path in written_files:
        print(f"- {algo_name}: {path}")