
"""Scanning engine."""
from __future__ import annotations
import os
from typing import List, Dict
from .features import extract_features
from .model import predict_proba
from .rules import apply_rules

SUPPORTED_EXT = {'.py','.js'}

def scan_file(path: str) -> Dict:
    try:
        with open(path,'r',encoding='utf-8',errors='ignore') as fh:
            content = fh.read()
    except Exception as e:
        return {'path': path, 'error': str(e)}
    feats = extract_features(path, content)
    rules = apply_rules(feats)
    prob = predict_proba(feats)
    severity = 'High' if prob>=0.7 else ('Medium' if prob>=0.4 else 'Low')
    return {'path': path,'lang': feats.get('lang'),'features': feats,'ml_score': prob,'severity': severity,'rule_matches': rules,'suggestions': [r['recommendation'] for r in rules]}

def scan_directory(root: str) -> List[Dict]:
    out = []
    for dp,_,files in os.walk(root):
        for name in files:
            ext = os.path.splitext(name)[1]
            if ext in SUPPORTED_EXT:
                out.append(scan_file(os.path.join(dp,name)))
    return out
