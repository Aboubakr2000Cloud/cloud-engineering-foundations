# Week 6 — Python Data Structures & File I/O

## Overview
Week 6 focuses on Python's essential data structures (dictionaries, tuples, sets) and file I/O operations. The capstone project is a smart file organizer that automatically sorts messy folders into organized category structures using pattern matching and intelligent duplicate handling.

## Project: Smart File Organizer

A command-line utility that automatically organizes files into category folders based on their extensions. The tool features dry-run mode for safe previewing, comprehensive statistics tracking, and robust error handling for production use.

### Project Structure
```
cloud-learning-project/
├── organizer.py          # Main CLI application
└──  test_files/           # Test directory for validation
```

## Features

### Core Functionality
- **Automatic Categorization**: Sorts files into predefined categories (Images, Documents, Videos, Audio, Archives, Code)
- **Extension Mapping**: Recognizes 30+ common file extensions across 6 categories
- **Smart Directory Creation**: Creates category folders only when needed
- **Recursive-Safe**: Skips directories, processes only files

### User Safety
- **Dry-Run Mode**: Preview organization without modifying files (`--dry-run`)
- **Duplicate Handling**: Auto-renames conflicting files (e.g., `photo.jpg` → `photo_1.jpg`)
- **Error Recovery**: Gracefully handles permission errors and exceptions
- **Input Validation**: Verifies folder existence and type before processing

### Statistics & Reporting
- **Detailed Tracking**: Counts processed files, skipped items, and errors
- **Category Breakdown**: Shows files organized per category
- **Summary Report**: Displays comprehensive statistics with `--stats` flag
- **Real-time Feedback**: Shows each file move as it happens

### Command-Line Interface
- **Positional Arguments**: Simple folder path input
- **Optional Flags**: `--dry-run` and `--stats` for control
- **Auto-generated Help**: Built-in `--help` documentation
- **Professional Design**: Clear messages and user-friendly output

## Usage

### Basic Organization
```bash
# Organize a folder
python organizer.py ~/Downloads

# Preview what would happen (recommended first!)
python organizer.py ~/Downloads --dry-run

# Show detailed statistics
python organizer.py ~/Downloads --stats
```

### Command-Line Arguments
```
positional arguments:
  source_folder    Folder to organize

optional arguments:
  --dry-run        Show what would happen without doing it
  --stats          Show detailed statistics
  -h, --help       Show this help message and exit
```

### Example Session
```bash
$ python organizer.py test_files --dry-run

[DRY RUN] Would move photo.jpg → Images/
[DRY RUN] Would move document.pdf → Documents/
[DRY RUN] Would move song.mp3 → Audio/
[DRY RUN] Would move video.mp4 → Videos/
Done!

$ python organizer.py test_files --stats

Moving photo.jpg → Images/
Moving document.pdf → Documents/
Moving song.mp3 → Audio/
Moving video.mp4 → Videos/

Summary:
- Images: 1 files
- Documents: 1 files
- Audio: 1 files
- Videos: 1 files

Total processed: 4
Skipped: 0
Errors: 0
Done!
```

## File Categories

The organizer recognizes these file types:

| Category | Extensions |
|----------|------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg |
| **Documents** | .pdf, .doc, .docx, .txt, .odt, .xlsx |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg |
| **Archives** | .zip, .tar, .gz, .rar, .7z |
| **Code** | .py, .js, .html, .css, .java, .cpp |
| **Others** | Any unrecognized extension |

## What It Does

1. **Scans Source Folder**: Iterates through all files in the specified directory
2. **Determines Category**: Matches file extensions against predefined categories
3. **Creates Organization**: Builds category folders as needed within source directory
4. **Handles Duplicates**: Automatically renames files if conflicts exist
5. **Moves Files**: Transfers files to appropriate category folders
6. **Tracks Progress**: Maintains statistics on all operations
7. **Reports Results**: Displays summary of organization activity

## Skills Demonstrated

### Python Data Structures
- ✅ Dictionaries for category mapping and statistics tracking
- ✅ Dictionary iteration with `.items()` for category processing
- ✅ Dynamic dictionary creation for statistics initialization
- ✅ List comprehensions for data filtering

### File I/O & Path Operations
- ✅ pathlib for modern, cross-platform path handling
- ✅ Directory iteration with `Path.iterdir()`
- ✅ Path properties: `.suffix`, `.stem`, `.name`
- ✅ File type checking: `.is_file()`, `.is_dir()`
- ✅ Directory creation with `.mkdir(exist_ok=True)`

### System Operations
- ✅ File moving with `shutil.move()`
- ✅ Path validation and existence checking
- ✅ Error handling for permission issues
- ✅ Safe file operations with exception handling

### Command-Line Interface
- ✅ argparse for professional argument parsing
- ✅ Boolean flags with `action="store_true"`
- ✅ Positional and optional arguments
- ✅ Help message generation

### Error Handling
- ✅ Try-except blocks for file operations
- ✅ Specific exception handling (PermissionError)
- ✅ General exception catching with error messages
- ✅ Graceful degradation (continue on errors)

### Programming Patterns
- ✅ Function decomposition (get_category, organize_folder, stats)
- ✅ Dry-run pattern for safe operations
- ✅ Statistics tracking with counters
- ✅ Duplicate file handling with auto-increment
- ✅ Input validation before processing

## Technical Highlights

### Duplicate File Resolution
```python
# Auto-rename with counter
counter = 1
while True:
    new_target = cat_folder / f"{stem}_{counter}{suffix}"
    if not new_target.exists():
        target_path = new_target
        break
    counter += 1
```

### Category Detection
```python
def get_category(file):
    extension = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"
```

### Statistics Tracking
```python
stats_dict = {}
for cat in CATEGORIES:
    stats_dict[cat] = []

# Track files per category
stats_dict[category].append(target_path.name)
```

### Error Handling Pattern
```python
try:
    shutil.move(str(file), str(target_path))
except PermissionError:
    errors += 1
    print(f"Permission denied: {file.name}")
except Exception as e:
    errors += 1
    print(f"Error with {file.name}: {e}")
```

## Testing

### Create Test Environment
```bash
# Create test folder with sample files
mkdir test_files
cd test_files
touch photo.jpg document.pdf song.mp3 video.mp4 code.py archive.zip
cd ..
```

### Recommended Testing Flow
```bash
# 1. Preview with dry-run
python organizer.py test_files --dry-run

# 2. Check output looks correct

# 3. Actually organize
python organizer.py test_files

# 4. Verify results
ls test_files/
# Should show: Images/ Documents/ Audio/ Videos/ Code/ Archives/

# 5. Check statistics
python organizer.py test_files --stats
```

## Error Handling

The organizer handles these scenarios gracefully:

| Scenario | Behavior |
|----------|----------|
| **Folder not found** | Displays error, exits cleanly |
| **Path is file, not folder** | Displays error, exits cleanly |
| **Permission denied** | Logs error, continues with other files |
| **Duplicate filename** | Auto-renames with `_1`, `_2`, etc. |
| **General exceptions** | Logs specific error, continues processing |

## Project Files

### `organizer.py`
Main application containing:
- **CATEGORIES**: Dictionary mapping categories to file extensions
- **get_category()**: Determines file category from extension
- **organize_folder()**: Core logic for file organization with statistics tracking
- **stats()**: Display function for detailed statistics reporting
- **main()**: CLI argument parsing and program flow control

---

**Week 6 Complete!** This project demonstrates mastery of Python data structures, file I/O, path operations, and professional CLI design—essential skills for automation and systems programming in cloud engineering.
