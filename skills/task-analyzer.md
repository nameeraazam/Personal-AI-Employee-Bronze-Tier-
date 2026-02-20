---
name: task-analyzer
description: Analyze file_drop type files in Needs_Action/, suggest simple actions
---

# Task Analyzer Skill

## Purpose
Analyze metadata files in Needs_Action/ to determine file type and suggest appropriate actions.

## Instructions

1. **Scan Needs_Action/ folder**
   - Look for `.md` files with frontmatter
   - Read the metadata section

2. **Analyze file type**
   - Check `type:` field in frontmatter
   - If `type: file_drop`:
     - Read `original_name`, `size_bytes`, `detected_at`, `status`
     - Determine file category based on name/extension

3. **Suggest actions**
   - **Test files** (TEST_*, test.*, sample.*): Suggest archive after review
   - **Documents** (.pdf, .docx, .txt): Suggest review and summarize
   - **Data files** (.csv, .xlsx, .json): Suggest parse and extract key info
   - **Images** (.jpg, .png, .gif): Suggest extract metadata
   - **Important/Unknown**: Suggest escalate for manual review

4. **Create simple plan (optional)**
   - If action is clear, create `Plan_[filename].md` in `Plans/`
   - Include suggested action steps as checkboxes

5. **Chain to basic-file-handler**
   - After analysis, invoke `basic-file-handler` skill to execute:
     - Create plan
     - Move to Done/
     - Log to Dashboard

6. **Output analysis summary**
   - File analyzed: [filename]
   - Type detected: [type]
   - Suggested action: [action]
   - Status: [chained to handler / completed]

## Example Usage
```
Input: Needs_Action/FILE_test_document.txt.md
Analysis:
- Type: file_drop
- Original: test_document.txt
- Category: test file
- Suggested action: Review and archive
- Chaining to basic-file-handler...
```

## Integration
This skill works best when:
- Filesystem watcher has created metadata files
- Files need automated triage
- You want to chain to basic-file-handler for execution
