# Cordova Pharmaceuticals — division logos

Logo assets for the *Planning in a Day* lab dataset. Cordova Pharmaceuticals is a
fictitious company used for course narrative only.

## Contents

| File | Division | Initials | Brand color | Glyph |
|---|---|---|---|---|
| `cordova-biosolutions.png` | Cordova BioSolutions | CBS | `#1B6AC9` | double helix |
| `cordova-neurosciences.png` | Cordova NeuroSciences | CNS | `#2F6F3E` | neuron |
| `cordova-cardio-labs.png` | Cordova Cardio Labs | CCL | `#C2334D` | heart + ECG |
| `cordova-oncology.png` | Cordova Oncology | CO | `#6B3FA0` | cell + nucleus |
| `cordova-consumer-health.png` | Cordova Consumer Health | CCH | `#E0761B` | leaf |
| `cordova-respiratory.png` | Cordova Respiratory | CR | `#0E9488` | lungs |

Each division also ships an `@512` variant for slides and print. The workbook
references the 96px files.

## Publishing

Both Excel's `IMAGE()` function and Fabric image columns require a URL that is
**https, publicly readable with no sign-in, and not redirected**. A public GitHub
repo satisfies all three.

```bash
# from the folder containing this README
git init
git add .
git commit -m "Cordova division logos"
git branch -M main
git remote add origin https://github.com/<OWNER>/cordova-assets.git
git push -u origin main
```

Files are then served at:

```
https://raw.githubusercontent.com/<OWNER>/cordova-assets/main/logos/<file>.png
```

Confirm it works by opening one of those URLs in a private browser window. If it
renders without a login prompt, Excel and Fabric will both resolve it.

## Repointing the workbook

The workbook ships with `YOUR-GITHUB-ORG` as a placeholder. Replace it with your
owner and repo — find-and-replace across the `Logo URL` column, or re-run
`rewrite_urls.py` with `BASE` changed.

## Regenerating

`make_logos.py` redraws all six from scratch. Colors, initials and glyph
assignments live in the `DIVISIONS` list at the top.
