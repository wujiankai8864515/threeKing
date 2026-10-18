# Liu Bei black-iron v1 identity sample QA

One built-in image_gen candidate. Actual output 1024×1536. Pure portrait artwork, no UI. No upscale and no upload. Four-card/three-biography brief completed separately.

The actual source full image was viewed before generation. It is the already delivered peach-garden v10, using ONLY the left Liu Bei face. San Guo Sha and the later unverified peach v11 were not inputs. Candidate full image and all nine native-pixel QA crops/comparisons were actually viewed with view_image.

## Useful result
- Mature Liu Bei facial family is recognizable: shaped mustache/short chin beard, hairline/topknot, brows/nose and intelligent gaze. He is not mistaken for central long-bearded Guan Yu or shaggy Zhang Fei.
- Sturdy shoulders/forearms, capable working posture and responsible demeanor; not a weak scholar.
- Clearly shown craft: two hands manipulate straw at a recognizable unfinished sandal; finished pair, hanging mats, rolled mat, stool and bundles support the story.
- Hand counts, thumb opposition, wrist/forearm attachment and the sandal-holding relationship have no obvious gross new defect in the inspected crops.
- White/rice-beige work robe with small muted green ornament, plain hairstyle and earth sash; no high-tier armor, crown, UI or early golden divinity.
- Independent town-doorway/stool composition distinct from a bean stall or wine/butcher shop.

## Concerns: worker and independent QA do not pass this as the series style anchor
- The drawing is more finely rendered/semi-realistic than the requested clean 2D mythic grouped-plane style. Facial shading and cloth surface detail are especially realistic compared with the identity source.
- Yellow dragon is pale but too large and explicitly visible for a barely perceptible distant low-tier dormant silhouette. Its stern spiky morphology also needs judgement against the requested independently designed benevolent yellow dragon.
- Dense crosshatched/worn microtexture appears on cloth; this is not the requested simple broad matte plane language.
- Straw/mats are structurally readable and mostly matte, but wooden stool contains some small warm marks. They must not be excused automatically as wear if the material standard rejects their dot-like appearance.
- Extreme bottom foreground ground and some nearest reed tips show photographic-looking softness. Face, hands, sandals and mat remain clear.

Independent reviewer /root/audit_image_quality_causes confirmed: weaving action and two hands have no obvious hard defect; mature gentle identity direction is valid. Failure is style/tier: realistic skin, dense hemp-cloth texture and wood/stone detailing deviate from the clean 2D language, and the dragon is too large and explicit. Normal straw fibers are not themselves treated as gold dust. Do not expand the remaining six images using this as the style anchor. No second candidate generated without new authorization.

## Deliverables
- 刘备-黑铁-v1-织席编履身份候选.png
- 刘备-四卡三传记制作brief.md
- prompt-and-reference.md: exact prompt and actual image role
- manifest.json: input/candidate hashes, native size and crop mapping
- qa-100pct/: nine actually inspected native comparisons/crops
