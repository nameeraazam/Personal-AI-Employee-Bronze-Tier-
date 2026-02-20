# List Pending Tasks Skill

This skill provides an overview of all pending tasks and plans in the system.

## How it works

The skill:
1. Lists all .md files in the Needs_Action/ folder (new unprocessed tasks)
2. Lists all plan files in both the Plans/ folder and root directory
3. Reads the status of each plan from its YAML frontmatter
4. Provides a summary count of items in each location
5. Formats the output in a clear, readable way

## Usage

Run the command:
```bash
python list_pending_tasks.py
```

## Features

- Shows unprocessed tasks in Needs_Action/ folder
- Displays plans with their current status
- Counts items in each location
- Works with plans in root or Plans/ folder
- Clear, formatted output for easy scanning
- Reads plan status from YAML frontmatter