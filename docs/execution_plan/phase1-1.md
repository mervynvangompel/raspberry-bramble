# Phase 1-1 Import CSV to Postgres

**Goal:** Import historical dog feeding data from Excel into the Postgres database running on k3s (pi-control node).

## What We Did

1. Created a CSV template matching the `feedings` table schema (columns: `cups`, `notes`, `timestamp`)
2. Built a Python transform script to convert calendar-style Excel data with historical data into flat CSV format
3. Transformed historical food tracker data using the script
4. Imported the transformed CSV into Postgres via `kubectl exec` and stdin pipe

## Files Created

- [docs/templates/feedings-template.csv](../../docs/templates/feedings-template.csv) — Template with 3 columns matching the `feedings` table
- [scripts/transform_feedings.py](../../scripts/transform_feedings.py) — Python script to transform calendar-style data to flat CSV
- [docs/templates/feedings-transformed.csv](../../docs/templates/feedings-transformed.csv) — Output CSV with all historical records

## How to Use the Transform Script

**Prerequisite:** Input CSV should be calendar-style (dates as headers, values in rows below).

```bash
cd /home/mervyn/Desktop/bramble
python3 scripts/transform_feedings.py --input docs/templates/import.csv --output docs/templates/feedings-transformed.csv --time 07:00:00
```

**Options:**
- `--input`: Path to source calendar-style CSV (default: `docs/templates/import.csv`)
- `--output`: Path to output flat CSV (default: `docs/templates/feedings-transformed.csv`)
- `--time`: Default time component for timestamps in HH:MM:SS format (default: `07:00:00`)

## How to Import into Postgres

### Method 1: Pipe via kubectl exec (simplest)

From the directory containing your CSV:

```bash
cd /home/mervyn/Desktop/bramble/docs/templates
cat feedings-transformed.csv | kubectl exec -i deployment/postgres -- psql -U postgres -d dogfeeding -c "\COPY feedings (cups,notes,timestamp) FROM STDIN CSV HEADER;"
```

### Method 2: Interactive psql (with kubectl exec)

```bash
kubectl exec -it deployment/postgres -- psql -U postgres -d dogfeeding
```

Then in the psql prompt (from the directory containing your CSV):

```sql
\copy feedings (cups,notes,timestamp) FROM 'feedings-transformed.csv' CSV HEADER;
```

Note: This only works if psql can resolve the relative path from where you ran `kubectl exec`.

### Verification

```bash
kubectl exec deployment/postgres -- psql -U postgres -d dogfeeding -c "SELECT count(*) FROM feedings;"
kubectl exec deployment/postgres -- psql -U postgres -d dogfeeding -c "SELECT * FROM feedings ORDER BY timestamp DESC LIMIT 10;"
```

## Key Notes

- Use `\COPY` (client-side, with backslash) when using pipes or when the file is on your local machine
- Use `COPY` (server-side, no backslash) only when the file is already inside the pod
- The transform script expects date cells and value cells in alternating rows (calendar format)
- Dates are parsed with DD/MM/YY or DD/MM/YYYY format; the time defaults to `--time` parameter
- CSV column order matters: `cups,notes,timestamp` (no `id`, which is auto-generated)