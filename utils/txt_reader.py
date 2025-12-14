import csv

def read_processes_from_txt(csv_file):
    processes = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            processes.append({
                "pid": row["Process_ID"],
                "arrival": int(row["Arrival_Time"]),
                "burst": int(row["CPU_Burst_Time"]),
                "priority": row["Priority"]
            })
    return processes
