"""OpenAaaS Docker executor: a task-local Pi agent using read-only AFLOW tools."""
import json,subprocess,pathlib,sys,os
work=pathlib.Path('/workspace')
def main():
 task=json.loads((work/'task.json').read_text(encoding='utf-8'))
 user_prompt=task.get('task_prompt') or task.get('prompt') or ''
 if not user_prompt.strip(): raise ValueError('task_prompt missing')
 role=os.environ.get('AFLOW_ROLE','query')
 role_instruction=('Retrieve exact AFLOW mirror records with filters and cite auid/aurl. '
                  if role=='query' else
                  'Summarize AFLOW mirror contents and provide descriptive statistics from exact records. ')
 policy=( 'You are a materials-science AFLOW database agent. '
          +role_instruction+
         'The only database is local /aflow/aflow.sqlite, populated by its owner. '
         'To inspect it call python3 /opt/aflow_tool.py --summary or --compound NAME --min-gap NUMBER --limit N using bash. '
         'Never invent AFLOW entries or numerical properties. '
         'Never use the network or access paths outside /workspace and /aflow. '
         'Write the final answer to /workspace/response.md. '
         'A complete answer must label data provenance as a local AFLOW mirror. ')
 prompt=policy+'\nUSER TASK:\n'+user_prompt+'\nOUTPUT REQUIREMENTS:\n'+str(task.get('output_prompt',''))
 # Pass prompt as argument list (no shell interpolation). The Pi model configuration must be supplied via mounted ~/.pi/agent auth.
 result=subprocess.run(['pi','-p','--tools','read,write,bash',prompt],cwd=work,capture_output=True,text=True,timeout=1800)
 (work/'agent_stdout.log').write_text(result.stdout[-50000:],encoding='utf-8')
 (work/'agent_stderr.log').write_text(result.stderr[-20000:],encoding='utf-8')
 answer=work/'response.md'
 if result.returncode != 0:
  if not answer.exists(): answer.write_text('Agent failed; inspect agent_stderr.log.\n',encoding='utf-8')
  raise RuntimeError(f'Pi exited with {result.returncode}')
 if not answer.exists():
  answer.write_text(result.stdout or 'Agent completed without textual output.',encoding='utf-8')
 print(answer.read_text(encoding='utf-8')[:10000])
if __name__=='__main__':
 try: main()
 except Exception as e:
  print('EXECUTOR_ERROR:',str(e),file=sys.stderr);sys.exit(1)
