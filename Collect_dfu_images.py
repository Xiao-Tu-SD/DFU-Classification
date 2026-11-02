

"""
collect_dfu_images.py
─────────────────────
Collects ALL ulcer images into one folder and ALL normal images
into another folder, then renames them sequentially.
 
Final structure:
    D:\Dia Foot\DFU\
        Diabetic Foot Ulcer\   <- ulcer_0001.jpg, ulcer_0002.jpg ...
        Normal\                <- normal_0001.jpg, normal_0002.jpg ...
 
Run:
    python collect_dfu_images.py
"""
 
import shutil
import csv
from pathlib import Path
 
# ──────────────────────────────────────────────
# CONFIG  ← your actual path
# ──────────────────────────────────────────────
ROOT = Path(r"D:\Dia Foot\DFU")
 
# All ulcer image sources
ULCER_SOURCES = [
    ROOT / "Original Images",
    ROOT / "Patches" / "Abnormal(Ulcer)",
    ROOT / "TestSet",
    ROOT / "Transfer-Learning images",
]
 
# All normal image sources
NORMAL_SOURCES = [
    ROOT / "Patches" / "Normal(Healthy skin)",
]
 
# Output folders
ULCER_OUT  = ROOT / "Diabetic Foot Ulcer"
NORMAL_OUT = ROOT / "Normal"
 
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
 
 
# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def collect_images(folders):
    """Collect all unique image files from a list of folders (recursive)."""
    seen, images = set(), []
    for folder in folders:
        if not folder.exists():
            print(f"  [!] Not found, skipping: {folder}")
            continue
        for f in sorted(folder.rglob("*")):
            if f.is_file() and f.suffix.lower() in IMG_EXTS and f not in seen:
                seen.add(f)
                images.append(f)
    return images
 
 
def copy_and_rename(files, out_folder, prefix):
    """Copy files to out_folder renamed as prefix_0001.ext ..."""
    out_folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx, src in enumerate(files, start=1):
        ext      = src.suffix.lower()
        new_name = f"{prefix}_{idx:04d}{ext}"
        dest     = out_folder / new_name
        shutil.copy2(str(src), str(dest))
        rows.append({"new_name": new_name, "original": str(src)})
        if idx % 100 == 0:
            print(f"    ... {idx} / {len(files)} copied")
    return rows
 
 
# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
print("=" * 55)
print("  DFU Image Collector")
print("=" * 55)
print(f"  Root : {ROOT}")
print()
 
# --- Scan ---
print("Scanning ulcer sources ...")
ulcer_files = collect_images(ULCER_SOURCES)
print(f"  -> {len(ulcer_files)} ulcer images found\n")
 
print("Scanning normal sources ...")
normal_files = collect_images(NORMAL_SOURCES)
print(f"  -> {len(normal_files)} normal images found\n")
 
# --- Copy & Rename ---
print(f"Copying ulcer images to: {ULCER_OUT}")
ulcer_rows = copy_and_rename(ulcer_files, ULCER_OUT, "ulcer")
print(f"  [DONE] {len(ulcer_rows)} ulcer images copied\n")
 
print(f"Copying normal images to: {NORMAL_OUT}")
normal_rows = copy_and_rename(normal_files, NORMAL_OUT, "normal")
print(f"  [DONE] {len(normal_rows)} normal images copied\n")
 
# --- Save Report ---
report_path = ROOT / "rename_report.csv"
with open(report_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["new_name", "original"])
    writer.writeheader()
    for row in ulcer_rows:
        writer.writerow({**row})
    for row in normal_rows:
        writer.writerow({**row})
 
# --- Summary ---
print("=" * 55)
print("  DONE!")
print("=" * 55)
print(f"  Diabetic Foot Ulcer/  ->  {len(ulcer_rows):>4} images (ulcer_0001 ...)")
print(f"  Normal/               ->  {len(normal_rows):>4} images (normal_0001 ...)")
print(f"  rename_report.csv     ->  full trace of every file")
print()
print("NEXT STEP: Tell me what to do next!")
print("  - Severity labelling (critical/moderate/healthy)?")
print("  - Train/Val/Test split?")
print("  - Start model training?")
