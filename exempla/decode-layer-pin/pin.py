#!/usr/bin/env python3
"""Independent f64 oracle and fixed-cap two-device public layer_step pin."""
import json, math, os, pathlib, re, subprocess, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKAGE = pathlib.Path(__file__).resolve().parent
# Based on decode_step.fab's documented serial-f32 contract (1e-5 absolute +
# 1e-4 relative). Fixed at 10% margin before any real-dimension execution.
ABS_CAP, REL_CAP = 1.1e-5, 1.1e-4
EPS, LN_THETA = 1e-5, 11.512925

def weight(r,c,salt): return ((r*7+c*3+salt*5)%17-8)*WEIGHT_SCALE
WEIGHT_SCALE=0.025
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def gemv(w,x): return [dot(row,x) for row in w]
def rms(x,g):
    inv=1/math.sqrt(sum(v*v for v in x)/len(x)+EPS)
    return [v*inv*z for v,z in zip(x,g)]
def rope(x,pos,dh,half=False):
    out=list(x); span=dh//2
    for head in range(len(x)//dh):
        base=head*dh
        for p in range(span):
            i,j=(base+p,base+p+span) if half else (base+2*p,base+2*p+1)
            a=pos*math.exp(-(p/span)*LN_THETA); c,s=math.cos(a),math.sin(a)
            out[i],out[j]=x[i]*c-x[j]*s,x[i]*s+x[j]*c
    return out

def reference(cfg, wrong_rope=False):
    global WEIGHT_SCALE
    D,QD,KVD,F,H,C,DH,GROUP,POS=cfg
    WEIGHT_SCALE=0.025 if D==4 else 0.001
    hin=[(j*2-3)*0.2 for j in range(D)]
    anorm=[0.8+j*0.1 for j in range(D)]; fnorm=[1.1-j*0.05 for j in range(D)]
    wq=[[weight(r,c,1) for c in range(D)] for r in range(QD)]
    wk=[[weight(r,c,2) for c in range(D)] for r in range(KVD)]
    wv=[[weight(r,c,3) for c in range(D)] for r in range(KVD)]
    wo=[[weight(r,c,4) for c in range(QD)] for r in range(D)]
    wg=[[weight(r,c,5) for c in range(D)] for r in range(F)]
    wu=[[weight(r,c,6) for c in range(D)] for r in range(F)]
    wd=[[weight(r,c,7) for c in range(F)] for r in range(D)]
    kin=[[(1+r*3+c)*.1 for c in range(KVD)] for r in range(C)]
    vin=[[-(1+r*2+c)*.07 for c in range(KVD)] for r in range(C)]
    normed=rms(hin,anorm); bad=wrong_rope
    q=rope(gemv(wq,normed),POS,DH,bad); k=rope(gemv(wk,normed),POS,DH,bad); v=gemv(wv,normed)
    kin[POS],vin[POS]=k,v
    context=[]; scale=0.5 if DH==2 else 1/math.sqrt(DH)
    for h in range(H):
        kh=h//GROUP; qh=q[h*DH:(h+1)*DH]
        scores=[dot(qh,kin[r][kh*DH:(kh+1)*DH])*scale for r in range(POS+1)]
        peak=max(scores); exps=[math.exp(z-peak) for z in scores]; den=sum(exps)
        probs=[z/den for z in exps]
        context.extend(sum(probs[r]*vin[r][kh*DH+d] for r in range(POS+1)) for d in range(DH))
    h1=[a+b for a,b in zip(hin,gemv(wo,context))]
    ff=rms(h1,fnorm); gate=gemv(wg,ff); up=gemv(wu,ff)
    act=[a/(1+math.exp(-a))*b for a,b in zip(gate,up)]
    hidden=[a+b for a,b in zip(h1,gemv(wd,act))]
    return {'hidden':hidden,'key':[x for row in kin for x in row], 'value':[x for row in vin for x in row]}

def parse_output(text,cfg):
    D,QD,KVD,F,H,C,DH,GROUP,POS=cfg; values={}
    for line in text.splitlines():
        m=re.fullmatch(r'(hidden|key|value)\[([^]]+)\]=([-+0-9.eE]+)',line.strip())
        if m:
            n,i,v=m.groups(); values.setdefault(n,{})[i]=float(v)
    counts={'hidden':D,'key':C*KVD,'value':C*KVD}; out={}
    for n,count in counts.items():
        if len(values.get(n,{}))!=count: raise AssertionError(f'missing {n}: {len(values.get(n,{}))}/{count}')
        out[n]=[values[n][str(i)] for i in range(D)] if n=='hidden' else [values[n][f'{r},{c}'] for r in range(C) for c in range(KVD)]
    return out

def errors(actual,expected):
    maxima={}
    for n,refs in expected.items():
        ds=[abs(a-b) for a,b in zip(actual[n],refs)]; caps=[ABS_CAP+REL_CAP*abs(v) for v in refs]
        if any(d>t for d,t in zip(ds,caps)):
            i=max(range(len(ds)),key=ds.__getitem__); raise AssertionError(f'{n}[{i}] error {ds[i]:.9g} exceeds fixed cap {caps[i]:.9g}')
        maxima[n]=max(ds,default=0)
    return maxima

def run_mode(faber,home,name,cfg):
    expected=reference(cfg); folder=PACKAGE if name=='tiny' else PACKAGE/'real'
    runs={}
    for device in ('reference','metal'):
        p=subprocess.run([faber,'run','--library-home',home,'--device',device,str(folder)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if p.returncode: raise RuntimeError(f'{name}/{device} failed (no skips):\n{p.stdout}')
        observed=parse_output(p.stdout,cfg); maxima=errors(observed,expected)
        runs[device]={'max_abs_error':maxima,'output':observed}
        print(f'{name}/{device}: passed; maxima {maxima}')
    return {'dimensions':dict(zip(('D','QD','KVD','F','heads','capacity','dh','group','position'),cfg)), 'devices':runs}

def main():
    faber=os.environ.get('FABER_BIN')
    if not faber or not pathlib.Path(faber).is_file(): raise SystemExit('set FABER_BIN to current faber executable')
    tiny=(4,4,2,6,2,3,2,2,1); real=(960,960,320,2560,15,4,64,3,2)
    with tempfile.TemporaryDirectory(prefix='.decode-layer-pin-home-',dir=ROOT) as home:
        pathlib.Path(home,'gradus').symlink_to(ROOT,target_is_directory=True)
        results={name:run_mode(faber,home,name,cfg) for name,cfg in (('tiny',tiny),('real',real))}
    # Red fixture: the rotate-half oracle is deliberately wrong for this layer.
    expected=reference(real,wrong_rope=True); actual=results['real']['devices']['reference']['output']
    try: errors(actual,expected)
    except AssertionError as exc:
        red={'variant':'rotate-half RoPE in oracle (layer uses consecutive pairs)','rejected':True,'reason':str(exc)}
        print('red case rejected:',exc)
    else: raise SystemExit('red case unexpectedly passed')
    receipt={'tolerance':{'absolute':ABS_CAP,'relative':REL_CAP,'basis':'10% margin over decode_step.fab documented serial-f32 cap (1e-5 + 1e-4*abs(reference)), fixed before real run'},'modes':results,'red_case':red,'result':'pass'}
    (PACKAGE/'receipt-real.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print('tiny and real layer_step pins passed on reference and metal; wrong RoPE rejected')
if __name__=='__main__':
    try: main()
    except Exception as e: raise SystemExit(str(e))
