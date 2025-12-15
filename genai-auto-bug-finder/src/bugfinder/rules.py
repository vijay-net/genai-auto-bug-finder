
"""Heuristic rules & fix recommendations."""
from typing import List, Dict

RULES: List[Dict] = [
    {'id':'PY001','lang':'python','condition':lambda f:f.get('danger_eval',0)==1,'title':'Use of eval()','severity':'High','explanation':'eval() can execute arbitrary code.','recommendation':'Avoid eval; use safe parsing/literal_eval.'},
    {'id':'PY002','lang':'python','condition':lambda f:f.get('danger_exec',0)==1,'title':'Use of exec()','severity':'High','explanation':'exec() executes dynamic code.','recommendation':'Refactor into functions/mappings.'},
    {'id':'PY003','lang':'python','condition':lambda f:f.get('danger_subprocess_shell',0)==1,'title':'shell=True in subprocess','severity':'Medium','explanation':'Risk of command injection.','recommendation':'Use shell=False with sanitized args.'},
    {'id':'PY004','lang':'python','condition':lambda f:f.get('danger_broad_except',0)==1,'title':'Broad except','severity':'Medium','explanation':'Hides errors; hard to debug.','recommendation':'Catch specific exceptions.'},
    {'id':'PY005','lang':'python','condition':lambda f:f.get('danger_mutable_default',0)==1,'title':'Mutable default args','severity':'Medium','explanation':'State persists across calls.','recommendation':'Default to None, init inside.'},
    {'id':'JS001','lang':'javascript','condition':lambda f:f.get('danger_eval',0)==1,'title':'Use of eval()','severity':'High','explanation':'Runs untrusted JS.','recommendation':'Avoid eval; safer parsing.'},
    {'id':'JS002','lang':'javascript','condition':lambda f:f.get('danger_innerHTML',0)==1,'title':'innerHTML assignment','severity':'High','explanation':'Potential XSS.','recommendation':'Use textContent or sanitize.'},
    {'id':'JS003','lang':'javascript','condition':lambda f:f.get('danger_document_write',0)==1,'title':'document.write()','severity':'Medium','explanation':'Deprecated; perf/security issues.','recommendation':'Use DOM APIs.'},
    {'id':'JS004','lang':'javascript','condition':lambda f:f.get('danger_var_usage',0)==1,'title':'var declarations','severity':'Low','explanation':'Hoisting bugs.','recommendation':'Prefer let/const.'},
]

def apply_rules(features: Dict) -> List[Dict]:
    lang = features.get('lang','unknown')
    return [{
        'id': r['id'],'title': r['title'],'severity': r['severity'],
        'explanation': r['explanation'],'recommendation': r['recommendation']
    } for r in RULES if r['lang']==lang and r['condition'](features)]
