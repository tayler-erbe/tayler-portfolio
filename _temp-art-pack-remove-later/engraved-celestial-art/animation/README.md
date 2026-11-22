# Beneath the Starry Veil

**Current best starting point: the cloud revision on the approved clockwork portrait.** Start in [current/](current/).

| File | Use |
| --- | --- |
| [celestial-opening.html](current/celestial-opening.html) | Standalone 1.31 MB browser prototype with its WebP assets embedded |
| [celestial-motion.gif](current/celestial-motion.gif) | Looping 12-second preview of the same artwork |
| [approved-portrait.webp](current/approved-portrait.webp) | Approved composition reference for scale and placement |
| [animation-still.webp](current/animation-still.webp) | The layered render at its resting pose |

## Composition and motion

- Use the framed portrait at full width on a phone, uncropped and undistorted. Leave the controls below the frame. The large diagonal navy star dome should dominate.
- Keep the traveler anchored. Gather the fold at his hand with a restrained reveal. Preserve the selected portrait's pose, tree, rayed sun, village and foreground. The main wheel is substantial and partly hidden by the left frame. Its companion gear should read clearly beside it.
- Behind the veil, give broader, near-ivory cloud banks priority over the planets. Alternate banks with engraved strips and tuck small planets between them. Place some clouds in front of other clouds and a few in front of the planets and rainbow. The attached [cloud-sheet reference](studies/02-portrait/cloud-sheet-reference.jpeg) shows the overlap and diagonal layering.
- Move the individual cutouts at nine poses per second. Far cloud and pattern plates drift a few pixels. Nearer sheets drift slightly farther, with different timing and opposite directions. Keep all of that motion inside the reveal.
- Turn the wheel, crescent and companion gear on independent pivots. Rotate the sun's corona around the face and swap in the sideways-glance cel briefly. Give the stars and planets separate rotational timings. Pivot small branch tips and blades of grass while keeping their roots fixed.

## Iterations

| Study | What we learned |
| --- | --- |
| [01 · Landscape proof](studies/01-landscape/) | Established the diagonal star dome, decorated border and right-side landscape in the engraving's original proportions. |
| [02 · Portrait proofs](studies/02-portrait/) | Recomposed the portrait for a vertical phone. We tried a profile peeking out from the lifted fold. The user preferred the original turned-away traveler and supplied the selected portrait. |
| [03 · Flattened motion](studies/03-flattened-motion/) | Tried local shader movement on a single portrait and added MP4 and GIF previews after playback problems. The warped-paper effect missed the intended mechanical movement of separate cutouts. |
| [04 · First paper cutouts](studies/04-first-paper-cutouts/) | Tested rigid sprite turns, cloud-bank offsets, mesh-like clockwork, branch pivots and an alternate face cel. The layering worked structurally. The new placement exposed too much of the veil and gave the gears too little visual weight. |
| [05 · Approved layout with layered reveal](studies/05-layered-portrait/) | Returned to the preferred portrait, increased the visual weight of the clockwork and interleaved moving sheets. The stepped mechanical motion was close. The cloud banks still read too small, the planets too large, and the pale highlights too muted relative to the original engraving. |
| [Current · Broader cloud banks](current/) | Kept the approved layout and stepped cutout motion. Rebuilt the reveal with larger, near-ivory cloud banks and planets roughly one-third smaller, partially hidden between the sheets. This is the latest comparison pass. |

The earlier HTML and GIF variants were rebuilt from retained sources and preview media for this archive. Their original Library versions were unavailable for an exact byte comparison. The current HTML and GIF are the latest cloud revision. The previous layered portrait is preserved in Study 05.

## Preview and integration

Open the current HTML in a browser and select **Preview motion**. The GIF plays as a separate preview. Some iPhone file-preview viewers showed a static frame during review. Device-specific performance and playback are unverified.

For app integration, call `window.celestialOpening.bindLoading(startupPromise)` with the app's actual initialization promise. The animation runs while loading and returns to the finished still when readiness is signaled. There is no minimum wait. A ready-state button click dispatches `celestial:continue` on `window`. Either the system preference or the on-screen **Reduce motion** setting keeps the art still.

## Rebuild the current files

From this directory, run:

```sh
python3 -m pip install Pillow numpy scipy
python3 source/approved-output.py html gif
```

FFmpeg is required to encode the GIF. Outputs go to `animation/build/`. The build uses the existing art-pack PNGs, the approved portrait and the source templates. The HTML is self-contained once built.
