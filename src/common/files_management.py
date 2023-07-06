import csv
from pathlib import Path
from typing import List


def open_saved_webpage(file_path: Path) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def write_csv(dest: Path, data: List[dict], mode='w'):
    with dest.open(mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        for r in data:
            writer.writerow(r.values())


def write_to_file(dest: Path, data: List[str], mode='w'):
    with dest.open(mode) as file:
        file.writelines(f"{line}\n" for line in data)


def read_urls(path: Path) -> List:
    with path.open('r') as f:
        return [line.strip() for line in f if line.strip()]
