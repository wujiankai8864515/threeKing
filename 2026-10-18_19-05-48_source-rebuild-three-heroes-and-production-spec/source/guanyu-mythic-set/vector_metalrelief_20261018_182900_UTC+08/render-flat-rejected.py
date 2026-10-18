import bpy, math, os, json
from mathutils import Vector
from pathlib import Path
D=Path(__file__).parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=1,rough=.23):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
gold=mat('satin gold face',(.62,.32,.065),.82,.22);edge=mat('polished gold chamfers',(.88,.53,.16),.90,.16);dark=mat('recessed bronze gold',(.23,.12,.032),1,.32);green=mat('deep jade enamel',(.025,.11,.047),.4,.27);purple=mat('oxblood enamel',(.095,.016,.035),.35,.26);black=mat('blue black enamel',(.01,.02,.025),.3,.28)
# Fine, directional machined surface, procedural and deterministic.
n=gold.node_tree.nodes;l=gold.node_tree.links;t=n.new('ShaderNodeTexCoord');w=n.new('ShaderNodeTexWave');w.wave_type='BANDS';w.bands_direction='X';w.inputs['Scale'].default_value=420;w.inputs['Distortion'].default_value=0;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.08;b.inputs['Distance'].default_value=.00035;l.new(t.outputs['Generated'],w.inputs['Vector']);l.new(w.outputs['Color'],b.inputs['Height']);l.new(b.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
def xy(p,z=0):return ((p[0]-512)*.01,(768-p[1])*.01,z)
def curve(name,loops,z=.04,thick=.02,bevel=.008,material=gold):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='2D';cu.resolution_u=2;cu.fill_mode='BOTH';cu.extrude=thick;cu.bevel_depth=bevel*2.4;cu.bevel_resolution=5
 for pts in loops:
  sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for p,v in zip(sp.points,pts):p.co=(*xy(v,0),1)
  sp.use_cyclic_u=True
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.location.z=z;ob.data.materials.append(material);return ob
def ring(name,cx,cy,r,ri,z=.08,material=gold,bevel=.008):
 pts=[(cx+r*math.cos(t*2*math.pi/192),cy+r*math.sin(t*2*math.pi/192)) for t in range(192)];loops=[pts]
 if ri:loops.append([(cx+ri*math.cos(t*2*math.pi/192),cy+ri*math.sin(t*2*math.pi/192)) for t in reversed(range(192))])
 return curve(name,loops,z,.018,bevel,material)
def wire(name,pts,z=.07,r=.004,material=edge,close=False):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*xy(v,z),1)
 sp.use_cyclic_u=close;ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(material)
outer=[(71,43),(961,43),(970,52),(970,1500),(960,1510),(72,1510),(62,1500),(62,53)]
inner=[(110,126),(875,126),(875,600),(950,676),(950,1425),(160,1425),(160,945),(80,850),(80,425),(110,385)]
curve('main structural frame',[outer,list(reversed(inner))],.025,.025,.012,gold)
wire('outer polished narrow crest',[(72,48),(958,48),(965,55),(965,1497),(957,1504),(75,1504),(68,1497),(68,56)],.098,.009,edge,True)
wire('inner recessed line',inner,.085,.012,dark,True);wire('inner bevel lip',inner,.101,.007,edge,True)
# Header sunken panel with raised fine rim.
head=[(427,64),(862,64),(862,115),(377,115)]
curve('header recess',[head],.086,.004,.002,dark);wire('header rim',head,.099,.004,edge,True)
# Small architectural engraving, narrow lines rather than printed wallpaper.
for xx in [260,330]:
 wire('header diamond groove',[(xx,55),(xx+31,76),(xx,97),(xx-31,76)],.081,.004,dark,True)
 wire('header diamond rim',[(xx,62),(xx+20,76),(xx,90),(xx-20,76)],.083,.003,edge,True)
for xx in [596,668,740]:wire('lower lozenge',[(xx,1440),(xx+30,1459),(xx,1478),(xx-30,1459)],.083,.004,edge,True)
# Turned metal sockets, true stepped recesses and bevels.
for name,cx,cy,r in [('country',151,130,88),('rank',151,1387,94),('troop',897,1418,79)]:
 ring(name+' outer shoulder',cx,cy,r,r-10,.07,gold,.012)
 ring(name+' outer mirror bevel',cx,cy,r-3,r-5,.105,edge,.004)
 ring(name+' recessed separator',cx,cy,r-12,r-17,.064,dark,.003)
 ring(name+' inset terrace',cx,cy,r-18,r-29,.085,gold,.008)
 ring(name+' inner lip',cx,cy,r-30,r-33,.105,edge,.004)
 ring(name+' enamel',cx,cy,r-35,0,.055,{'country':green,'rank':purple,'troop':black}[name],.003)
# Thin flat scroll bands with precise bevels, replacing round tube ornament.
def bez(p0,p1,p2,p3,N=24):
 return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]) for t in [i/N for i in range(N+1)]]
def band(name,pts,width=12,z=.11):
 width=width*.95*.01;hh=.032
 profile=bpy.data.curves.new(name+' bevel section','CURVE');profile.dimensions='2D';profile.resolution_u=1
 vv=[(-width/2+.006,-hh/2),(width/2-.006,-hh/2),(width/2,-hh/2+.005),(width/2,hh/2-.005),(width/2-.006,hh/2),(-width/2+.006,hh/2),(-width/2,hh/2-.005),(-width/2,-hh/2+.005)]
 sp=profile.splines.new('POLY');sp.points.add(len(vv)-1)
 for p,v in zip(sp.points,vv):p.co=(v[0],v[1],0,1)
 sp.use_cyclic_u=True;po=bpy.data.objects.new(name+' hidden profile',profile);bpy.context.collection.objects.link(po);po.hide_render=True;po.hide_viewport=True
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.twist_mode='Z_UP';cu.bevel_mode='OBJECT';cu.bevel_object=po;cu.use_fill_caps=True
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*xy(v,z),1)
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(gold)
pts=[(34,222),(76,222)]+bez((76,222),(102,224),(104,197),(88,197))[1:]+bez((88,197),(73,197),(77,211),(87,207))[1:];band('left cloud return',pts,12)
pts=[(99,190),(202,190)]+bez((202,190),(226,190),(222,213),(207,212))[1:];band('upper cloud ledge',pts,13)
pts=[(139,227),(245,227)]+bez((245,227),(270,227),(271,198),(257,199))[1:]+bez((257,199),(247,200),(249,211),(255,208))[1:];band('right cloud scroll',pts,12)
pts=bez((145,227),(117,226),(119,255),(136,253))+bez((136,253),(149,252),(146,240),(139,243))[1:];band('lower cloud curl',pts,11)
for cx,sgn in [(222,1),(815,-1)]:
 pts=[(cx,1408),(cx+sgn*61,1408)]+[(cx+sgn*x,y) for x,y in bez((61,1408),(85,1408),(84,1382),(72,1383))[1:]];band('lower scroll shoulder',pts,11,.12)
# Diamond stepped plan with individually beveled planes.
def diamond(r):return [(913,124-r),(913+r,124),(913,124+r),(913-r,124)]
curve('level outer tier',[diamond(105),diamond(89)[::-1]],.10,.018,.01,gold)
curve('level dark incision',[diamond(87),diamond(82)[::-1]],.075,.008,.003,dark)
curve('level inner bevel',[diamond(80),diamond(67)[::-1]],.12,.014,.007,edge)
curve('level central plane',[diamond(65)],.08,.01,.005,gold)
# Faceted relief five-point stars; no flat icon fill.
for k in range(4):
 cx,cy=911,280+k*85;pts=[]
 for j in range(10):
  a=-math.pi/2+j*math.pi/5;r=31 if j%2==0 else 13.5;pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
 verts=[xy((cx,cy),.25)]+[xy(p,.12 if j%2==0 else .11) for j,p in enumerate(pts)];faces=[(0,j+1,(j+1)%10+1) for j in range(10)];mesh=bpy.data.meshes.new('cut star');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new('five point cut star',mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(edge)
# Straight passive extensions; shared physically lit material, no hooks or triangles.
for i in range(3):
 y=1018+i*91;pts=[(950,y),(685,y)]+[(685+20*math.cos(a),y+20+20*math.sin(a)) for a in [math.pi*1.5-t*math.pi/2/12 for t in range(13)]]+[(665,y+56)]+[(685+20*math.cos(a),y+56+20*math.sin(a)) for a in [math.pi-t*math.pi/2/12 for t in range(13)]]+[(950,y+76)]
 curve('passive same-frame extension',[pts],.035,.024,.012,gold)
 wire('passive fine lower lip',[(x,yy) for x,yy in pts],.099,.005,edge)
 # A thin incised inner rule, fully straight at the frame connection.
 wire('passive top incision',[(683,y+7),(947,y+7)],.089,.003,dark)
 wire('passive bottom incision',[(683,y+69),(947,y+69)],.089,.003,dark)
# Existing outer rail is uninterrupted at the joined panel.
wire('unbroken right rail',[(956,695),(956,1330)],.105,.008,edge)
# Recess-like fine inlay geometry on broad faces, with no stochastic grit.
for cy in range(980,1280,32):
 wire('left etched diamond',[(113,cy-12),(126,cy),(113,cy+12),(100,cy)],.080,.0024,dark,True)
 wire('left inset diamond',[(113,cy-7),(121,cy),(113,cy+7),(105,cy)],.081,.0016,edge,True)
for cy in range(210,595,34):
 wire('right etched diamond',[(911,cy-13),(929,cy),(911,cy+13),(893,cy)],.080,.0021,dark,True)
for i in range(3):
 yy=1018+i*91+38
 for xx in range(696,944,31):
  wire('passive engraved lattice',[(xx,yy-25),(xx+15,yy),(xx,yy+25),(xx-15,yy)],.089,.0019,dark,True)

# Lighting: broad key plus a narrow reflection strip; no sparkles/no random noise.
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.38,.42,.48,1);world.node_tree.nodes['Background'].inputs[1].default_value=.55
for name,loc,power,size,sy in [('large softbox',(-4,7,9),450,3,7),('strip reflection',(7,-3,7),600,1,8),('soft front',(0,0,8),950,10,14)]:
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.name=name;ob.data.energy=power;ob.data.shape='RECTANGLE';ob.data.size=size;ob.data.size_y=sy;ob.rotation_euler=(Vector((0,0,0))-ob.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,0,20));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=15.36;cam.rotation_euler=(0,0,0);bpy.context.scene.camera=cam
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=1024;scene.cycles.adaptive_threshold=.008;scene.cycles.use_denoising=False;scene.render.resolution_x=2048;scene.render.resolution_y=3072;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.view_settings.view_transform='AgX';scene.view_settings.exposure=0;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.filepath=str(D/'gold-metal-native-2048.png');scene.render.threads_mode='FIXED';scene.render.threads=8
bpy.ops.wm.save_as_mainfile(filepath=str(D/'gold-frame-native.blend'));bpy.ops.render.render(write_still=True)
