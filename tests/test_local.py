import pathlib,subprocess,tempfile,sqlite3,sys,json,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td)
 csv=p/'aflow.csv'
 # Fixtures are clearly synthetic and are never shipped as an AFLOW dataset.
 csv.write_text('auid,compound,Egap,aurl\nTEST-0001,DemoX,1.2,https://invalid.example/demo\n',encoding='utf-8')
 db=p/'aflow.sqlite'
 r=subprocess.run([sys.executable,str(ROOT/'B/import_aflow.py'),str(csv),'--output',str(db)],capture_output=True,text=True)
 assert r.returncode==0,r.stderr
 con=sqlite3.connect(db)
 assert con.execute('select count(*) from materials').fetchone()[0]==1
 assert con.execute('select Egap from materials').fetchone()[0]==1.2
 con.close()
 assert 'base_url = "https://YOUR-C-DOMAIN"' in (ROOT/'B/config/agent-query.toml.example').read_text()
 assert not (ROOT/'B/aflow-data/aflow.sqlite').exists()
 print('PASS: CSV import, schema, example C URL, no fake AFLOW database')
