
"""ML model utilities: RandomForest + heuristic fallback."""
from __future__ import annotations
from typing import Dict
import os, joblib, numpy as np

FEATURE_KEYS = [
    'loc','avg_line_len','cyclomatic','functions',
    'danger_eval','danger_exec','danger_subprocess_shell','danger_broad_except','danger_mutable_default',
    'danger_innerHTML','danger_document_write','danger_var_usage'
]
MODEL_PATH = os.environ.get('BUGFINDER_MODEL_PATH','models/rf_model.joblib')

def features_to_vector(f: Dict) -> np.ndarray:
    return np.array([float(f.get(k,0)) for k in FEATURE_KEYS], dtype=float)

def load_model():
    return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def predict_proba(f: Dict) -> float:
    m = load_model()
    if m is None:
        score = 0.1 + sum(0.2 for k in FEATURE_KEYS if k.startswith('danger_') and f.get(k,0))
        score += min(max((f.get('cyclomatic',1)-1)/10,0),0.4)
        return min(score,0.99)
    v = features_to_vector(f).reshape(1,-1)
    return float(m.predict_proba(v)[0][1])
