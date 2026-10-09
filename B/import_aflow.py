"""Import CSV exported from AFLOW into a local, read-only mirror consumable by B workers.
No AFLOW records are bundled or fabricated. CSV requires `auid` and `compound`.
"""
import argparse,csv,sqlite3,pathlib
p=argparse.ArgumentParser()
p.add_argument('csv_path',help='CSV exported from AFLOW')
p.add_argument('--output',default='aflow-data/aflow.sqlite')
a=p.parse_args()
source=pathlib.Path(a.csv_path)
if not source.is_file(): raise SystemExit('CSV not found')
dest=pathlib.Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True)
con=sqlite3.connect(dest)
con.execute('CREATE TABLE IF NOT EXISTS materials (auid TEXT PRIMARY KEY, compound TEXT NOT NULL, prototype TEXT, spacegroup_relax TEXT, Egap REAL, energy_atom REAL, aurl TEXT)')
def number(s):
 if not s or s.strip().lower() in ('none','null','nan','n/a'):return None
 try:return float(s)
 except ValueError:return None
count=0
with source.open(newline='',encoding='utf-8-sig') as f:
 reader=csv.DictReader(f)
 if not {'auid','compound'}<=set(reader.fieldnames or []):raise SystemExit('Required CSV columns: auid, compound')
 for row in reader:
  if not row.get('auid') or not row.get('compound'):continue
  con.execute('INSERT OR REPLACE INTO materials VALUES (?,?,?,?,?,?,?)',(
    row['auid'].strip(),row['compound'].strip(),row.get('prototype'),row.get('spacegroup_relax'),number(row.get('Egap')),number(row.get('energy_atom')),row.get('aurl')))
  count+=1
con.commit();con.close()
print(f'Imported {count} AFLOW CSV rows to {dest}')
