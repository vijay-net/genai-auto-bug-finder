
#!/usr/bin/env python3
import argparse, json
from .bugfinder.engine import scan_file, scan_directory

def main():
    p = argparse.ArgumentParser(description='GenAI Auto Bug Finder CLI')
    p.add_argument('target')
    p.add_argument('--json', action='store_true')
    a = p.parse_args()
    res = scan_file(a.target) if (a.target.endswith('.py') or a.target.endswith('.js')) else scan_directory(a.target)
    print(json.dumps(res, indent=2) if a.json else res)

if __name__=='__main__':
    main()
