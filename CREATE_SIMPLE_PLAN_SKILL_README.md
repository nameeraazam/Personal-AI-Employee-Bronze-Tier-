# Create Simple Plan Skill

This skill reads .md files from the Needs_Action/ folder, creates basic plan files with checkbox steps, and moves the original task files to Done/.

## How it works

The skill:
1. Looks for .md files in the Needs_Action/ folder
2. For each file, creates a Plan_[filename].md file with basic steps
3. Moves the original task file to the Done/ folder
4. Logs the activity to Dashboard.md

## Usage

Run the command:
```bash
python create_simple_plan.py
```

## Features

- Processes all .md files in Needs_Action/ folder
- Creates plan files with proper frontmatter
- Moves processed files to Done/ folder
- Logs activities to Dashboard.md
- Handles errors gracefully
- Works with existing Plans/ folder if present

## Plan File Format

Each plan file includes:
- YAML frontmatter with origin, creation time, and status
- Title based on the original filename
- 5 checkbox steps for basic task processing
- Proper file naming (Plan_[original-name].md)