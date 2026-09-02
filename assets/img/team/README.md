# Instructor photos

Drop Gopi's photos here using exactly these filenames, then run `python3 build.py`
from the repo root. The placeholders are replaced automatically.

| File | Crop | Target size |
|---|---|---|
| `gopi-portrait.jpg` | Portrait 4:5 | ~800 x 1000, under 150 KB |
| `gopi-car-1.jpg` | Square | ~400 x 400, under 80 KB |
| `gopi-lesson-1.jpg` | Square | ~400 x 400, under 80 KB |
| `gopi-student-pass.jpg` | Square | ~400 x 400, under 80 KB |

Alt text is already written for each slot in the `PHOTOS` dict in `content.py`.
Change it there if the photo you use shows something different, since accurate alt
text is both an accessibility requirement and a small image-search signal.

If a file is missing the site still builds and that slot keeps its placeholder.
