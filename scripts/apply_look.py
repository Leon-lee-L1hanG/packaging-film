import bpy,sys,argparse,json
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--out',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);dest=Path(a.out)
if dest.exists():raise RuntimeError('Output already exists; choose a new version')
P=Path(__file__).resolve().parents[1];cfg=json.loads(Path(a.config).read_text(encoding='utf-8-sig'));manifest=json.loads((P/'references/look-manifest.json').read_text(encoding='utf8'))
mapping=cfg.get('materials',{});bounds=cfg.get('bounds_objects',[])
for name in list(mapping)+bounds:
 if name not in bpy.data.objects:raise RuntimeError('Unknown object: '+name)
with bpy.data.libraries.load(str(P/'assets/approved-look.blend'),link=False) as (src,dst):
 for mat in mapping.values():
  if mat not in src.materials:raise RuntimeError('Unknown library material: '+mat)
 names=list(dict.fromkeys(mapping.values()));dst.materials=names[:]
 if cfg.get('lighting',False):
  if not bounds:raise RuntimeError('Explicit bounds_objects required for lighting')
  dst.worlds=[manifest['world']];dst.objects=[x['name'] for x in manifest['lights']]
mats=dict(zip(names,dst.materials))
for name,matname in mapping.items():
 o=bpy.data.objects[name];m=mats[matname]
 if o.type!='MESH':raise RuntimeError('Expected mesh for material mapping: '+name)
 required={n.uv_map for n in m.node_tree.nodes if n.type=='UVMAP' and n.uv_map}
 missing=required-{u.name for u in o.data.uv_layers}
 if missing:raise RuntimeError(f'{name} missing UV maps {missing}; prepare UVs before applying')
for name,matname in mapping.items():
 o=bpy.data.objects[name]
 if o.data.users>1:o.data=o.data.copy()
 o.data.materials.clear();o.data.materials.append(mats[matname])
 if len(o.data.polygons):
  for face in o.data.polygons:face.material_index=0
s=bpy.context.scene
if cfg.get('lighting',False):
 pts=[bpy.data.objects[n].matrix_world@Vector(c) for n in bounds for c in bpy.data.objects[n].bound_box]
 lo=Vector([min(x[i] for x in pts) for i in range(3)]);hi=Vector([max(x[i] for x in pts) for i in range(3)])
 center=(lo+hi)/2;scale=max(hi-lo)/manifest['reference_max_extent']
 if scale<=0:raise RuntimeError('Degenerate model bounds')
 # Retain old lights in file but hide them in this version to avoid double illumination.
 for o in s.objects:
  if o.type=='LIGHT':o.hide_render=True
 col=bpy.data.collections.new('包装同款_摄影灯光');s.collection.children.link(col)
 for o in dst.objects:
  col.objects.link(o);o.location=center+(o.location-Vector(manifest['reference_center']))*scale
  o.data.size*=scale;o.data.size_y*=scale;o.data.energy*=scale*scale
 s.world=dst.worlds[0]
for k,v in manifest['view'].items():setattr(s.view_settings,k,v)
s.render.engine='CYCLES'
dest.parent.mkdir(parents=True,exist_ok=True);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
print('LOOK_APPLIED',str(dest))

