
"""Root-cause summary helpers."""
from typing import Dict, List

def summarize(findings: List[Dict]) -> Dict:
    total = len(findings)
    high = sum(1 for f in findings if f.get('severity')=='High')
    medium = sum(1 for f in findings if f.get('severity')=='Medium')
    return {'total': total, 'high': high, 'medium': medium, 'low': total-high-medium}
