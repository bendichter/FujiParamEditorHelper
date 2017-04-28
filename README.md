# FujiParamEditorHelper
helper function for interacting with [FujiParamEditor](http://public.beuth-hochschule.de/~mixdorff/thesis/fujisaki.html) files in python.

## Installation

```bash
git clone https://github.com/bendichter/FujiParamEditorHelper.git
cd FujiParamEditorHelper
pip install .
```

## Usage
Interacting with .f0_ascii files:
```python
from FujiParamEditorHelper import write_f0_ascii, read_f0_ascii

write_f0_ascii(pitch, tt_pitch, fname)
read_f0_ascii(f0_ascii_file)
```

Interacting with .PAC files:
```python
from FujiParamEditorHelper import read_pac_file, get_accent_contour, get_phrase_contour, get_baseline
# for parameters:
read_pac_file(pac_file)

# for contours of components of model:
accent = get_accent_contour(pac_file)
phrase = get_phrase_contour(pac_file)
baseline = get_baseline(pac_file)
```

to reconstruct pitch from Fujisaki components:
```python
reconstructed_pitch = fuji2pitch(baseline, accent, phrase)
```

