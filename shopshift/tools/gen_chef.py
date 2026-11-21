import json, os, re, time, urllib.error
from tts import tts
L=json.load(open('chef_lines.json')); key=open('/home/claude/.gemini_key_potion').read().strip()
STYLE="Voice: a warm, encouraging head chef in his 50s teaching a young apprentice. Calm, kind, clear, and patient. Speak slowly and clearly for an 8-year-old."
for fid,text in L.items():
    out=f'voice/raw/{fid}.wav'
    if os.path.exists(out): continue
    for a in range(20):
        try: print(fid, tts(text,'Rasalgethi',STYLE,model='gemini-3.1-flash-tts-preview',out=out,key=key), flush=True); break
        except urllib.error.HTTPError as e:
            q=re.findall(r'"quotaId": "([^"]+)"',e.read().decode(errors='ignore')); print(fid,'HTTP',e.code,q,flush=True)
            if any('PerDay' in x for x in q): print('DAILY CAP'); raise SystemExit
            time.sleep(min(60,10*2**min(a,3)))
print('CHEF DONE')
