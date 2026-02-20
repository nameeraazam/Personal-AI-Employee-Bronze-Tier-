#!/usr/bin/env python3
"""
create-simple-plan skill
Reads .md files from Needs_Action/, creates Plan_[filename].md files with basic steps, then moves originals to Done/.
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import shutil


def create_simple_plan():
    """
    Reads .md files from Needs_Action/, creates Plan_[filename].md files with basic steps,
    then moves originals to Done/.
    """
    project_root = Path.cwd()
    needs_action_dir = project_root / "Needs_Action"
    done_dir = project_root / "Done"
    dashboard_path = project_root / "Dashboard.md"

    # Ensure directories exist
    needs_action_dir.mkdir(exist_ok=True)
    done_dir.mkdir(exist_ok=True)

    # Find all .md files in Needs_Action/
    md_files = list(needs_action_dir.glob("*.md"))

    if not md_files:
        print("No pending tasks in Needs_Action/.")
        return True

    success_count = 0

    for file_path in md_files:
        try:
            print(f"Processing: {file_path.name}")

            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Determine a short task name from filename
            original_filename = file_path.name
            task_name = original_filename.replace('.md', '').replace('FILE_', 'file ').replace('_', ' ').strip()

            # Create the plan filename
            plan_filename = f"Plan_{original_filename.replace('.md', '')}.md"

            # Decide where to save the plan file (root or Plans/ folder if exists)
            plans_dir = project_root / "Plans"
            if plans_dir.exists():
                plan_path = plans_dir / plan_filename
            else:
                plan_path = project_root / plan_filename

            # Generate current ISO datetime
            created_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

            # Create the plan content
            plan_content = f"""---
task_origin: Needs_Action/{original_filename}
created: {created_time}
status: pending
---

# Plan for {task_name}

- [ ] Review the content of the dropped file
- [ ] Decide required actions (e.g., archive, escalate, summarize)
- [ ] Execute basic next step if safe (no external actions in Bronze)
- [ ] Move original task file to Done/ when finished
- [ ] Log activity to Dashboard.md
"""

            # Write the plan file
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(plan_content)

            print(f"Created plan: {plan_path.name}")

            # Move the original file to Done/
            done_file_path = done_dir / original_filename
            shutil.move(str(file_path), str(done_file_path))

            print(f"Moved original task to Done/: {original_filename}")

            # Log activity to Dashboard.md
            log_to_dashboard = project_root / "update_dashboard_activity_fixed.py"
            if log_to_dashboard.exists():
                try:
                    import subprocess
                    subprocess.run([sys.executable, str(log_to_dashboard), f"Created plan for {task_name} and moved to Done"],
                                 check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    # If the skill script fails, log manually
                    with open(dashboard_path, 'a', encoding='utf-8') as f:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        f.write(f"\n   - [{timestamp}] Created plan for {task_name} and moved to Done")
            else:
                # Manual logging if the skill script doesn't exist
                if dashboard_path.exists():
                    with open(dashboard_path, 'a', encoding='utf-8') as f:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        f.write(f"\n   - [{timestamp}] Created plan for {task_name} and moved to Done")

            print(f"Logged activity for: {task_name}")
            success_count += 1

        except PermissionError:
            print(f"Error: Permission denied when processing {file_path}")
            continue
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue

    print(f"Successfully processed {success_count} file(s)")
    return True


def main():
    create_simple_plan()


if __name__ == "__main__":
    main()