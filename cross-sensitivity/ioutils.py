
import sys
import csv
from typing import List

def detect_separator(sample_line: str) -> str:
    if "," in sample_line:
        return ","
    if "\t" in sample_line:
        return "\t"
    if " " in sample_line:
        return " "
    return "," # default


def load_data(file_path: str, sep: str) -> List[List[str]]:
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        f.seek(0)
        if sep == "auto":
            delimiter = detect_separator(first_line)
        else:
            delimiter = sep

        if delimiter == " ":
            # Handle multiple spaces as a single separator
            data = [line.strip().split() for line in f if line.strip()]
        else:
            reader = csv.reader(f, delimiter=delimiter)
            data = [row for row in reader if row]

    return data