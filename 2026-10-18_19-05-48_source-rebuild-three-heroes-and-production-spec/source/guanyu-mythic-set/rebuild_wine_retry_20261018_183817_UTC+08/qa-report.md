# Warm-wine v12 fresh-composition retry QA

One authorized built-in image_gen call, using latest v11 as identity/story/design input but explicitly excluding failed weapon/ground rendering. Actual output is 1536×1024, not an upscale. Peach garden unchanged. No images uploaded.

Source full image, candidate full image and all 10 native-pixel diagnostic crops/comparisons in qa-100pct were actually opened with view_image; all crops were inspected at original pixel detail. Diagnostic scripts crop and label only; illustration was changed only by image_gen.

## Improvements
- New composition shifts hero/horse right and opens a visible outer side lane.
- Blade is now higher in image than the front hoof and farther back in the outer lane, much closer to a trailing carry than v11's nearest-foreground blade.
- Both sides of the grip now have a substantial visible shaft span. Main visible shaft is straight through the hand and blade collar.
- Weapon does not visibly cross horse legs. Shoulder, elbow and wrist chain is readable; rein hand remains separate and recognizable.
- Mature face, impressive fantasy armor, normal dark horse anatomy, supporting Liu/Zhang/Cao and camp/green-dragon story are retained.
- Foreground ground is substantially recomposed into larger rock and earth planes with fewer visually granular highlights.

## Unresolved concerns: not an unconditional pass
- The upper tail shaft eventually disappears into/behind the waist belt/costume; no clearly visible final capped pommel. Thus the required complete visible two-sided pole is still not demonstrated, and the waist contact/occlusion needs independent judgement.
- Several closest lower-left rocks/grass remain softened/out of focus; the demand for crisp nearest foreground forms is not completely fulfilled.
- Liu Bei is primarily white, but a broad green central panel remains; green has not been reduced solely to small insignia accents.
- Dragon now exposes substantial scale-patterned body area; primary head and green identity remain, but cloud-hidden-body preference may warrant root judgement.

Independent review requested from /root/audit_image_quality_causes; not yet received. No further generation was started.

Exact prompt and role/exclusion record: prompt-and-source.md
Source/candidate hashes and native dimensions: manifest.json
