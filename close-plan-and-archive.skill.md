---
name: close-plan-and-archive
description: "Marks a plan as completed, updates its status in the YAML frontmatter, and moves it to the Archive/ folder with a timestamp. Use this when finishing work on a plan."
trigger_keywords:
  - "close plan"
  - "archive plan"
  - "complete plan"
  - "finish task"
priority: high
---

## Instructions for Claude

When this skill is triggered:

1. If a specific plan filename is provided as an argument, process that plan file.
2. If no argument is provided, process all plan files found.
3. Locate plan files in either the root directory or Plans/ folder (files starting with "Plan_").
4. Update the YAML frontmatter in the plan file:
   - Change status from "pending" to "completed"
   - Add a "completed: [current ISO datetime]" field
5. Move the updated plan file to the Archive/ folder with an updated name that includes a timestamp.
6. Log the activity to Dashboard.md using the update-dashboard-activity skill if available.
7. Handle errors gracefully.

## Implementation

Run the following command to close and archive a specific plan:
```bash
python close_plan_and_archive.py Plan_FILE_example.md
```

Run the following command to close and archive all pending plans:
```bash
python close_plan_and_archive.py
```