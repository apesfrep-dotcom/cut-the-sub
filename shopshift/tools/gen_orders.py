"""Generate Shop Shift order data + voice lines.

4 weeks x 5 shifts x 8 orders = 160 orders. Each of the 20 customers appears
exactly 8 times (rotation), with lines fixed so they can be voiced.

Order types
  split : cut a sub into n equal pieces. Player places the first cut (1/n);
          the game copies that piece down the sub (iterating the unit).
  cut   : cut at num/den of the sub (wholes=2 -> two subs end to end, 0..2).
  fair  : two pieces of same-size subs; who got more? answer a|b|same.
  same  : sub pre-cut into D pieces; tap pieces to make num/den. answer k.
  left  : num/den already eaten; choose how much is left. answer (d-n)/d.

Ruler (fades by week): 1 full ticks, 2 halves only, 3 none, 4 none + 0..2 lines.
"""
import json, random
from fractions import Fraction as F

R = random.Random(20261120)

WORD = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',11:'eleven',12:'twelve'}
DEN1 = {2:'half',3:'third',4:'fourth',6:'sixth',8:'eighth'}
DENP = {2:'halves',3:'thirds',4:'fourths',6:'sixths',8:'eighths'}

def say(n, d):
    if d == 2 and n == 1: return 'one half'
    return f"{WORD[n]} {DEN1[d] if n == 1 else DENP[d]}"

def say_mixed(n, d):
    w, r = divmod(n, d)
    if r == 0: return f"{WORD[w]} whole sub" + ("s" if w > 1 else "")
    return f"{WORD[w]} and {say(r, d)}"

# ---------------------------------------------------------------- customers
C = {
 'rose':    dict(name='Grandma Rose', who='my grandkids', a='Sophie', b='Ben',
                 open=["Hello, sweetheart!", "Oh good, you're working today!", "Hi, dear."],
                 happy=["Oh, that's just perfect, sweetheart!", "You have such careful hands. Thank you!"],
                 unsure=["Hmm, that doesn't look quite right, dear.", "Oh my. Let's look at that one again."]),
 'marco':   dict(name='Marco', who='the guys at my shop', a='my nephew', b='my cousin',
                 open=["Ciao, my friend!", "Ah, my favorite sub cutter!", "Buongiorno!"],
                 happy=["Bellissimo! Exactly right!", "Perfetto! You cut like a pro."],
                 unsure=["Eh, not quite, my friend.", "Hmm. Measure twice, cut once!"]),
 'twins':   dict(name='The Patel Twins', who='our birthday party', a='Arjun', b='Priya',
                 open=["Hi! We're back!", "Hey! It's us again!", "Hi! We need your help!"],
                 happy=["Yes! That's totally fair!", "Woo-hoo! You got it!"],
                 unsure=["Wait... that doesn't look right.", "Hmm, are you sure about that?"]),
 'rivera':  dict(name='Coach Rivera', who='my team', a='my goalie', b='my striker',
                 open=["Hey there, chef!", "Big game today!", "Hey, champ!"],
                 happy=["That's a winner! Great job!", "Nailed it! High five!"],
                 unsure=["Hmm, let's run that play again.", "Not quite. Take another look."]),
 'kim':     dict(name='Ms. Kim', who='my class', a='Maya', b='Leo',
                 open=["Good morning!", "Hi there! I've got a math problem for you.", "Hello again!"],
                 happy=["Wonderful! That's exactly right.", "Gold star for you!"],
                 unsure=["Hmm, let's check that together.", "Close, but take another look."]),
 'lily_max':dict(name='Lily and Max', who='our cousins', a='Lily', b='Max',
                 open=["Hi! Hi!", "We're hungry!", "Hi! Mom sent us!"],
                 happy=["Yay! Thank you!", "That's awesome!"],
                 unsure=["Uh oh. That doesn't look fair.", "Hmm... wait a second."]),
 'carmen':  dict(name='Abuela Carmen', who='my family', a='my son', b='my daughter',
                 open=["Hola, mijo!", "Buenas tardes!", "Hola, hola!"],
                 happy=["Muy bien! That's perfect.", "Ay, que bueno! Thank you."],
                 unsure=["Ay, no, no. Look again, mijo.", "Hmm, that's not quite it."]),
 'jasmine': dict(name='Jasmine', who='my study group', a='my roommate', b='me',
                 open=["Hey!", "Hi! Quick lunch break.", "Hey, it's me again!"],
                 happy=["Yes! Thank you so much!", "Perfect, that's exactly what I needed."],
                 unsure=["Hmm, I don't think that's right.", "Wait, can you double-check that?"]),
 'okafor':  dict(name='Mr. Okafor', who='my tour group', a='my brother', b='me',
                 open=["Good afternoon!", "Hello, my friend!", "Afternoon!"],
                 happy=["Excellent work! Thank you.", "Very good! Spot on."],
                 unsure=["Hmm. I don't think so, my friend.", "Not quite. Try once more."]),
 'garcia':  dict(name='Mrs. Garcia', who='my office', a='my boss', b='my assistant',
                 open=["Hi! I've got the office order.", "Hello! Busy day at work.", "Hi there!"],
                 happy=["Great, that's exactly right!", "Perfect! The office will love it."],
                 unsure=["Hmm, that's not what's on my list.", "Hold on, that doesn't look right."]),
 'fire':    dict(name='Captain Reyes', who='the fire station crew', a='my rookie', b='my lieutenant',
                 open=["Hey there! Station lunch run.", "Hi! The crew's starving.", "Afternoon!"],
                 happy=["Right on target! Thanks!", "That's a five-alarm cut! Great job."],
                 unsure=["Hmm, that's off a bit.", "Let's take another look at that."]),
 'singh':   dict(name='Dr. Singh', who='the nurses on my floor', a='my nurse', b='my intern',
                 open=["Hi! I'm on a quick break.", "Hello! Lunch for the hospital.", "Hi there."],
                 happy=["Perfect. That's precise!", "Excellent. Thank you!"],
                 unsure=["Hmm, I don't think that's right.", "Let's double-check that one."]),
 'hank':    dict(name='Hank', who='my construction crew', a='my welder', b='my foreman',
                 open=["Howdy!", "Hey, bud!", "Crew's hungry again!"],
                 happy=["That's a clean cut! Nice work.", "Right on the money!"],
                 unsure=["Hmm, that's not level, bud.", "Measure that one again."]),
 'lou':     dict(name='Lou', who='my fishing buddies', a='my buddy Earl', b='me',
                 open=["Morning, kid!", "Well hello there!", "Hey, kid!"],
                 happy=["Now that's a keeper!", "Ha! Perfect. Thanks, kid."],
                 unsure=["Hmm, not quite, kid.", "Eh, that one got away from you."]),
 'brooks':  dict(name='Officer Brooks', who='my patrol team', a='my partner', b='me',
                 open=["Hi there!", "Afternoon!", "Hello again!"],
                 happy=["Fair and square. Thank you!", "Exactly right. Nice job."],
                 unsure=["Hmm, I don't think that's right.", "Let's look at the evidence again."]),
 'tasha':   dict(name='Coach Tasha', who='my soccer team', a='my goalie', b='my captain',
                 open=["Hey! Practice just ended.", "Hi! Team snack time.", "Hey there!"],
                 happy=["Goal! That's perfect!", "Great teamwork! Thanks!"],
                 unsure=["Hmm, that's offside.", "Not quite. Let's try that again."]),
 'band':    dict(name='The Garage Band', who='the band', a='Jax', b='Vee',
                 open=["Yo!", "Hey! We just finished practice.", "What's up!"],
                 happy=["Yeah! That rocks!", "Awesome! You're a rock star."],
                 unsure=["Hmm. That's a little off-key.", "Wait, that doesn't sound right."]),
 'sam':     dict(name='Sam', who='the post office crew', a='my coworker', b='me',
                 open=["Hi! Mail's done for the day.", "Hey! Lunch break.", "Hi again!"],
                 happy=["Special delivery! Thank you!", "That's exactly right. Thanks!"],
                 unsure=["Hmm, return to sender.", "I don't think that's right."]),
 'theo':    dict(name='Theo', who='my scout troop', a='Owen', b='me',
                 open=["Hi! I'm on a troop mission!", "Hello! Scout lunch!", "Hi! It's me, Theo!"],
                 happy=["Awesome! That earns a badge!", "Yes! Thank you!"],
                 unsure=["Hmm, I don't think that's right.", "Wait, can you check that?"]),
 'dale':    dict(name='Dale', who='my ranch hands', a='my son', b='my neighbor',
                 open=["Howdy, partner.", "Afternoon.", "Well, howdy."],
                 happy=["Yep. That's a fine cut.", "Good work, partner."],
                 unsure=["Nope. Not quite, partner.", "Hmm. Let's try that again."]),
}
ORDER = ['rose','marco','twins','rivera','kim','lily_max','carmen','jasmine','okafor','garcia',
         'fire','singh','hank','lou','brooks','tasha','band','sam','theo','dale']
assert set(ORDER) == set(C)

# --------------------------------------------------------- math pools by week
DENS = {1:[2,4,8], 2:[2,3,4,6], 3:[2,3,4,6,8], 4:[2,3,4,6,8]}
def proper(d): return [(n, d) for n in range(1, d)]

def pick_cut(w):
    d = R.choice(DENS[w])
    if w == 4 and R.random() < 0.6:     # beyond one whole
        d = R.choice([2,3,4])
        n = R.choice([k for k in range(d+1, 2*d) ])
        return dict(num=n, den=d, wholes=2)
    n, d = R.choice(proper(d))
    return dict(num=n, den=d, wholes=1)

def pick_split(w):
    return dict(n=R.choice({1:[2,4,8],2:[3,6,4],3:[3,6,8,4],4:[3,6,8]}[w]))

def pick_fair(w):
    while True:
        if w == 1:
            d1, d2 = R.choice([(2,4),(4,8),(2,8),(4,4),(8,8)])
        elif w == 2:
            d1, d2 = R.choice([(3,6),(2,3),(3,4),(6,6),(2,6),(3,3)])
        else:
            d1, d2 = R.sample([2,3,4,6,8], 2)
        f1 = R.choice(proper(d1)); f2 = R.choice(proper(d2))
        if w >= 3 and R.random() < 0.35:      # same numerator, different denominators
            n = R.choice([1,2,3]); ds = [d for d in [2,3,4,6,8] if d > n]
            if len(ds) >= 2:
                d1, d2 = R.sample(ds, 2); f1, f2 = (n, d1), (n, d2)
        if f1 == f2: continue
        a, b = F(*f1), F(*f2)
        ans = 'a' if a > b else 'b' if b > a else 'same'
        return dict(a=list(f1), b=list(f2), answer=ans)

def pick_same(w):
    opts = {1:[((1,2),4),((1,2),8),((1,4),8),((3,4),8),((1,2),4)],
            2:[((1,3),6),((2,3),6),((1,2),6),((1,2),4),((1,3),6)],
            3:[((1,2),8),((3,4),8),((2,3),6),((1,2),6),((1,4),8)],
            4:[((2,3),6),((3,4),8),((1,2),8),((1,3),6),((1,2),6)]}[w]
    (n, d), D = R.choice(opts)
    return dict(num=n, den=d, pieces=D, answer=n*D//d)

def pick_left(w):
    d = R.choice({1:[2,4,8],2:[3,4,6],3:[3,4,6,8],4:[3,6,8]}[w])
    n = R.choice(range(1, d))
    ln, ld = d-n, d
    # 3 choices: correct (unsimplified, same denominator as eaten), the eaten amount, and a near miss
    wrong = {(n, d)}
    near = (d-n+1, d) if d-n+1 < d else (d-n-1, d)
    if near[0] > 0 and near != (ln, ld): wrong.add(near)
    choices = [list(x) for x in {(ln, ld), *wrong}]
    R.shuffle(choices)
    return dict(num=n, den=d, choices=choices, answer=[ln, ld])

PICK = dict(split=pick_split, cut=pick_cut, fair=pick_fair, same=pick_same, left=pick_left)

# types per shift (8 each). Week 1 introduces modes one shift at a time.
PLAN = {
 (1,1): ['split','cut','split','cut','split','cut','split','cut'],
 (1,2): ['cut']*5 + ['split']*3,
 (1,3): ['fair']*3 + ['cut']*3 + ['split']*2,
 (1,4): ['same']*3 + ['fair']*2 + ['cut']*2 + ['split'],
 (1,5): ['left']*3 + ['same']*2 + ['fair'] + ['cut'] + ['split'],
}
MIX = ['split','cut','cut','fair','same','left','fair','cut']
for wk in (2,3,4):
    for sh in range(1,6): PLAN[(wk,sh)] = MIX[:]

RULER = {1:'boxes',2:'ticks',3:'ends',4:'none'}
# -------------------------------------------------------------------- lines
def line(cid, t, p, k):
    c = C[cid]; o = c['open'][k % 3]
    if t == 'split':
        n = p['n']
        return f"{o} I need this sub cut into {WORD[n]} equal pieces for {c['who']}."
    if t == 'cut':
        if p['wholes'] == 2:
            return f"{o} We need {say_mixed(p['num'], p['den'])} subs for {c['who']}. Cut it right there."
        return [f"{o} Just {say(p['num'],p['den'])} of the sub for me, please.",
                f"{o} Could you cut me {say(p['num'],p['den'])} of this sub?",
                f"{o} I'd like {say(p['num'],p['den'])} of the sub, please."][k % 3]
    if t == 'fair':
        A, B = c['a'], c['b']
        fa, fb = say(*p['a']), say(*p['b'])
        if B == 'me':
            return f"{o} {A[0].upper()+A[1:]} got {fa} of a sub, and I got {fb} of the same size sub. Who got more?"
        return f"{o} {A[0].upper()+A[1:]} got {fa} of a sub, and {B} got {fb} of the same size sub. Is that fair? Who got more?"
    if t == 'same':
        return f"{o} I wanted {say(p['num'],p['den'])} of a sub, but it's already cut into {DENP[p['pieces']]}. Can you give me the right number of pieces?"
    if t == 'left':
        return f"{o} I already ate {say(p['num'],p['den'])} of my sub. How much is left for later?"

orders, seen = [], {}
for wk in range(1,5):
    for sh in range(1,6):
        s = (wk-1)*5 + (sh-1)
        custs = [ORDER[(s*8 + j) % 20] for j in range(8)]
        types = PLAN[(wk,sh)]
        for j, (cid, t) in enumerate(zip(custs, types)):
            # avoid exact repeats of the same problem for the same customer
            for _ in range(50):
                p = PICK[t](wk)
                if (wk, sh) == (1, 1):   # gentle first shift
                    if t == 'split': p = dict(n=[2,4,2,4][j//2])
                    if t == 'cut': p = dict(num=[1,1,3,1][j//2], den=[2,4,4,2][j//2], wholes=1)
                key = (cid, t, json.dumps(p, sort_keys=True))
                if key not in seen: break
            seen[key] = 1
            k = sum(1 for o in orders if o['cust'] == cid)
            orders.append(dict(id=f"{cid}_o{k+1}", cust=cid, week=wk, shift=sh, type=t,
                               ruler=RULER[wk], **p,
                               line=line(cid, t, p, k)))


# ============================================================ NEW ORDER TYPES (v2)
# Added on top of the original 160 so their voice lines stay valid.
R2 = random.Random(777)
FOODS = {1:['baguette'], 2:['flatbread','churro'], 3:['hot_dog','licorice','churro'], 4:['baguette','flatbread','hot_dog']}
FOODW = {'baguette':'baguette','flatbread':'flatbread','churro':'churro','hot_dog':'hot dog','licorice':'licorice rope'}
NEWPLAN = {(1,1):[], (1,2):['name','name'], (1,3):['fix','fix'], (1,4):['two','two'], (1,5):['lineup','lineup']}
ROT = ['name','fix','two','lineup']
for wk in (2,3,4):
    for sh in range(1,6):
        k = (wk*5+sh)*2
        NEWPLAN[(wk,sh)] = [ROT[k%4], ROT[(k+1)%4]]

def p_name(w):
    d = R2.choice(DENS[w]); n = R2.randrange(1, d)
    cands = []
    if n+1 < d: cands.append((n+1, d))        # counted the lines, not the spaces
    if n-1 > 0: cands.append((n-1, d))
    if n+1 <= d: cands.append((n, d+1) if d+1 in (3,4,5,6,7,8,9) else (n+1, d+2))
    for m in DENS[w]:
        for k in range(1, m): cands.append((k, m))
    out = [(n, d)]
    for c in cands:
        if len(out) == 3: break
        if c[0] < c[1] and F(*c) != F(n, d) and all(F(*c) != F(*x) for x in out): out.append(c)
    R2.shuffle(out)
    return dict(num=n, den=d, choices=[list(x) for x in out], answer=[n, d])

def p_fix(w):
    d = R2.choice(DENS[w]); n = R2.randrange(1, d)
    right = R2.random() < 0.35
    if right: at = n/d
    else:
        err = R2.choice(['lines', 'over', 'under'])
        if err == 'lines' and n < d-1: at = n/(d+1)*1.0 if R2.random()<.5 else (n+1)/d
        elif err == 'over': at = min(.97, n/d + R2.choice([.08, .12]))
        else: at = max(.03, n/d - R2.choice([.08, .12]))
        if abs(at - n/d) < .05: at = min(.97, n/d + .1)
    return dict(num=n, den=d, at=round(at, 4), right=right)

PAIRS = {1:[((1,4),(2,4)),((1,2),(1,4)),((1,4),(1,2)),((1,8),(3,8)),((3,8),(2,8)),((2,4),(1,4))],
         2:[((1,3),(1,3)),((1,6),(3,6)),((2,6),(2,6)),((1,3),(2,6)),((1,4),(2,4)),((1,6),(2,6))],
         3:[((1,4),(1,2)),((2,8),(3,8)),((1,3),(1,6)),((1,2),(1,3)),((3,8),(1,2)),((1,6),(1,2))],
         4:[((1,2),(1,3)),((1,4),(5,8)),((2,6),(1,2)),((3,8),(1,4)),((1,3),(1,2)),((1,8),(3,4))]}
def p_two(w):
    a, b = R2.choice(PAIRS[w]); assert F(*a) + F(*b) < 1
    return dict(a=list(a), b=list(b))

def p_lineup(w):
    while True:
        ds = [R2.choice(DENS[w]) for _ in range(3)]
        fr = [(R2.randrange(1, d), d) for d in ds]
        vals = [F(*x) for x in fr]
        if len(set(vals)) == 3 and min(abs(a-b) for i,a in enumerate(vals) for b in vals[i+1:]) >= F(1,8):
            return dict(fracs=[list(x) for x in fr])

NEWPICK = dict(name=p_name, fix=p_fix, two=p_two, lineup=p_lineup)

def new_line(cid, t, p, k, food):
    c = C[cid]; o = c['open'][(k+1) % 3]; fw = FOODW[food]
    if t == 'name':
        return f"{o} Somebody already cut this {fw} for me. What fraction is my piece, from the left end?"
    if t == 'fix':
        return f"{o} I asked for {say(p['num'],p['den'])} of the {fw}, and the new kid cut it. Is that cut right?"
    if t == 'two':
        A = c['a'][0].upper()+c['a'][1:]; B = c['b']
        bw = "I want" if B == 'me' else f"{B} wants"
        return f"{o} {A} wants {say(*p['a'])} of the {fw}, and {bw} {say(*p['b'])}. Cut {c['a']}'s piece first, then the next piece right after it."
    if t == 'lineup':
        f = [say(*x) for x in p['fracs']]
        return f"{o} Three orders for this {fw}: {f[0]}, {f[1]}, and {f[2]}. Can you put each ticket where its cut goes?"

new_orders = []
nk = {}
for wk in range(1,5):
    for sh in range(1,6):
        s = (wk-1)*5 + (sh-1)
        for j, t in enumerate(NEWPLAN[(wk,sh)]):
            cid = ORDER[(s*2 + j + 7) % 20]
            k = nk.get(cid, 0); nk[cid] = k + 1
            food = FOODS[wk][(s + j) % len(FOODS[wk])]
            p = NEWPICK[t](wk)
            new_orders.append(dict(id=f"{cid}_n{k+1}", cust=cid, week=wk, shift=sh, type=t, food=food,
                                   ruler=RULER[wk], pos=[3, 6][j], **p, line=new_line(cid, t, p, k, food)))

# Friday inspector: bare number line, like a test question
INSP = dict(name='Inspector Hale',
            intro=["Inspection time. No food today, just a number line. Show me what you learned this week.",
                   "Hello again. Same rules: a plain number line. Let's see how you do.",
                   "Inspection day. No ruler marks, no food. Just you and the number line.",
                   "Final inspection. This number line goes from zero to two. Take your time."],
            happy=["Excellent. That passes inspection.", "Very good. I'm impressed."],
            unsure=["Hmm. That won't pass inspection.", "Let's look at that more carefully."])
boss = []
for wk in range(1,5):
    items = []
    if wk < 4:
        d = R2.choice(DENS[wk]); n = R2.randrange(1, d)
        items.append(dict(type='cut', num=n, den=d, wholes=1, line=f"Show me where {say(n,d)} goes on this number line."))
    else:
        d = R2.choice([2,3,4]); n = R2.randrange(d+1, 2*d)
        items.append(dict(type='cut', num=n, den=d, wholes=2, line=f"Show me where {say_mixed(n,d)} goes on this number line."))
    pn = p_name(wk); items.append(dict(type='name', **pn, line="What fraction is at this point on the number line?"))
    pl = p_lineup(wk); f = [say(*x) for x in pl['fracs']]
    items.append(dict(type='lineup', **pl, line=f"Put {f[0]}, {f[1]}, and {f[2]} where they belong on the number line."))
    for i, it in enumerate(items):
        it.update(id=f"inspector_w{wk}_{i+1}", cust='inspector', week=wk, shift=5, bare=True, ruler='bare', food=None)
        it.setdefault('wholes', 1)
        boss.append(it)


# ---- v3: remove "line them up" (too many fractions at once); replace with single-fraction orders.
R3 = random.Random(4242)
for idx, o in enumerate(new_orders):
    if o['type'] != 'lineup': continue
    wk = o['week']; cid = o['cust']; fw = FOODW[o['food']]; c = C[cid]
    for key in ('fracs',): o.pop(key, None)
    opener = c['open'][(idx+2) % 3]
    if idx % 2 == 0:
        d = R3.choice(DENS[wk]); n = R3.randrange(1, d)
        cands = [(n+1,d) if n+1<d else (n-1,d)]
        for m in DENS[wk]:
            for k in range(1,m): cands.append((k,m))
        out=[(n,d)]
        for cc in cands:
            if len(out)==3: break
            if cc[0]>0 and cc[0]<cc[1] and all(F(*cc)!=F(*x) for x in out): out.append(cc)
        R3.shuffle(out)
        o.update(type='name', num=n, den=d, choices=[list(x) for x in out], answer=[n,d],
                 line=f"{opener} Somebody already cut this {fw} for me. What fraction is my piece, from the left end?")
    else:
        d = R3.choice(DENS[wk]); n = R3.randrange(1, d)
        o.update(type='cut', num=n, den=d, wholes=1, line=f"{opener} Could you cut me {say(n,d)} of this {fw}?")
    o['id'] = o['id'].replace('_n', '_m')
for o in boss:
    if o['type'] != 'lineup': continue
    o.pop('fracs', None); wk = o['week']
    d = R3.choice(DENS[wk]); n = R3.randrange(1, d)
    o.update(type='cut', num=n, den=d, wholes=1, id=o['id']+'b', line=f"Last one. Show me where {say(n,d)} goes on this number line.")

# Surprise events: one per shift (none in the very first shift)
EV = ['vip','outage','dog']
events = {}
for s in range(1, 20):
    wk = s//5 + 1
    kinds = [e for e in EV if not (e == 'outage' and wk == 4)]
    events[s] = dict(kind=R2.choice(kinds), at=R2.randrange(1, 9))

# --------------------------------------------------------------- self-check
from collections import Counter
cnt = Counter(o['cust'] for o in orders)
assert all(v == 8 for v in cnt.values()), cnt
for o in orders:
    if o['type'] == 'fair':
        a, b = F(*o['a']), F(*o['b'])
        assert o['answer'] == ('a' if a > b else 'b' if b > a else 'same')
    if o['type'] == 'same':
        assert F(o['answer'], o['pieces']) == F(o['num'], o['den'])
    if o['type'] == 'left':
        assert F(*o['answer']) == 1 - F(o['num'], o['den']) and o['answer'] in o['choices']
    if o['type'] == 'cut':
        assert 0 < F(o['num'], o['den']) < o['wholes']

reactions = {cid: dict(happy=C[cid]['happy'], unsure=C[cid]['unsure']) for cid in ORDER}
names = {cid: C[cid]['name'] for cid in ORDER}
for o in new_orders:
    if o['type']=='two': assert F(*o['a'])+F(*o['b'])<1
    if o['type']=='name': assert o['answer'] in o['choices'] and len(o['choices'])==3, o
reactions['inspector'] = dict(happy=INSP['happy'], unsure=INSP['unsure'])
names['inspector'] = INSP['name']
json.dump(dict(orders=orders, new=new_orders, boss=boss, insp_intro=INSP['intro'], events=events,
               reactions=reactions, names=names), open('orders.json','w'), indent=1)
print('new', len(new_orders), Counter(o['type'] for o in new_orders), 'boss', len(boss))
print(len(orders), 'orders;', Counter(o['type'] for o in orders))
for o in orders[:3] + orders[-3:]: print(o['id'], o['type'], o['line'])
