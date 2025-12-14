from __future__ import annotations
from pathlib import Path

def select_csv_file(data_dir: str | Path = "data"):
   
    data_path = Path(data_dir).expanduser().resolve()

    if not data_path.exists() or not data_path.is_dir():
        raise FileNotFoundError(f"Data klasörü bulunamadı: {data_path}")

    csv_files = sorted(data_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"{data_path} içinde .csv bulunamadı.")

    print("\nCSV Dosyası Seç")
    print("-" * 30)
    for idx, f in enumerate(csv_files, start=1):
        print(f"{idx}) {f.name}")

    while True:
        choice = input(f"\nSeçim (1-{len(csv_files)}): ").strip()
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= len(csv_files):
                selected = csv_files[i - 1].resolve()
                print(f"\nSeçilen dosya: {selected}")
                return str(selected)
        print("Geçersiz seçim. Tekrar dene.")
