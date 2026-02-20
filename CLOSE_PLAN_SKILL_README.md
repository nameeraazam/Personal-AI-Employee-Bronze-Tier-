# Close Plan and Archive Skill

This skill marks plan files as completed and archives them to the Archive/ folder.

## How it works

The skill:
1. Takes a plan file (or processes all plan files if none specified)
2. Updates the YAML frontmatter to mark status as "completed"
3. Adds a completion timestamp to the frontmatter
4. Moves the plan to the Archive/ folder with a timestamp in the filename
5. Logs the activity to Dashboard.md

## Usage

To close and archive a specific plan:
```bash
python close_plan_and_archive.py Plan_FILE_example.md
```

To close and archive all pending plans:
```bash
python close_plan_and_archive.py
```

## Features

- Updates YAML frontmatter with status and completion timestamp
- Archives files with timestamped names in Archive/ folder
- Logs activities to Dashboard.md
- Handles errors gracefully
- Works with plans in root or Plans/ folder
- Preserves original content while updating metadata