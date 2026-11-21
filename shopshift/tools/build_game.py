import json, re
d = json.load(open('orders.json'))
import importlib.util
spec = importlib.util.spec_from_file_location('g', 'gen_orders.py')
src = open('gen_orders.py').read().split('# ---------------------------------------------------------------- math pools')[0]
ns = {}; exec(src, ns)
d['cast'] = {k: {'a': v['a'], 'b': v['b']} for k, v in ns['C'].items()}
html = open('/home/claude/cut-the-sub/shopshift/src.html').read().replace('/*DATA*/null', json.dumps(d, separators=(',', ':')))
open('/home/claude/cut-the-sub/shopshift/index.html', 'w').write(html)
print('built', len(html)//1024, 'KB')
