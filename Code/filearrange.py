#!/usr/bin/env python3
"""
Simple File Organizer

Organizes files into categorized folders based on their extensions.
"""

import os
import shutil
from pathlib import Path

# File categories and their extensions
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".md"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sh"],
    "Others": []
}

def get_category(file_extension):
    """Return the category for the given file extension."""
    for category, extensions in CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"

def organize_files(folder_path, dry_run=False):
    """Organize files in the given folder."""
    folder = Path(folder_path).resolve()
    
    if not folder.exists() or not folder.is_dir():
        print(f"Error: {folder} is not a valid directory.")
        return

    # Create category folders if they don't exist
    for category in CATEGORIES:
        if not (folder / category).exists() and not dry_run:
            (folder / category).mkdir(exist_ok=True)

    moved_files = 0
    skipped_files = 0

    for item in folder.iterdir():
        # Skip directories and organizer-created folders
        if item.is_dir() or item.parent.name in CATEGORIES:
            skipped_files += 1
            continue

        if item.is_file():
            category = get_category(item.suffix)
            target_dir = folder / category
            target_path = target_dir / item.name

            # Handle duplicate filenames
            counter = 1
            while target_path.exists():
                new_name = f"{item.stem}({counter}){item.suffix}"
                target_path = target_dir / new_name
                counter += 1

            if dry_run:
                print(f"[DRY RUN] Would move: {item.name} -> {category}/{target_path.name}")
            else:
                try:
                    shutil.move(str(item), str(target_path))
                    print(f"Moved: {item.name} -> {category}/{target_path.name}")
                    moved_files += 1
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")
                    skipped_files += 1

    print(f"\nSummary: Moved {moved_files} files, skipped {skipped_files} files")
    if dry_run:
        print("Note: Dry run mode - no files were actually moved.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Organize files into categories.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to organize (default: current)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    args = parser.parse_args()

    print(f"Organizing files in: {args.folder}")
    if args.dry_run:
        print("Running in dry-run mode (no changes will be made)\n")

    organize_files(args.folder, args.dry_run)