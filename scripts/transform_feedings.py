#!/usr/bin/env python3
"""
Transform a calendar-style CSV (`docs/templates/import.csv`) into a flat
`feedings` CSV suitable for importing into Postgres.

Usage:
  ./scripts/transform_feedings.py --input docs/templates/import.csv \
      --output docs/templates/feedings-transformed.csv --time 07:00:00
"""
import csv
from datetime import datetime, time
import argparse


def parse_date(s):
    s = s.strip()
    if not s:
        return None
    for fmt in ('%d/%m/%y', '%d/%m/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    # fallback: try dayfirst with 2-digit year via split
    parts = s.split('/')
    if len(parts) == 3:
        d, m, y = parts
        y = y.zfill(2)
        try:
            return datetime.strptime(f"{d}/{m}/{y}", '%d/%m/%y').date()
        except Exception:
            pass
    raise ValueError(f"Unrecognized date format: {s}")


def transform(input_path, output_path, default_time_str):
    default_time = datetime.strptime(default_time_str, '%H:%M:%S').time()
    with open(input_path, newline='') as f:
        reader = csv.reader(f)
        rows = [r for r in reader]

    if len(rows) < 2:
        raise SystemExit('Input CSV seems too short or empty')

    # Skip header row (weekday names). Then rows should come in pairs:
    # date_row, value_row, date_row, value_row, ...
    data_rows = rows[1:]

    out_rows = []
    i = 0
    while i < len(data_rows) - 0:
        date_row = data_rows[i]
        # Find the next row that looks like values (numeric) — usually i+1
        if i + 1 < len(data_rows):
            value_row = data_rows[i + 1]
            i += 2
        else:
            break

        # ensure both rows are lists of same number of columns — iterate by index
        maxcols = max(len(date_row), len(value_row))
        for c in range(maxcols):
            date_cell = date_row[c] if c < len(date_row) else ''
            val_cell = value_row[c] if c < len(value_row) else ''
            date_cell = date_cell.strip()
            val_cell = val_cell.strip()
            if not date_cell or not val_cell:
                continue
            try:
                d = parse_date(date_cell)
            except ValueError:
                # skip unparseable
                continue
            # build timestamp
            dt = datetime.combine(d, default_time)
            # normalize cups value
            cups = val_cell.replace(',', '.')
            out_rows.append((cups, '', dt.strftime('%Y-%m-%d %H:%M:%S')))

    # write output
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cups', 'notes', 'timestamp'])
        for r in out_rows:
            writer.writerow(r)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', '-i', default='docs/templates/import.csv')
    ap.add_argument('--output', '-o', default='docs/templates/feedings-transformed.csv')
    ap.add_argument('--time', default='07:00:00', help='time component for timestamps (HH:MM:SS)')
    args = ap.parse_args()
    transform(args.input, args.output, args.time)
    print('Wrote', args.output)
