# Local fidelity plan — pending explicit permission

No image generation, compositing, or image mutation has been performed for this plan. Source identity is locked by locked-sources.json; originals are read-only by workflow and must never be overwritten.

## Frozen assets
Bronze card, biography one (rally), biography two (Hulao) remain byte-for-byte unchanged. Hulao may be read as the approved weapon-effect reference only. Silver and gold illustrations are accepted bases with only the requested weapon effect eligible to change. Biography three has only its terminal spear tip eligible to change. Blackiron has only a small hero-placement adjustment eligible to change.

## Four bounded edits
1. Silver: isolate the visible blade tip at lower left. Generate a restrained directional red-white light accent matching Hulao at substantially lower intensity; composite only the effect onto the locked original after approval. Do not regenerate blade metal, shaft, hands, face, armor, tiger, scenery, or UI. Initial inspection envelope approximately x=20..450,y=780..1250, but the actual permitted alpha must be a narrow contour around the terminal blade, not the whole rectangle.
2. Gold: add the same restrained energy only along the right-side spear blade, approximately x=720..1024,y=650..880. Preserve blade and shaft pixels wherever the effect alpha is zero; avoid tiger/face/hand coverage. Use a small number of continuous directional streaks, not particles or gold dust. No whole-frame generated output may become the new source.
3. Biography three: straighten only the terminal point of the wavy spear blade at right, approximately x=1340..1490,y=480..565. Keep serpentine blade body, collar, shaft, hands, orientation, effects, tiger and refugees unchanged. Use the smallest shape-following alpha mask covering the old terminal curve and replacement straight point; masked local background reconstruction only where old tip vacates space. Exact bounds to be visually confirmed before generation.
4. Blackiron: a small horizontal hero translation, tentatively 24–40 px right at native resolution, with no scaling, rotation or resampling of hero pixels. Face and full hero must be copied from locked original, never regenerated. Sky and tiger outside the silhouette boundary stay pixel-identical. This is NOT literally a small local patch: the hero silhouette and vacated boundary span much of image height, and the pillar grip is an attachment constraint. Before acting, confirm whether user accepts a masked cutout translation plus local background repair; do not silently claim a tiny ROI can move the entire hero. Prefer the smallest displacement that improves framing and preserves grip.

## Permission and execution gate
Await root's explicit relay of user authorization for local generation plus masked compositing. Do not start generation based on this plan alone. Builtin image_gen has no explicit mask argument, so generation is proposal material only; final image must derive from the locked original plus an explicitly authorized local alpha layer. No full-frame repaint accepted. If permitted masking cannot preserve a constraint, stop and explain instead of broadening scope.

## Required QA
- Save each attempted patch and alpha mask separately in a new timestamp directory.
- Save exact prompt, source hash, changed-pixel bounding box, per-image changed count, and mask hash.
- Assert every pixel outside authorized alpha support is exactly equal to locked source; changed count outside mask must be zero.
- Check faces/armor/tigers/shaft as separate invariant regions, except blackiron hero translation where pixel correspondence is checked by inverse integer offset.
- Inspect 100% crop and full-frame; no halos, clipped effects, softened details, gold specks or unexpected scene changes.
- Recompose existing UI only after native illustration passes; preserve identical UI fields and native 1:1 art placement.
- Do not overwrite sources or claim user acceptance of new edits before review.
