import json, subprocess, re
W=json.load(open('../work/warp.json'))['brasa.html']['segs']
def inv(o):
    for n0,a,n1,b in W:
        if o<=b: return n0+(n1-n0)*(o-a)/(b-a)
B=lambda o:17.65+inv(o)
I=lambda t:t if t<=15.3 else (15.3+(t-15.3)*.35/.7 if t<=16 else t-.35)
w=json.load(open('vo.json')); bd=json.load(open('vo-bounds.json'))
starts=[0,4,12,18,30,41,55,60,69,78,87,95,104]
places=[0.05,2.3,6.4,10.15,14.4,20.3,26.4,30.4,37.0,42.6,48.5,52.5,55.6]
onset={8:28.14}
vo=[]  # (file, a, b, at)
for a,b,at in [(0,1.3,.1),(1.3,5.9,1.9),(5.9,8.1,6.4),(8.1,14.65,8.6),(14.65,16.32,15.7)]: vo.append(('vo-intro.mp3',a,b,at))
for k in range(4,13):
    ws=onset.get(k,w[starts[k]]['s']); vo.append(('vo.mp3',bd[k],bd[k+1],B(places[k])-(ws-bd[k])))
def mv(f):
    o=subprocess.run(['ffmpeg','-i',f,'-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'mean_volume: ([-\d.]+)',o).group(1))
# (file, time, target mean dB)
X='sfx2/'; Y='sfx/'
cues=[(Y+'scroll.mp3',0.3,-34),(X+'scratch.mp3',I(7.0),-28),(X+'air1.mp3',I(7.85),-30),(X+'air3.mp3',I(10.55),-31),(X+'air4.mp3',I(13.2),-31),
 (X+'gl4.mp3',16.0,-32),(X+'air2.mp3',17.5,-31),
 (Y+'steps.mp3',B(15.2),-34),(Y+'steps.mp3',B(17.4),-36),
 (X+'air1.mp3',B(19.8),-30),(Y+'notif.mp3',B(21.15),-30),
 (X+'pop1.mp3',B(21.85),-30),(X+'pop2.mp3',B(23.2),-30),(X+'pop1.mp3',B(24.5),-30),(X+'pop2.mp3',B(25.75),-30),
 (X+'air4.mp3',B(25.9),-32),(Y+'typing.mp3',B(26.9),-34),(Y+'crickets.mp3',B(28.0),-36),
 (X+'gl1.mp3',B(30.1),-31),(X+'gl2.mp3',B(31.4),-33),
 (X+'air3.mp3',B(35.9),-31),(Y+'tap.mp3',B(36.95),-30),(Y+'typing.mp3',B(37.6),-35),(Y+'sent.mp3',B(38.9),-31),(Y+'cash.mp3',B(39.85),-30),
 (X+'gl3.mp3',B(41.9),-32),(X+'air2.mp3',B(44.0),-31),(X+'air1.mp3',B(46.0),-31),
 (X+'air4.mp3',B(47.9),-32),(Y+'tap.mp3',B(49.0),-31),(Y+'tap.mp3',B(50.0),-31),
 (Y+'boom.mp3',B(52.0),-28),(X+'sting.mp3',B(55.7),-26),(Y+'tap.mp3',B(58.5),-30)]
inp=[];fc=[];lab=[]
for i,(f,a,b,at) in enumerate(vo):
    inp+=['-i',f]; d=int(at*1000)
    fc.append(f'[{i}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.05:.3f}:d=0.05,adelay={d}|{d}[v{i}]'); lab.append(f'[v{i}]')
n=len(vo)
fc.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,aformat=channel_layouts=stereo,apad=whole_dur=58.4,atrim=0:58.4,volume=1.0,asplit=2[vo][key]')
inp+=['-i','trilha4.wav']; m=n
fc.append(f'[{m}:a]volume=0.55[mus0];[mus0][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=250[mus]')
sl=[]
for j,(f,at,tg) in enumerate(cues):
    k=m+1+j; inp+=['-i',f]; g=tg-mv(f); d=int(at*1000)
    fc.append(f'[{k}:a]aformat=channel_layouts=stereo,volume={g:.1f}dB,adelay={d}|{d}[s{j}]'); sl.append(f'[s{j}]')
fc.append(''.join(sl)+f'amix=inputs={len(sl)}:normalize=0,apad=whole_dur=58.4,atrim=0:58.4[sfx]')
fc.append('[vo][mus][sfx]amix=inputs=3:normalize=0,alimiter=limit=0.89,afade=t=out:st=57.6:d=0.8[out]')
cmd=['ffmpeg','-y','-v','error']+inp+['-filter_complex',';'.join(fc),'-map','[out]','-ar','48000','-t','58.4','mix-v4.wav']
subprocess.run(cmd,check=True)
for x in vo: print(x[0],round(x[1],2),round(x[2],2),'@',round(x[3],2))
