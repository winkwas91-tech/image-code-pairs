# image-code-pairs

Build a manifest that pairs reference images with the Python scripts that describe them.

I used this kind of pairing when preparing an image-to-CAD dataset:
same stem name, one image, one script, one JSON row.

## Run

```bash
python3 build_manifest.py samples --out manifest.csv
python3 -m unittest discover -s tests -v
```

No extra packages.

## Matching rule

`samples/ring_18.png` + `samples/ring_18.py` → one row.

Rows with only an image or only a script are marked as `incomplete`.

## Output

```csv
id,image,script,status
ring_18,samples/ring_18.png,samples/ring_18.py,complete
band_wide,samples/band_wide.png,,incomplete
```
