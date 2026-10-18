# Bronze and silver fresh-render candidate QA
Created 2026-10-18, directory timestamp 18:30:38 UTC+08.
Status: both candidates preserve structure and identity reasonably well, but I do NOT recommend accepting either as having met the full new material/foreground-clarity standard. These are review candidates only, not approved final art.

## Execution and provenance
- Exactly one built-in image_gen invocation per requested illustration. No API fallback, no second candidate, no smoothing/denoising/postprocessing of the final art.
- Each invocation actually included two references, in this order: its own latest cleaned source for identity/design/pose/story/composition, then the approved second mythic travel sample for broad-plane anime-mythic materials only.
- The sample's bent pole, story, horse and pose were explicitly excluded in both prompts.
- New source-based complete drawing and lighting rebuild was explicitly requested. The results nevertheless remain strongly tied to the source render; the requested material reset was only partially achieved.
- Both outputs are native 1024 x 1536. No upscaling. A 1190-wide frame layout would still use the 1024-wide illustration at 1:1.
- Exact input paths, roles, dimensions and SHA-256 hashes are in actual-reference-mapping-native-dimensions.json. Full prompts are beside the images.
- No candidate was uploaded or substituted into final framed deliveries.

## Inspection completed
Personally viewed the complete second mythic sample and both current pure illustration sources, both complete output candidates, and all 15 source/candidate paired crops at original pixel scale.
Crops cover face, entire pole from butt through both hands to blade root, blade face/edge, cloth/armor, horse head/muscles/legs, near mud/ground, tree, dragon, gate and blank plaque.
QA comparison artwork is 1 input pixel to 1 displayed crop pixel; only a separate label strip was added. There was no resampling of the crop artwork.

## Bronze: preserved and improved
- Same main face identity/bone planes, mature sharp eyes and long beard. No material new facial drift detected.
- Three brothers remain on ordinary horses, Guan Yu large, Liu Bei/Zhang Fei smaller. Liu green-white, Guan green-black, Zhang black-red with little green.
- Enemy distinction remains: the foreground Yellow Turban flees while looking back.
- Both grips and the entire physical shaft trace a single straight axis, retaining a long shaft and wide blade belly. Blade macro ornament and identity remain.
- Peach branch is substantially sharper; foreground subject and supporting riders remain legible; cloud dragon is subordinate.
- Blade surface/edge is much cleaner than the source, and coarse mud-clod structure is more legible.

## Bronze: blockers under the new standard
- Mud sheets still form a very bright cream-white reflected web with many small bright points, especially around the main lower foreleg/hoof and splash at y ~1000-1300. This is not the requested quiet rough diffuse earth.
- The dark front leg still carries scattered bright point marks.
- A few pale brown specks/smudges remain on the lower blade edge. They must not be excused as intentional mud to pass the new clean-material criterion.
- Closest foreground ground and petals, especially bottom-left and bottom edge at y ~1340-1536, remain strongly defocused. The prompt explicitly asked for clear nearest painted forms.
- Therefore the material rebuild is incomplete even though identity, pose, long weapon and story are retained.

## Silver: preserved and improved
- Face identity, dynamic lunge/twist and fantasy armor silhouettes preserved; no substantial new facial swelling detected.
- Both hands and the continuous shaft trace one straight diagonal axis. No bend like the style sample's known error was introduced.
- Wide magical blade, intentional large gems and green aura remain. Large green dragon and gatehouse composition remain.
- Gate plaque remains entirely blank for independent later text overlay.
- Subject cloth reads matte; gate stones and some middle-foreground rocks are more legible.

## Silver: blockers/limitations under the new standard
- Closest foreground rocks at the lower edge remain strongly defocused, especially x ~0-600, y ~1320-1536. This fails the explicit near-clear requirement.
- Armor still uses many short bright scale-edge highlights, and overall surface rendering remains very close to the source rather than a confidently rebuilt broad-plane material scheme. Purposeful edge highlights are not automatically defects, but this is not strong evidence of the requested full reset.
- Thus the candidate should not be described as fully rebuilt and accepted merely because the face, weapon and composition survived.

## Handoff
The parent and independent reviewer received exact candidate paths, provenance JSON and all comparison crops, plus the blockers above. No additional generation is underway.

