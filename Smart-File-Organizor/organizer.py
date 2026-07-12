#!/usr/bin/env python3
"""
Smart File Organizer
Automatically organize files into category folders
"""

import argparse
from pathlib import Path
import shutil

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
}

def get_category(file):
    extension = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
           return category
    return "Others"

def organize_folder(source_folder, dry_run=False):
    stats_dict = {}

    for cat in CATEGORIES:
       stats_dict[cat] = []

    total_processed = 0
    skipped = 0
    errors = 0

    for file in source_folder.iterdir():
        if not file.is_file():
            skipped += 1
            continue
        try:
           category = get_category(file)
           cat_folder = source_folder / category
           cat_folder.mkdir(exist_ok=True)

           target_path = cat_folder / file.name

           if not dry_run:
               if target_path.exists():
                  stem = target_path.stem
                  suffix = target_path.suffix
                  counter = 1
                  while True:
                      new_target = cat_folder / f"{stem}_{counter}{suffix}"
                      if not new_target.exists():
                          target_path = new_target
                          break
                      counter += 1

               shutil.move(str(file), str(target_path))
               stats_dict[category].append(target_path.name)
               total_processed += 1
               print(f"Moving {file.name} → {category}/")
           else:
               if target_path.exists():
                  print(f"[DRY RUN] Would rename {file.name} to {target_path.name}")
               else:
                  print(f"[DRY RUN] Would move {file.name} → {category}/")

        except PermissionError:
               errors += 1
               print(f"Permission denied: {file.name}")
        except Exception as e:
               errors += 1
               print(f"Error with {file.name}: {e}")

    return stats_dict, total_processed, skipped, errors

def stats(stats_dict, total_processed, skipped, errors):
    print("\nSummary:")
    for cat, files in stats_dict.items():
        count = len(files)
        if count > 0:
           print(f"- {cat}: {count} files")
    print(f"\nTotal processed: {total_processed}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_folder", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without doing it")
    parser.add_argument("--stats", action="store_true", help="Show detailed statistics")
    args = parser.parse_args()

    source = Path(args.source_folder)

    if not source.exists():
        print(f"Error: {source} not found!")
        return
    if not source.is_dir():
        print(f"Error: {source} is not a directory!")
        return

    stats_dict, total_processed, skipped, errors = organize_folder(Path(args.source_folder), args.dry_run)
    if args.stats:
       stats(stats_dict, total_processed, skipped, errors)
    print("Done!")

if __name__ == "__main__":
    main()
