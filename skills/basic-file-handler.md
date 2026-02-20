---
name: basic-file-handler
description: Read files, create summaries/plans, move to Done, append to Dashboard.md under Recent Activity
---

# Basic File Handler Skill

## Purpose
Process files from Needs_Action/ by creating plans, moving to Done/, and logging activity to Dashboard.

## Instructions

1. **Read the target file**
   - Look in `Needs_Action/` for any `.md` file
   - Read and understand the content

2. **Create a plan**
   - Create `Plan_[filename].md` in `Plans/` folder
   - Include frontmatter with task name and creation timestamp
   - Add checkboxes:
     - [ ] Review file content
     - [ ] Decide action (archive / escalate)
     - [ ] Move to Done/
     - [ ] Log to Dashboard

3. **Move file to Done/**
   - Move the original file from `Needs_Action/` to `Done/`
   - Preserve the filename

4. **Update Dashboard**
   - Append to `Dashboard.md` under `## Recent Activity` section
   - Format: `- [YYYY-MM-DD HH:MM] Processed [filename] → plan created, moved to Done`
   - Use current datetime in ISO format

5. **Output confirmation**
   - List all file paths created/updated/moved
   - Confirm completion

## Example Usage
```
Input: Needs_Action/FILE_report.txt.md
Output:
- Created: Plans/Plan_FILE_report.txt.md
- Moved: Needs_Action/FILE_report.txt.md → Done/FILE_report.txt.md
- Updated: Dashboard.md (appended log entry)
```
