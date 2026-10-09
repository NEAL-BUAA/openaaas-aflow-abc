#!/usr/bin/env python3
"""Read-only local AFLOW mirror tool; no network calls. Query an imported subset of data."""
import argparse,csv,json,sqlite3,sys
from pathlib import Path
DB=Path('/aflow/aflow.sqlite')
ALLOWED={'auid','compound','prototype','spacegroup_relax','Egap','energy_atom','aurl'}

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--compound',default=None)
 p.add_argument('--min-gap',type=float,default=None)
 p.add_argument('--limit',type=int,default=20)
 p.add_argument('--summary',action='store_true')
 args=p.parse_args()
 if args.limit<1 or args.limit>100: raise ValueError('limit must be 1..100')
 if not DB.is_file(): raise FileNotFoundError('No AFLOW SQLite database mounted at /aflow/aflow.sqlite. Run B/import_aflow.py on B.')
 con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True)
 con.row_factory=sqlite3.Row
 try:
  if args.summary:
   result=dict(con.execute('SELECT COUNT(*) AS records, COUNT(DISTINCT compound) AS compounds FROM materials').fetchone())
  else:
   where=[]; params=[]
   if args.compound:
    where.append('compound LIKE ?');params.append('%'+args.compound+'%')
   if args.min_gap is not None:
    where.append('Egap >= ?');params.append(args.min_gap)
   statement='SELECT auid,compound,prototype,spacegroup_relax,Egap,energy_atom,aurl FROM materials'
   if where: statement+=' WHERE '+' AND '.join(where)
   statement+=' ORDER BY compound, auid LIMIT ?';params.append(args.limit)
   result=[dict(r) for r in con.execute(statement,params)]
  print(json.dumps(result,ensure_ascii=False,indent=2))
 finally: con.close()
if __name__=='__main__':
 try: main()
 except Exception as ex:
  print(json.dumps({'error':str(ex)}));sys.exit(1)
