# Instructor photos

Drop Gopi's photos here using exactly these filenames, then run `python3 build.py`
from the repo root. The placeholders are replaced automatically.

| File | Crop | Target size |
|---|---|---|
| `gopi-portrait.jpg` | Portrait 4:5 | ~800 x 1000, under 150 KB |
| `gopi-lesson-1.jpg` | Square | ~400 x 400, under 80 KB |
| `gopi-student-pass-woman.jpg` | Square | ~400 x 400, under 80 KB |
| `gopi-student-pass.jpg` | Square | ~400 x 400, under 80 KB |

The strip renders left to right in the order listed in the `PHOTOS["strip"]` list
in `content.py`, currently: guy (`gopi-lesson-1.jpg`), woman
(`gopi-student-pass-woman.jpg`) in the middle, guy (`gopi-student-pass.jpg`).
Reorder that list to change the arrangement.

Alt text is already written for each slot in the `PHOTOS` dict in `content.py`.
Change it there if the photo you use shows something different, since accurate alt
text is both an accessibility requirement and a small image-search signal. The hero
slot also has `caption_label` / `caption_name` fields (e.g. "The training vehicle" /
"Adelaide Confident Driving Academy") that overlay the photo — update those too if
the hero photo changes back to a portrait of Gopi (`caption_label: "Lead instructor"`).

If a file is missing the site still builds and that slot keeps its placeholder.

Filled as of 2026-09-10: `gopi-portrait.jpg` is the branded side-on shot of the
Vitara (a marketing mockup, not a candid photo). The strip is three students with
their Certificate of Competency — two young men either side, the woman in the
middle. `gopi-car-1.jpg` (the rear 3/4 shot of the car) is still in this folder
but no longer used on the page, since the strip is all-student now — swap it back
in for one of the three if you'd rather show the car again. Full-resolution
originals are kept in the client's `uploaded_assets/` folder, one level up from
the web project.
