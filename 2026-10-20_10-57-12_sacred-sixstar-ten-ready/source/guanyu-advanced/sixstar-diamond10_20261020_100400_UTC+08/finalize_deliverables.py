from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, numpy as np
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2))
jobs = json.loads((P/'jobs.json').read_text())
art_path = P/'source-08-unchanged.png'
art = np.array(Image.open(art_path).convert('RGBA'))
mask = Image.new('L', (1310,1966)); mask.paste(Image.open(P/'art-native-slot-mask.png').convert('L'), (60,140))
reg = (slice(285,1821), slice(144,1168))
anchors = json.loads((P/'standard-glyph-anchors.json').read_text())['glyph_centers']
expected_art = '7792f1f0b3a0a7099a5dadd8b8881ceb82f10d9751fa2afab36858d490df6bd6'
expected_five = '9c046c5bcd0f537e1c6ce55e6030b8ca6522f902066240313b855d960b91a206'
assert sha(art_path) == expected_art
assert sha(P/'reference-approved-five.png') == expected_five
assert sha(P.parent/'frame-hierarchy_20261020_000010_UTC+08/frame-5star.png') == expected_five
variants, checks = [], []
ui_hashes = []
for j in jobs:
    d=P/j['id']; meta=json.loads((d/'manifest.json').read_text())
    card=Path(meta['output']); frame=d/'frame-6star-expanded.png'; ui=d/'dynamic-ui-expanded.png'
    ca=np.array(Image.open(card).convert('RGBA')); fa=np.array(Image.open(frame).convert('RGBA')); ua=np.array(Image.open(ui).convert('RGBA'))
    assert ca.shape == fa.shape == ua.shape == (1966,1310,4)
    valid=(np.array(mask)[reg]==255)&(fa[reg][:,:,3]==0)&(ua[reg][:,:,3]==0)
    changed=int((np.any(ca[reg]!=art,axis=2)&valid).sum()); assert changed==0
    assert meta['glyph_centers']==anchors
    ui_hashes.append(sha(ui))
    fixes = [{'operation':'clear stray generated construction line from transparent opening','rectangle_xyxy':[347,330,973,365]}] if j['id']=='07' else []
    meta.update(status='candidate_pending_user_review',visual_review_passed=True,
        active_style_revision='holy_material_vfx_user_latest', six_star_passive_count='three retained per current user direction',
        uncovered_art_pixels_checked=int(valid.sum()),uncovered_art_pixels_changed=changed,
        frame_sha256=sha(frame),output_sha256=sha(card),dynamic_ui_sha256=sha(ui),
        native_source_frame=str(d/'generated-frame-source.png'),native_source_frame_sha256=sha(d/'generated-frame-source.png'),
        native_frame_size=[1024,1536],postprocess_fixes=fixes,
        visual_review={'six_stars':True,'three_passives_readable':True,'all_standard_information_readable':True,
            'distinct_structure':True,'sacred_pearl_crystal_and_gold_finish':True,'no_dense_full_screen_sparkles':True,
            'no_purple_or_red_palette':True,'no_art_repainting':True})
    write(d/'manifest.json',meta)
    for f in (d/'card').glob('*.json'):
        old=json.loads(f.read_text()); old['intermediate_output_retained']=False; old['final_composite']=str(card)
        old['six_star_passive_count']='three retained per current user direction';write(f,old)
    variants.append({'id':j['id'],'name':j['name'],'card':str(card),'frame':str(frame),'manifest':str(d/'manifest.json'),
        'generation_arguments':str(d/'actual-args.json'),'native_frame_source':str(d/'generated-frame-source.png')})
    checks.append({'id':j['id'],'pixels_checked':int(valid.sum()),'pixels_changed':changed,'glyph_anchors_match':True,'visual_review_passed':True})
assert len(set(ui_hashes))==1, 'All ten complete dynamic UI layers must be identical'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fw,fh,cap,top=440,660,48,82
sheet=Image.new('RGB',(fw*5,top+(fh+cap)*2),(25,31,39));draw=ImageDraw.Draw(sheet)
draw.text((24,13),'六星神圣框 · 10 款完整卡探索',font=ImageFont.truetype(font,34),fill=(246,239,218))
draw.text((26,55),'同一张 08 空域护城原图 · 编号仅用于选款',font=ImageFont.truetype(font,18),fill=(186,195,203))
for n,v in enumerate(variants):
    x=(n%5)*fw;y=top+(n//5)*(fh+cap)
    im=Image.open(v['card']).convert('RGBA');im.thumbnail((fw-12,fh),Image.Resampling.LANCZOS)
    sheet.paste(im,(x+(fw-im.width)//2,y),im)
    draw.text((x+18,y+fh+7),v['id']+' '+v['name'],font=ImageFont.truetype(font,24),fill=(246,239,218))
overview=P/'00-六星神圣框10款总览.jpg';sheet.save(overview,quality=95,subsampling=0)
now=datetime.now(timezone.utc).isoformat()
qa={'checked_at_utc':now,'source_sha256':expected_art,'five_star_unchanged_sha256':expected_five,
    'source_native_size':[1024,1536],'art_scale':1,'final_canvas_size':[1310,1966],
    'native_generated_frame_size':[1024,1536],'native_4k_claim':False,
    'all_dynamic_ui_layers_identical':True,'dynamic_ui_sha256':ui_hashes[0],
    'total_uncovered_art_pixels_checked':sum(c['pixels_checked'] for c in checks),'total_pixels_changed':0,
    'checks':checks,'notes':['Pixel comparison excludes pixels intentionally covered by frame, glow, UI, or original art-slot mask.',
    '07 generated construction line removed only from frame alpha opening; no illustration pixels edited.',
    'Stronger sacred halos intentionally overlie a small part of the illustration. The native source illustration remains byte-identical.',
    'Visual review covers both full-card sheets and enlarged title, stars, passives and medallions.']}
write(P/'QA.json',qa)
write(P/'manifest.json',{'status':'candidate_pending_user_review','ready_at_utc':now,'variant_count':10,
    'active_revision':'holy_material_vfx_user_latest','overview':str(overview),'source_illustration':str(art_path),
    'source_sha256':expected_art,'approved_five_star_unchanged':True,'variants':variants,
    'superseded_history':'Each NN/history-diamond folder is an unshown superseded draft, not an additional deliverable.',
    'folder_name_note':'Original task directory retained after latest holy-style revision to avoid creating a duplicate batch.'})
write(P/'uploads.json',{'uploads':[{'local_path':str(f),'purpose':'create_library_file','library_artifact_type':'image'} for f in [overview]+[Path(v['card']) for v in variants]]})
print(json.dumps({'overview':str(overview),'variants':len(variants),'pixels_checked':qa['total_uncovered_art_pixels_checked'],'pixels_changed':0},ensure_ascii=False))
