# Week 6 — Python Data Structures & File I/O: Key Learnings

## Core Concepts Mastered

### Data Structures

**Dictionaries (Key-Value Pairs)**
- Creating and accessing dictionaries with `{}` syntax
- Dictionary methods: `.get()`, `.items()`, `.keys()`, `.values()`
- Iterating with `for key, value in dict.items()`
- Dictionary comprehensions for data transformation
- Use case: Counting occurrences, grouping data, lookups

**Tuples (Immutable Sequences)**
- Creating tuples with `()` syntax
- Tuple unpacking: `x, y, z = (1, 2, 3)`
- When to use: Function returns, fixed data, dictionary keys
- Immutability prevents accidental modification

**Sets (Unique Collections)**
- Creating sets with `{}` or `set()`
- Mathematical operations: union `|`, intersection `&`, difference `-`
- Fast membership testing with `in`
- Removing duplicates from lists
- Use case: Unique values, set operations

### File Operations

**Reading & Writing Files**
- Context managers with `with open()` for automatic cleanup
- File modes: `'r'` (read), `'w'` (write/overwrite), `'a'` (append)
- Reading patterns: `.read()`, `.readlines()`, line-by-line iteration
- Writing with `.write()` and `.writelines()`

**JSON Data**
- `json.load()` - Read JSON from file to Python dict/list
- `json.dump()` - Write Python dict/list to JSON file
- `json.loads()` / `json.dumps()` - String conversions
- Use case: Configuration files, data persistence

**CSV Files**
- `csv.reader()` for reading CSV data
- `csv.DictReader()` for accessing columns by name
- `csv.writer()` and `csv.DictWriter()` for writing
- Handling headers and structured data

### OS & Path Operations

**pathlib Module (Modern)**
- `Path` objects for cross-platform path handling
- Path operations: `.exists()`, `.is_file()`, `.is_dir()`
- Listing files: `.iterdir()`, `.glob()`, `.rglob()`
- Path properties: `.name`, `.stem`, `.suffix`, `.parent`
- Creating directories: `.mkdir(parents=True, exist_ok=True)`
- Reading/writing: `.read_text()`, `.write_text()`

**os Module**
- `os.listdir()` - List directory contents
- `os.walk()` - Recursive directory traversal
- `os.path.join()` - Platform-independent path joining
- File info: `os.path.getsize()`, `os.path.getmtime()`

**shutil Module**
- `shutil.copy()` - Copy files
- `shutil.move()` - Move/rename files
- `shutil.rmtree()` - Remove directory trees

### Command-Line Arguments

**argparse Module**
- `ArgumentParser()` - Create CLI interface
- Positional arguments: `parser.add_argument("name")`
- Optional arguments: `parser.add_argument("-f", "--flag")`
- Flags: `action="store_true"` for boolean options
- Type conversion: `type=int`, `type=float`
- Choices validation: `choices=["option1", "option2"]`
- Help messages: Automatic `--help` generation

## Practical Patterns Learned

### Safe File Operations
```python
# Check before operating
if path.exists() and path.is_file():
    # Process file
```

### Error Handling for Files
```python
try:
    with open("file.txt") as f:
        content = f.read()
except FileNotFoundError:
    # Handle missing file
except PermissionError:
    # Handle permission issues
```

### Duplicate File Handling
```python
# Auto-rename with counter
counter = 1
while target.exists():
    target = folder / f"{stem}_{counter}{suffix}"
    counter += 1
```

### Statistics Tracking
```python
# Use dictionaries to count
stats = {category: 0 for category in categories}
stats[category] += 1
```

### Dry-Run Pattern
```python
if dry_run:
    print(f"Would move {file}")
else:
    shutil.move(file, target)
```

## Key Takeaways

### When to Use Which Data Structure
- **List**: Ordered collection, allow duplicates, need indexing
- **Dict**: Key-value mapping, fast lookups, structured data
- **Tuple**: Immutable data, function returns, fixed collections
- **Set**: Unique values only, membership testing, set operations

### File I/O Best Practices
- Always use `with` statement for automatic cleanup
- Handle `FileNotFoundError` and `PermissionError`
- Use pathlib for modern, readable path handling
- Validate paths before operations

### CLI Script Design
- Use argparse for professional argument handling
- Provide helpful `--help` messages
- Validate inputs before processing
- Use dry-run mode for destructive operations
- Show progress and statistics to users

### Real-World Applications
- **Configuration management**: JSON files for settings
- **Data processing**: CSV reading/writing for structured data
- **File organization**: Automated folder management
- **Log analysis**: Processing and filtering log files
- **Backup scripts**: Copying and archiving files

---

## Learning through mini-projects

- Down below a series of practical Python mini-projects for the week6 of Python Data Structures & File I/O, and it documents the challenges I faced, and how I solved them and some key concepts learned. The goal was to move from basic scripting to a **clean, professional CLI tool** minds.
  
### Mini-project 1: File Iteration & Duplicate Detection

#### 🔹 New Concepts Learned

* `pathlib.Path` and why it’s better than raw strings
* Recursive file traversal with `rglob("*")`
* Using dictionaries to group related data
* Understanding **keys vs values** in dictionaries

#### ⚠️ Challenges Faced

* Script wasn’t detecting duplicates even though files existed
* Confusion between filenames vs full paths
* Printing duplicates inside the loop (wrong place)

#### ✅ Final Solution

* Use filename (or size) as dictionary key
* Store **list of paths** as value
* Move duplicate detection **after** the loop

Key idea:

```python
files_dict.setdefault(filename, []).append(file)
```

### Mini-project 2: File Size Comparison with Flags

#### 🔹 New Concepts Learned

* `argparse` flags with `action="store_true"`
* Switching behavior using CLI flags (`--size-mode`)
* File metadata using `file.stat().st_size`

#### ⚠️ Challenges Faced

* `--size_mode` not working
* Logic executed but output was empty

#### ✅ Final Solution

* Correct flag definition
* Use `args.size_mode` inside logic

Key idea:

```python
if args.size_mode:
    key = size
else:
    key = filename
```

### Mini-project 3: Backup Script (Copy + Compress)

#### 🔹 New Concepts Learned

* Creating directories safely with `mkdir(parents=True, exist_ok=True)`
* Copying files using `shutil.copy`
* ZIP creation with `shutil.make_archive`
* Absolute vs relative paths

#### ⚠️ Challenges Faced

* Destination folder created but empty
* Files silently overwriting each other

#### ✅ Final Solution

* Use absolute paths
* Prevent overwriting by renaming duplicates

Key idea:

```python
if target_path.exists():
    counter += 1
```

### Mini-project 4: Cleaner Script (Delete by Days / Size)

#### 🔹 New Concepts Learned

* File timestamps (`st_mtime`)
* `datetime.timedelta`
* Optional CLI arguments
* Industry-standard `--dry-run`

#### ⚠️ Challenges Faced

* Misunderstanding dry-run purpose
* Optional arguments logic
* Confirmation before deletion

#### ✅ Final Solution

* Dry-run only prints actions
* Confirmation via `input()`
* Deletion logic isolated and safe

Key idea:

```python
if dry_run:
    print("[DRY-RUN] Would delete")
else:
    file.unlink()
```

### Final Project: Smart File Organizer 🗂️

#### 🎯 Project Goal

Automatically organize files into category folders with a professional CLI.

#### 🔹 Core Concepts Mastered

* CLI design with `argparse`
* Clean project structure
* File categorization by extension
* Dry-run safety mode
* Statistics tracking
* Error handling
* Duplicate filename resolution

#### ⚠️ Key Challenges & Solutions

##### 1️⃣ Category Detection

**Problem:** Mapping extensions to folders

**Solution:**

```python
def get_category(file):
    for cat, exts in CATEGORIES.items():
        if file.suffix.lower() in exts:
            return cat
    return "Others"
```

##### 2️⃣ Dry-Run Logic

**Problem:** Avoid moving files while still showing actions

**Solution:**

```python
if not dry_run:
    shutil.move(...)
else:
    print("[DRY-RUN]")
```

---

####" 3️⃣ Duplicate Filename Handling

**Problem:** Files overwriting each other

**Solution:** Increment filename until free

```python
file_1.txt, file_2.txt, ...
```

####" 4️⃣ Statistics Tracking

**Learned:**

* Dictionaries of lists
* Counting via `len()`

```python
Stats[category].append(file.name)
```

##### 5️⃣ Scope & Return Values

**Big Concept Learned:**

* Functions return **tuples**
* Order matters
* Variable names inside/outside functions are independent

```python
return Stats, total_processed, skipped, errors
```

#### 🧠 Engineering Mindset Gained

* Separation of concerns
* Defensive programming
* Safe file operations
* CLI-first thinking
* Readability > cleverness

### 🚀 Final Outcome

✅ Professional CLI tool
✅ Safe file operations
✅ Clean logic
✅ Industry practices

**Technical highlights:**
- Dictionary-based category system
- pathlib for cross-platform compatibility
- argparse for professional CLI
- Exception handling for graceful degradation
- Statistics tracking with dictionaries

---


