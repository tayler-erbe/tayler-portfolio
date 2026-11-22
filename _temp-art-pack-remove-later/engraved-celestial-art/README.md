# Engraved celestial art pack (temporary)

Layered, hand-coloured engraving-style pieces for building a slowly animated opening scene, in the spirit of the 1888 Flammarion engraving (the figure lifting the edge of the sky). Temporary folder: it will be removed from this repository later.

`reference/original_engraving_reference.jpg` is the target composition: **landscape, about 1.26 : 1**, decorated border frame, a large diagonal navy star dome sweeping from the figure at lower left to the top right, the layers of "beyond the sky" under the dome's edge at upper left, a tree and a rayed sun at right, hills and a village behind the tree.

**Current best animation:** [layered mobile portrait](animation/README.md), with the preferred build, previous studies, and composition and motion notes.

## Folders

| Folder | What is in it | Notes |
|---|---|---|
| `scene_layers/` | 25 transparent PNG layers: `sky_dome`, `cloud_layer_1-3`, `rainbow_cloud_section_1-3`, `sun_face`, `moon_crescent`, `star_01-08`, `tree`, `figure_with_cloak`, `plants`, `rocks`, `landscape_foreground`, `village_horizon`, `border_left`, `border_right` | The source set. Canvas origin and anchor vary per file: place by eye. Edges of some pieces carry red/yellow fringes to clean. |
| `generated_scene_pieces/` | `beyond_sky` (flat full picture), `sky_dome_wide` (magenta key), `figure_no_cloak` and `cloak_held` (hazy glow around them), `ground_fill`, `sky_patch` | Fills for hidden parts and a figure that can lift its cloak. |
| `beyond_sky_layers/` | 12 separate layers for the area beyond the sky: `b01_night_sky`, `b02_wheel`, `b03_sun_rays`, `b04_rainbow`, `b05` and `b06` light bands, `b07` to `b11` five cloud banks far to near, `b12_zigzag_glow` | All on flat magenta (#FF00FF) except `b01`: key the magenta out. |
| `wheel_parts/` | `w1_wheel_only`, `w2_crescent_only`, `w3_hub`, `w4_gears` | Built to move as a clockwork: wheel and crescent counter-rotate about one centre, hub against the wheel, cogs mesh with the rim. `w2` and `w3` have a faint glow haze to remove. |
| `variety_sheets/` | 24 stars, 6 sun faces, 10 moons and phases, 8 planets, 6 trees, each on magenta in a loose grid | Cut each piece out by connected components. `x1_stars` has a hazy ground. |
| `loose_pieces/` | 14 extra single pieces (sun, moon phases, clouds, rocks, plants, landscape strips, borders, stars) | Same engraving style. |
| `cloud_banks/` | 5 long cloud banks with a hanging skirt of engraved streaks (`bank_1` small and far to `bank_5` rising to the right) | Transparent PNGs, already cut out. Used by the animation's reveal. |
| `sun_eye_cels/` | 6 sun-face medallions differing only in the eyes: far left, left, ahead, far right, half closed, closed | Transparent PNGs, already cut out. Used by the animation's sun. |
| `reference/` | The original engraving | Target layout. |

## Cleanup every piece needs

Key out flat magenta (#FF00FF) with a small tolerance and feather the edge a pixel; remove red/yellow fringe at piece edges; threshold the alpha of the pieces that came with a soft glow (`figure_no_cloak`, `cloak_held`, `w2`, `w3`, `x1_stars`); match scale and engraving density between pieces so nothing looks pasted.
