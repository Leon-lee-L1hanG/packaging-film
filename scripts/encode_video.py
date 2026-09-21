import argparse,json,subprocess,shutil
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--frames',required=True);p.add_argument('--fps',type=float,default=24);p.add_argument('--start',type=int,default=1);p.add_argument('--count',type=int,required=True);p.add_argument('--audio');p.add_argument('--copy-audio',action='store_true');p.add_argument('--out',required=True);p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe')
a=p.parse_args();folder=Path(a.frames);out=Path(a.out)
if out.exists():raise RuntimeError('Output already exists; choose a new version')
if a.count<=0 or a.fps<=0:raise RuntimeError('Positive count and fps required')
if a.copy_audio and not a.audio:raise RuntimeError('--copy-audio requires --audio')
ff=shutil.which(a.ffmpeg) or a.ffmpeg;probe=a.ffprobe or str(Path(ff).with_name('ffprobe.exe' if Path(ff).suffix=='.exe' else 'ffprobe'))
def run(args):return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
duration=a.count/a.fps;size=None
for f in range(a.start,a.start+a.count):
 path=folder/f'frame_{f:04}.png'
 with Image.open(path) as im:
  if size is None:size=im.size
  if im.size!=size:raise RuntimeError('Mixed frame dimensions')
  im.verify()
if any(v%2 for v in size):raise RuntimeError('yuv420p requires even dimensions')
if a.audio:
 meta=json.loads(run([probe,'-v','error','-show_streams','-show_format','-of','json',a.audio]));aud=next((x for x in meta['streams'] if x['codec_type']=='audio'),None)
 if aud is None:raise RuntimeError('No audio stream')
 audio_duration=float(aud.get('duration',meta['format'].get('duration',0)))
 if abs(audio_duration-duration)>.05:raise RuntimeError('Audio duration mismatch; prepare correctly timed mix first')
out.parent.mkdir(parents=True,exist_ok=True)
args=[ff,'-n','-v','error','-framerate',str(a.fps),'-start_number',str(a.start),'-i',str(folder/'frame_%04d.png')]
if a.audio:args+=['-i',a.audio]
args+=['-map','0:v:0']
if a.audio:args+=['-map','1:a:0']
args+=['-frames:v',str(a.count),'-t',str(duration),'-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','slow','-crf','16','-profile:v','high','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709']
if a.audio:args+=['-c:a','copy'] if a.copy_audio else ['-c:a','aac','-b:a','320k','-ar','48000','-ac','2']
args+=['-movflags','+faststart',str(out)]
run(args);run([ff,'-v','error','-xerror','-i',str(out),'-f','null','-'])
meta=json.loads(run([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));v=next(x for x in meta['streams'] if x['codec_type']=='video');n,d=map(int,v['r_frame_rate'].split('/'))
assert int(v['nb_read_frames'])==a.count and (v['width'],v['height'])==size and abs(n/d-a.fps)<1e-5
assert abs(float(meta['format']['duration'])-duration)<.05
report={'full_decode_ok':True,'size':size,'frames':a.count,'fps':a.fps,'duration':float(meta['format']['duration']),'audio_copied':a.copy_audio,'visual_review':'required separately'}
if a.copy_audio:
 def ah(path):return run([ff,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
 report['audio_hash_unchanged']=ah(a.audio)==ah(out)
 assert report['audio_hash_unchanged']
out.with_suffix('.verification.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report))
