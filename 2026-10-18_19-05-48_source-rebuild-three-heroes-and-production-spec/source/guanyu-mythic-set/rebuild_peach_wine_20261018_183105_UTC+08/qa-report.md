# Source-regeneration QA

Exactly one built-in image_gen candidate was made per scene. Both actual rasters are 1536×1024. Neither is an upscale. No images were uploaded.

The latest specification and second mythic validation prompt were read. The mythic escort validation image was actually viewed as broad form/material direction, but not supplied as an image input, avoiding transfer of its bent weapon axis and irrelevant story. Each actual image input was its own latest material-cleanup v10, explicitly limited to identity, design and macro-story layout. Full exact prompts are in prompts-and-source-roles.md.

Both source full images, both candidate full images, and all 13 unscaled comparison crops in qa-100pct were actually opened with view_image. Comparison strips preserve original pixels and add only labels/canvas; the script does not edit the artworks.

## Peach garden v11: independent QA passed with minor style risk pending root decision
- Recognizable Liu Bei, Guan Yu and Zhang Fei retained, all three clear, six bowl-holding hands readable without a newly observed gross anatomical defect.
- Liu green-white, Guan green-black, Zhang black-red remain. No heart ornament or palace introduced.
- Root and altar/stone geometry and lighting visibly rebuilt rather than merely smoothed. Foreground is clearly delineated; distant woodland softens atmospherically.
- Matte cloth and matte bark/stone largely use grouped continuous values; vessel/armor metal retains intentional broad edge/relief light.
- No global blur wash, uniformly tiled weave or overall plastic smoothing observed.
- Small warm moss/edge marks on tree/ground still require the independent review to distinguish designed natural forms from disallowed residual sparkle; not automatically excused as dirt.

## Warm wine v11: worker and independent QA REJECTED
Useful changes:
- Weapon blade is now low and downward, outside horse legs rather than raised skyward; lowered weapon arm and ordinary dark horse identities remain.
- Guan's face, rein hand, Liu/Zhang/Cao identities and colors, camp, army and green dragon remain recognizable.

Blocking concerns:
- No visible tail shaft beyond the weapon gripping hand; the required complete long pole and physically readable balance are not demonstrated.
- Visible shaft is short relative to the very large blade. The blade occupies the forward outer foreground, not a clearly readable backward trailing direction.
- Nearest rocks retain localized defocus and granular bright rendering inherited from the source; this fails the requirement that the new illustration rebuild foreground materials as sharp clean forms.
- Large areas remain near the previous source rendering rather than visibly restructured material/light language. This is not passed merely because the blade was moved.

No retry or extra candidate was made because this assignment permits exactly one candidate per image.

## Provenance
manifest.json records real inputs, source and candidate SHA-256 hashes, native dimensions, one-call counts and each diagnostic crop path.

## Later color update, received after generation
Lead relayed updated direction: Liu Bei should be chiefly white or a suitable personal main color with little green; Zhang Fei black-red with little green; Shu green mainly appears as small badge/identity accents. Guan Yu keeps green robes without tinting the entire person/background green. Lead stated current peach garden does not need regeneration solely for this color update. This note does not rewrite the actual prompts or falsely claim those prompts contained the later instruction. Warm wine remains pending root disposition of its failed requirements.

Independent reviewer confirmed peach garden identities, six hands, colors and depth. Sparse warm bark marks mostly follow bark fragment edges/moss, not random cross-material gold dust; reviewer recommends passing with that residual sparse-edge-light style risk for root decision. Warm-wine v11 independently rejected for missing tail, short shaft/giant blade proportion, forward blade placement and near-rock defocus.
