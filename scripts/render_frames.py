import bpy,sys,argparse,json,hashlib,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--preview',action='store_true');p.add_argument('--frames');p.add_argument('--start',type=int);p.add_argument('--end',type=int)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);s=bpy.context.scene
if not s.camera:raise RuntimeError('Scene needs an authored camera')
if not bpy.data.filepath:raise RuntimeError('Save the packed animated blend before rendering')
folder=Path(a.out);folder.mkdir(parents=True,exist_ok=True)
s.render.engine='CYCLES';device='CPU';denoiser='OPENIMAGEDENOISE'
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 found=any(d.type=='OPTIX' for d in prefs.devices)
 for d in prefs.devices:d.use=found and d.type=='OPTIX'
 if found:device='GPU';denoiser='OPTIX'
except Exception as exc:print('GPU unavailable:',str(exc))
s.cycles.device=device;s.cycles.denoiser=denoiser;s.cycles.use_denoising=True;s.cycles.samples=24 if a.preview else 64
s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.09 if a.preview else .03;s.cycles.adaptive_min_samples=4 if a.preview else 8
s.render.resolution_percentage=50 if a.preview else 100;s.render.use_border=False;s.render.use_crop_to_border=False;s.render.use_persistent_data=True
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8'
sig={'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'preview':a.preview,'device':device,'denoiser':denoiser,'blender':bpy.app.version_string,'samples':s.cycles.samples,'resolution':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage]}
stamp=folder/'signature.json'
if stamp.exists() and json.loads(stamp.read_text())!=sig:raise RuntimeError('Scene/settings changed; use a new render folder')
stamp.write_text(json.dumps(sig,indent=2))
frames=list(map(int,a.frames.split(','))) if a.frames else range(a.start if a.start is not None else s.frame_start,(a.end if a.end is not None else s.frame_end)+1)
begin=time.time()
for f in frames:
 dest=folder/f'frame_{f:04}.png'
 if dest.exists() and dest.stat().st_size>0:continue
 s.frame_set(f);s.render.filepath=str(dest);bpy.ops.render.render(write_still=True)
 (folder/'progress.json').write_text(json.dumps({'frame':f,'elapsed':round(time.time()-begin,2),'device':device}))
 print('FRAME',f,flush=True)
print('RENDER_COMPLETE',flush=True)
