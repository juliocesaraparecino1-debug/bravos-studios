import json, subprocess, re, sys
K='/home/user/bravos-studios/ferramentas/sfx-kit'
meta={s['id']:s for s in json.load(open(K+'/sounds.json'))['sounds']}
DUR=57.4
# (sound id, time the sound's sync point must hit, target peak dBFS)
C=[]
def c(i,t,db): C.append((i,t,db))
# A hook
for t,i,db in [(.05,'swipe-slow-soft',-19),(.55,'swipe-medium-soft',-21),(1.0,'swipe-fast-soft',-24)]: c(i,t,db)
c('click-tap-firm',1.8,-17); c('pop-large-in',1.86,-19)
# B intro
c('whoosh-medium-medium',2.55,-17); c('pop-large-bubble',2.82,-18); c('whoosh-fast-soft',3.22,-21); c('zip-out-soft',4.1,-22)
c('pop-medium-in',4.9,-20); c('pop-small-in',5.22,-22); c('transform-morph',5.5,-22); c('pop-large-in',5.78,-18); c('shimmer-short-bright',6.1,-24); c('tone-ding-high',6.1,-23)
# C midias
c('whoosh-medium-soft',6.68,-19); c('click-toggle-on-firm',7.78,-16); c('pop-medium-in',7.82,-20)
for t0,lab in [(8.58,'Posts'),(9.04,'Reels'),(9.42,'Motion')]:
    c('zip-in-soft',t0+.6,-21); c('pop-small-bubble',t0+.35,-23)
c('click-tap-medium',10.5,-17); c('notification-message-in-soft',10.6,-21)
# D graficos
c('swish-medium',11.4,-21); c('whoosh-medium-medium',11.6,-18); c('notification-success-clear',12.62,-20)
c('zip-in-soft',13.95,-21); c('swish-medium',14.7,-22); c('zip-in-medium',15.85,-21); c('zip-in-hard',16.4,-22)
for t in (13.7,14.9,15.6,16.2): c('pop-small-bubble',t,-25)
c('move-spring',17.4,-24)
# E diferencial
c('reverse-whoosh-medium-soft',17.85,-20); c('boom-hit-soft',17.9,-21)
c('boom-hit-soft',20.48,-19); c('pop-large-in',20.6,-22); c('bass-808-short',21.16,-19); c('pop-medium-in',21.3,-23)
# F barber
c('whoosh-slow-soft',22.45,-19); c('pop-large-bubble',23.18,-20)
scr=[(26.14,'swipe-fast-firm'),(27.82,'swipe-medium-soft'),(29.04,'swipe-fast-soft'),(31.0,'swipe-slow-soft'),(32.24,'swipe-medium-firm'),(33.1,'swipe-fast-firm')]
for t,i in scr: c('click-tap-soft',t-.2,-24); c(i,t-.1,-22)
for t,i in [(26.3,'pop-medium-in'),(27.95,'pop-small-in'),(29.2,'pop-medium-bubble'),(31.15,'pop-small-in'),(32.4,'pop-medium-in'),(33.25,'pop-small-bubble')]: c(i,t,-23)
c('notification-success-soft',33.7,-22)
# G referencia
c('whoosh-medium-soft',34.72,-19); c('pop-large-in',35.55,-21)
c('swipe-slow-firm',36.6,-23); c('swipe-medium-soft',38.1,-24); c('swipe-slow-soft',39.7,-24)
for t,i in [(37.8,'pop-medium-in'),(38.55,'pop-small-bubble'),(39.7,'pop-medium-bubble'),(40.4,'pop-small-in'),(41.1,'pop-medium-in')]: c(i,t,-23)
c('swipe-fast-firm',41.55,-21); c('notification-message-in-clear',43.0,-18)
# H trio
c('whoosh-medium-medium',43.6,-19)
c('tone-step-1',43.54,-21); c('tone-step-2',44.2,-21); c('tone-step-3',45.02,-21)
c('bass-sub-drop-short',45.95,-22); c('move-zoom-in',46.5,-23)
# I 24h
c('reverse-whoosh-short-soft',48.95,-19); c('boom-hit-medium',49.06,-16); c('transform-fill',49.1,-27); c('pop-large-in',49.64,-20)
# J fechamento
c('whoosh-slow-medium',51.15,-18); c('pop-large-bubble',51.06,-20); c('pop-large-in',51.2,-22); c('whoosh-fast-soft',51.7,-22)
c('sting-bold-short',51.98,-17); c('pop-medium-in',54.5,-19); c('click-button-firm',54.62,-16); c('shimmer-medium-soft',54.75,-24)
json.dump(C,open('cues.json','w'))
inp=['-i','vo.wav','-i','/home/user/bravos-studios/video/audio/trilha.mp3']; fc=[]
fc.append(f'[0:a]aformat=channel_layouts=stereo,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vo][key]')
fc.append(f'[1:a]aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=PTS-STARTPTS,extrastereo=m=3.2,equalizer=f=2500:t=q:w=1.0:g=-5,equalizer=f=900:t=q:w=1.0:g=-3,volume=0.3,afade=t=in:d=0.8,afade=t=out:st={DUR-2.6}:d=2.6[m0];[m0][key]sidechaincompress=threshold=0.012:ratio=10:attack=10:release=380[mus]')
def peak(f):
    o=subprocess.run(['ffmpeg','-i',f,'-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'max_volume: ([-\d.]+)',o).group(1))
labs=[]
for j,(i,t,db) in enumerate(C):
    m=meta[i]; f=K+'/'+m['file']; start=max(0,t-m['sync']['at']); g=db-peak(f); d=int(start*1000)
    inp+=['-i',f]; k=2+j
    pn=[.8,.2][j%2] if len(C)>0 else .5
    fc.append(f'[{k}:a]aformat=channel_layouts=stereo,pan=stereo|c0={2*(1-pn):.2f}*c0+{2*pn-1 if pn>.5 else 0:.2f}*c1|c1={2*pn:.2f}*c1+{2*(1-pn)-1 if pn<.5 else 0:.2f}*c0,volume={g:.1f}dB,adelay={d}|{d},apad=whole_dur={DUR},atrim=0:{DUR}[s{j}]'); labs.append(f'[s{j}]')
fc.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0[sfx]')
fc.append('[vo][mus][sfx]amix=inputs=3:normalize=0,alimiter=limit=0.89[out]')
subprocess.run(['ffmpeg','-y','-v','error']+inp+['-filter_complex',';'.join(fc),'-map','[out]','-ar','48000','-t',str(DUR),'mix-pre.wav'],check=True)
print(len(C),'cues')
