import bpy,sys,argparse,json,hashlib,array
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--out',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);s=bpy.context.scene;rows=[]
for o in s.objects:
 r={'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'matrix_world':[list(x) for x in o.matrix_world],'hidden':o.hide_render,'materials':[m.name if m else None for m in getattr(o.data,'materials',[])]}
 if o.type=='MESH':
  v=array.array('f',[0])*(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',v)
  inds=array.array('i',[0])*len(o.data.loops);o.data.loops.foreach_get('vertex_index',inds)
  pts=[o.matrix_world@Vector(x) for x in o.bound_box]
  r.update(vertices=len(o.data.vertices),polygons=len(o.data.polygons),geometry_sha256=hashlib.sha256(v.tobytes()+inds.tobytes()).hexdigest(),uv=[x.name for x in o.data.uv_layers],bounds=[[min(x[i] for x in pts) for i in range(3)],[max(x[i] for x in pts) for i in range(3)]])
 rows.append(r)
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'source':bpy.data.filepath,'frame':s.frame_current,'units':s.unit_settings.system,'scale_length':s.unit_settings.scale_length,'range':[s.frame_start,s.frame_end],'fps':s.render.fps/s.render.fps_base,'objects':rows,'images':[{'name':i.name,'packed':bool(i.packed_file),'path':bpy.path.abspath(i.filepath)} for i in bpy.data.images if i.type!='RENDER_RESULT']},ensure_ascii=False,indent=2),encoding='utf8')
print('INSPECTED',len(rows))
