import csv

def read_processes_from_csv(csv_file):
    processes = []

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  
        for row in reader:
            if not row:
                continue

            process = {
                "pid": row[0],
                "arrival": int(row[1]),
                "burst": int(row[2]),
                "priority": row[3]
            }

            processes.append(process)

    return processes
