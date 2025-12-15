
from src.bugfinder.engine import scan_directory
if __name__=='__main__':
    findings = scan_directory('data/sample_code')
    for f in findings:
        print(f["path"], '->', f['severity'], f['ml_score'])
        for r in f.get('rule_matches', []):
            print('  -', r['id'], r['title'], 'fix:', r['recommendation'])
