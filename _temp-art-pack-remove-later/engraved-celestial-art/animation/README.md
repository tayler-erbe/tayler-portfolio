# Beneath the Starry Veil

**Current best starting point: the clean-layer rebuild.** Every element is its own cut-out piece stacked back to front; nothing from the approved portrait sits underneath. The plan, with every layer alone and stacked, is [plan/opening-scene-layer-plan.pdf](plan/opening-scene-layer-plan.pdf). Start in [current/](current/).

| File | Use |
| --- | --- |
| [celestial-opening.html](current/celestial-opening.html) | Standalone 1.9 MB browser prototype with its WebP assets embedded |
| [celestial-motion.gif](current/celestial-motion.gif) | Looping 12-second preview of the same artwork |
| [approved-portrait.webp](current/approved-portrait.webp) | Approved composition reference for scale and placement |
| [animation-still.webp](current/animation-still.webp) | The layered render at its resting pose |

## Composition and motion

- Use the framed portrait at full width on a phone, uncropped and undistorted. Leave the controls below the frame. The large diagonal navy star dome should dominate.
- Keep the traveler anchored. Gather the fold at his hand with a restrained reveal. Preserve the selected portrait's pose, tree, rayed sun, village and foreground. The main wheel is substantial and partly hidden by the left frame. Its companion gear should read clearly beside it.
- Behind the veil, give broader, near-ivory cloud banks priority over the planets. Alternate banks with engraved strips and tuck small planets between them. Place some clouds in front of other clouds and a few in front of the planets and rainbow. The attached [cloud-sheet reference](studies/02-portrait/cloud-sheet-reference.jpeg) shows the overlap and diagonal layering.
- Move the individual cutouts at nine poses per second. Far cloud and pattern plates drift a few pixels. Nearer sheets drift slightly farther, with different timing and opposite directions. Keep all of that motion inside the reveal.
- Turn the wheel, crescent and companion gear on independent pivots. Rotate the sun's corona around the face and step the face through its eye cels (side to side, then closing). Give the stars and planets separate rotational timings. Pivot small branch tips and blades of grass while keeping their roots fixed.

## Iterations

| Study | What we learned |
| --- | --- |
| [01 · Landscape proof](studies/01-landscape/) | Established the diagonal star dome, decorated border and right-side landscape in the engraving's original proportions. |
| [02 · Portrait proofs](studies/02-portrait/) | Recomposed the portrait for a vertical phone. We tried a profile peeking out from the lifted fold. The user preferred the original turned-away traveler and supplied the selected portrait. |
| [03 · Flattened motion](studies/03-flattened-motion/) | Tried local shader movement on a single portrait and added MP4 and GIF previews after playback problems. The warped-paper effect missed the intended mechanical movement of separate cutouts. |
| [04 · First paper cutouts](studies/04-first-paper-cutouts/) | Tested rigid sprite turns, cloud-bank offsets, mesh-like clockwork, branch pivots and an alternate face cel. The layering worked structurally. The new placement exposed too much of the veil and gave the gears too little visual weight. |
| [05 · Approved layout with layered reveal](studies/05-layered-portrait/) | Returned to the preferred portrait, increased the visual weight of the clockwork and interleaved moving sheets. The stepped mechanical motion was close. The cloud banks still read too small, the planets too large, and the pale highlights too muted relative to the original engraving. |
| [06 · Broader cloud banks](studies/06-broader-cloud-banks/) | Kept the approved layout and stepped cutout motion. Rebuilt the reveal with larger, near-ivory cloud banks and planets roughly one-third smaller. Compared with the approved portrait, the banks still read as many small scalloped puffs, and the turning sun rays and their backing came out grey beside the portrait's warm gold. |
| [07 · Drawn cloud banks](studies/07-drawn-cloud-banks/) | Replaced the stacked puffs with five long cloud banks drawn for this reveal (`cloud_banks/`: ivory crowns, slate engraved shadows, a hanging skirt of streaks). Order below the clockwork is bank, ribbon, bank, ribbon and zigzag, bank, ribbon, bank, bank; three small planets sit between sheets. The sun's backing is now taken from the approved portrait and the rays are graded to its gold-cream. Motion is unchanged: nine poses a second, the same pivots and timings. |
| [08 · Pasted over the portrait](studies/08-pasted-over-portrait/) | Same composition. The crescent moon is now its own piece (cut from the portrait, sky patched beneath) and rocks and drifts. Stars turn about three times faster and every third one rocks in place. Cloud banks and ribbons travel about twice as far on shorter cycles. Four more leaf clumps lifted from the portrait rock on the tree, and the two existing boughs and the grass swing wider. The sun's face is now six drawn eye cels (`sun_eye_cels/`): the eyes travel slowly left, back to centre, right, back to centre, then the lids lower, close for about two seconds and reopen; the cycle is about 12 seconds. There is no in-between cel for a slight look to the right, so that turn is one step. Still nine poses a second. Latest pass: the crescent now lifts whole (an earlier cut took only half of it); a third of the stars spin, a third swell and shrink by about a fifth, a third rock; the wheel, crescent, hub and both gears are about 12% larger and still mesh; two clouds inside the dome (over the sun, left of the tree) are lifted from the portrait and rock a little on a pin, with the sky beneath filled from the nearest colours. The cloud to the right of the tree still belongs to the plate and does not move. | Review: because the approved portrait was the bottom layer, the old sun rays, moon and stars showed behind the moving pieces, and the moon cut showed a gap in some poses. |
| [Current · Clean layers](current/) | Rebuilt from 157 separate cut-out pieces in 19 layers, back to front: sky (drawn from the approved portrait, bent so its rolled edge follows the approved curve), behind-the-veil backdrop, far sheets, clockwork, banks/ribbons/planets, stars (drawn from the portrait, one piece each), moon, sun (rays + eye cels), clouds inside the sky (eight pieces along one arc from low on the left, behind the tree and up over the sun, mirroring the veil's curve and separating night from day), hills and village, fields, tree trunk, leaf clumps, grass, flowers (still stems, turning heads), rocks, traveler, paper grain, frame. Every cut piece casts a small soft shadow onto the layer behind it. Built by `source/layered.py` and `source/layered-output.py`. |

The earlier HTML and GIF variants were rebuilt from retained sources and preview media for this archive. Their original Library versions were unavailable for an exact byte comparison. The current HTML and GIF are the more-movement revision, built together from `source/` in one run. Earlier passes are preserved in Studies 05 to 07.

Known differences from the approved portrait in the current still: the reveal is brighter and busier than the portrait's quieter grey-blue banks; the ringed planet near the upper gear is very small; the rays are a separate plate, so their exact shapes differ from the portrait's.

## Preview and integration

Open the current HTML in a browser and select **Preview motion**. The GIF plays as a separate preview. Some iPhone file-preview viewers showed a static frame during review. Device-specific performance and playback are unverified.

For app integration, call `window.celestialOpening.bindLoading(startupPromise)` with the app's actual initialization promise. The animation runs while loading and returns to the finished still when readiness is signaled. There is no minimum wait. A ready-state button click dispatches `celestial:continue` on `window`. Either the system preference or the on-screen **Reduce motion** setting keeps the art still.

## Rebuild the current files

From this directory, run:

```sh
python3 -m pip install Pillow numpy scipy
python3 source/layered-output.py html gif
```

FFmpeg is required to encode the GIF. Outputs go to `animation/build/layered/`. `python3 source/layered.py` writes each layer alone and stacked to `build/layer-plan/`, and `python3 source/plan_pdf.py plan/opening-scene-layer-plan.pdf` rebuilds the plan. The build uses the art-pack PNGs (including `cloud_banks/`), the approved portrait and the source templates. The HTML is self-contained once built.
