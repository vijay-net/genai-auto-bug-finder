
"""Feature extraction for Python & JS."""
from __future__ import annotations
import ast, re
from typing import Dict, Any

PY_DANGERS = {
    'eval': r"eval\(",
    'exec': r"exec\(",
    'subprocess_shell': r"subprocess\.Popen\(.*shell=True",
    'broad_except': r"except\s*:\s*",
}
JS_DANGERS = {
    'eval': r"eval\(",
    'innerHTML': r"innerHTML\s*=",
    'document_write': r"document\.write\(",
    'var_usage': r"var\s+",
}

def cyclomatic_complexity_py(src: str) -> int:
    try:
        t = ast.parse(src)
    except SyntaxError:
        return -1
    c = 1
    for n in ast.walk(t):
        if isinstance(n, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.Try, ast.With, ast.BoolOp)):
            c += 1
    return c

def count_functions_py(src: str) -> int:
    try:
        t = ast.parse(src)
    except SyntaxError:
        return 0
    return sum(1 for n in ast.walk(t) if isinstance(n, ast.FunctionDef))

def has_mutable_default_py(src: str) -> bool:
    try:
        t = ast.parse(src)
    except SyntaxError:
        return False
    for n in ast.walk(t):
        if isinstance(n, ast.FunctionDef):
            for d in n.args.defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    return True
    return False

def extract_python_features(src: str) -> Dict[str, Any]:
    lines = src.splitlines()
    return {
        'lang': 'python',
        'loc': len(lines),
        'avg_line_len': (sum(len(l) for l in lines) / max(len(lines), 1)) if lines else 0,
        'cyclomatic': cyclomatic_complexity_py(src),
        'functions': count_functions_py(src),
        'danger_eval': int(bool(re.search(PY_DANGERS['eval'], src))),
        'danger_exec': int(bool(re.search(PY_DANGERS['exec'], src))),
        'danger_subprocess_shell': int(bool(re.search(PY_DANGERS['subprocess_shell'], src))),
        'danger_broad_except': int(bool(re.search(PY_DANGERS['broad_except'], src))),
        'danger_mutable_default': int(has_mutable_default_py(src)),
    }

def extract_js_features(src: str) -> Dict[str, Any]:
    lines = src.splitlines()
    m = lambda p: int(bool(re.search(p, src)))
    return {
        'lang': 'javascript',
        'loc': len(lines),
        'avg_line_len': (sum(len(l) for l in lines) / max(len(lines), 1)) if lines else 0,
        'danger_eval': m(JS_DANGERS['eval']),
        'danger_innerHTML': m(JS_DANGERS['innerHTML']),
        'danger_document_write': m(JS_DANGERS['document_write']),
        'danger_var_usage': m(JS_DANGERS['var_usage']),
    }

def extract_features(path: str, content: str) -> Dict[str, Any]:
    if path.endswith('.py'):
        return extract_python_features(content)
    elif path.endswith('.js'):
        return extract_js_features(content)
    else:
        return {'lang': 'unknown', 'loc': len(content.splitlines()), 'avg_line_len': 0}
