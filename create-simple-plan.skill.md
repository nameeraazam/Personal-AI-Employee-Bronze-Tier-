---
name: create-simple-plan
description: "Reads a .md file from Needs_Action/, creates a basic Plan_[filename].md in the root (or Plans/ folder if exists) with 3-5 checkbox steps, then moves the original task file to Done/. Use this for every new task file discovered in Needs_Action/ during Bronze Tier processing."
trigger_keywords:
  - "process needs_action"
  - "create plan"
  - "plan for task"
  - "handle file drop"
priority: high
---

## Instructions for Claude

When this skill is triggered (or when processing a file in Needs_Action/):

1. List all .md files in Needs_Action/ folder.
2. For each file (process one at a time if multiple):
   a. Read the full content of the file (e.g., FILE_something.md).
   b. Determine a short task name from filename or content (e.g., "review dropped file test.txt").
   c. Create a new file in root called Plan_[original-filename-without-ext].md (example: Plan_FILE_test.md).
   d. Write this structure inside the new Plan file:

      ---
      task_origin: Needs_Action/[original-file.md]
      created: [current ISO datetime]
      status: pending
      ---

      # Plan for [short task name]

      - [ ] Review the content of the dropped file
      - [ ] Decide required actions (e.g., archive, escalate, summarize)
      - [ ] Execute basic next step if safe (no external actions in Bronze)
      - [ ] Move original task file to Done/ when finished
      - [ ] Log activity to Dashboard.md

   e. After creating the Plan file, move the original .md from Needs_Action/ to Done/.
   f. Append to Dashboard.md using the update-dashboard-activity skill if available (or manually log: "Created plan for [task] and moved to Done").

3. If no files in Needs_Action/: Output "No pending tasks in Needs_Action/."
4. Handle errors gracefully: If file can't be moved/read, log reason and stop without crashing.

This skill keeps things simple for Bronze Tier — no complex reasoning yet, just planning + file movement.

## Implementation

Run the following command to process files in Needs_Action/:
```bash
python create_simple_plan.py
```