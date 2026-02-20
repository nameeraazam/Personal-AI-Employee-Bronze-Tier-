# Personal AI Employee - Bronze Tier

A file-based AI automation system that monitors, processes, and manages tasks using Claude Code and agent skills.

## 🎯 Bronze Tier Achievement

This project meets all Bronze Tier requirements for the Personal AI Employee Hackathon:

- ✅ Folder structure: Inbox → Needs_Action → Done
- ✅ Dashboard.md + Company_Handbook.md
- ✅ Working filesystem watcher (watchdog-based)
- ✅ Claude Code read/write integration
- ✅ AI functionality as Agent Skills (.md files)
- ✅ Complete automation flow

## 📁 Project Structure

```
AI_Employee_Vault/
├── Inbox/                  # Drop files here - monitored by watcher
├── Needs_Action/           # Pending tasks (auto-created by watcher)
├── Done/                   # Completed tasks
├── Plans/                  # Task plans with checklists
├── Archive/                # Archived completed plans
├── skills/                 # Agent skill definitions (.md)
│   ├── basic-file-handler.md
│   └── task-analyzer.md
├── scripts/
│   ├── filesystem_watcher.py    # Monitors Inbox folder
│   └── orchestrator.py          # Processes tasks automatically
├── Dashboard.md            # Activity log
├── Company_Handbook.md     # Company context
└── requirements.txt        # Python dependencies
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `watchdog` - Filesystem monitoring library

### 2. Run the Filesystem Watcher

Open a terminal and start the watcher:

```bash
python scripts/filesystem_watcher.py
```

The watcher will:
- Monitor the `Inbox/` folder continuously
- Detect new files dropped into Inbox
- Copy them to `Needs_Action/` with `FILE_` prefix
- Create metadata `.md` files with frontmatter
- Log all actions to console

**Keep this running in the background.**

### 3. Run the Orchestrator

In a separate terminal, run the orchestrator:

**Single run (process once):**
```bash
python scripts/orchestrator.py
```

**Loop mode (check every 60 seconds):**
```bash
python scripts/orchestrator.py --loop 60
```

The orchestrator will:
- Scan `Needs_Action/` for task files
- Read metadata and determine task type
- Create plans in `Plans/` folder
- Move processed files to `Done/`
- Update `Dashboard.md` with activity logs

## 🧪 How to Test

### End-to-End Test

1. **Start the watcher:**
   ```bash
   python scripts/filesystem_watcher.py
   ```

2. **Drop a test file in Inbox:**
   ```bash
   echo "Test content" > Inbox/test_report.txt
   ```

3. **Check watcher output:**
   You should see:
   ```
   ✓ Copied: test_report.txt -> FILE_test_report.txt
   ✓ Created metadata: FILE_test_report.txt.md
   ```

4. **Verify Needs_Action folder:**
   ```bash
   ls Needs_Action/
   ```
   Should contain:
   - `FILE_test_report.txt` (copied file)
   - `FILE_test_report.txt.md` (metadata)

5. **Run orchestrator:**
   ```bash
   python scripts/orchestrator.py
   ```

6. **Check results:**
   - `Plans/` should have `Plan_FILE_test_report.txt.md`
   - `Done/` should have `FILE_test_report.txt.md`
   - `Dashboard.md` should have new log entry

### Expected Dashboard Entry

```markdown
## Recent Activity
   - [2026-02-20 17:24] Processed FILE_test_report.txt.md → plan created, moved to Done
```

## 🤖 Architecture Overview

```
┌─────────┐
│  Inbox  │ ← User drops files here
└────┬────┘
     │
     ▼
┌──────────────────┐
│ Filesystem       │ (watchdog monitors)
│ Watcher          │
└────┬─────────────┘
     │ Copies with FILE_ prefix
     │ Creates metadata .md
     ▼
┌─────────────────┐
│ Needs_Action/   │ ← Pending tasks
└────┬────────────┘
     │
     ▼
┌──────────────────┐
│ Orchestrator     │ (scans periodically)
│                  │
│ Uses Agent       │
│ Skills logic     │
└────┬─────────────┘
     │ Creates plans
     │ Moves to Done
     │ Logs to Dashboard
     ▼
┌─────────────────┐
│ Done/ + Plans/  │ ← Completed
│ Dashboard.md    │ ← Activity log
└─────────────────┘
```

## 🎨 Agent Skills

Skills are defined as `.md` files in the `skills/` folder:

### basic-file-handler.md
- Reads files from Needs_Action
- Creates plans with checkboxes
- Moves files to Done
- Updates Dashboard

### task-analyzer.md
- Analyzes file_drop metadata
- Suggests actions based on file type
- Chains to basic-file-handler

## 🔧 Claude Code Integration

This project is designed to work with Claude Code:

1. Claude can read/write all vault folders
2. Skills are invoked via `.md` instructions
3. Dashboard tracks all AI actions
4. Plans provide structured task management

### Using with Claude Code

```bash
# Ask Claude to process tasks
claude "Process all pending tasks in Needs_Action"

# Ask Claude to create a plan
claude "Create a plan for the new file in Needs_Action"

# Ask Claude to update dashboard
claude "Log today's completed tasks to Dashboard"
```

## 📋 Bronze Tier Checklist

- ✅ Folder structure (Inbox, Needs_Action, Done, Plans, Archive)
- ✅ Dashboard.md with activity logging
- ✅ Company_Handbook.md for context
- ✅ Filesystem watcher using watchdog
- ✅ Automated file detection and metadata creation
- ✅ Orchestrator for task processing
- ✅ Agent skills as .md files
- ✅ Complete automation flow
- ✅ Claude Code read/write integration
- ✅ Windows compatible (pathlib)
- ✅ Error handling and logging

## 🛠️ Troubleshooting

**Watcher not detecting files:**
- Ensure you're dropping files directly in `Inbox/` (not subfolders)
- Check file permissions
- Try restarting the watcher

**Orchestrator not processing:**
- Verify `.md` files exist in `Needs_Action/`
- Check frontmatter format (must start with `---`)
- Ensure Dashboard.md has `## Recent Activity` section

**Import errors:**
- Run `pip install -r requirements.txt`
- Verify Python 3.7+ is installed

## 📝 License

MIT License - Feel free to use and modify for the hackathon!

## 🏆 Hackathon Submission

This project demonstrates Bronze Tier capabilities:
- Automated file monitoring and processing
- Structured task management with plans
- Activity logging and tracking
- AI agent skill integration
- Complete end-to-end workflow

Built for the Personal AI Employee Hackathon 2026.
