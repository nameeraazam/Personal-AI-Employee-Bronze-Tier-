---
name: update-dashboard-activity
description: "Appends a new line to Dashboard.md under ## Recent Activity with timestamp and short description of what was processed. Use this whenever the agent finishes handling a task from Needs_Action (e.g., created a plan, moved file to Done)."
trigger_keywords:
  - "update dashboard"
  - "log activity"
  - "append recent activity"
  - "task processed"
priority: medium
---

## Instructions for Claude

When this skill is triggered (or when you decide to log an activity after processing a file/task):

1. Get the current date/time in ISO-like format (e.g., 2026-02-18 04:15).
2. Read the existing content of Dashboard.md in the project root.
3. Find the section "## Recent Activity" (it should already exist from your starter file).
4. Append a new bullet point at the end of that section in this exact format:
   - [YYYY-MM-DD HH:MM] Processed [short description]. Example: Processed FILE_test.txt → plan created and moved to Done
5. Do NOT overwrite or delete existing content