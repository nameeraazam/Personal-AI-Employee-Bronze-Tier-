---
name: list-pending-tasks
description: "Lists all pending tasks in Needs_Action/ folder and all pending plans in Plans/ folder and root. Use this to get an overview of work that needs to be done."
trigger_keywords:
  - "list pending"
  - "show tasks"
  - "pending tasks"
  - "what to do"
  - "list work"
priority: medium
---

## Instructions for Claude

When this skill is triggered:

1. List all .md files in the Needs_Action/ folder (these are new tasks to be processed).
2. List all plan files (starting with "Plan_") in both the Plans/ folder and root directory.
3. For each plan file, attempt to read its status from the YAML frontmatter.
4. Display the status of each plan (pending, completed, etc.).
5. Provide a summary count of tasks in each location.
6. Format the output in a clear, readable way.

## Implementation

Run the following command to list all pending tasks:
```bash
python list_pending_tasks.py
```