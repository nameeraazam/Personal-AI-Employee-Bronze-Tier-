#!/usr/bin/env python3
"""
list-pending-tasks skill
Lists all pending tasks in Needs_Action/ folder and all pending plans in Plans/ folder and root.
"""

import sys
from pathlib import Path


def list_pending_tasks():
    """
    Lists all pending tasks in Needs_Action/ folder and all pending plans in Plans/ folder and root.
    """
    project_root = Path.cwd()
    needs_action_dir = project_root / "Needs_Action"
    plans_dir = project_root / "Plans"

    print("## Pending Tasks in Needs_Action/")
    print()

    # List all .md files in Needs_Action/
    needs_action_files = list(needs_action_dir.glob("*.md"))
    if needs_action_files:
        for file_path in needs_action_files:
            print(f"- {file_path.name}")
        print()
    else:
        print("No pending tasks in Needs_Action/ folder.")
        print()

    print("## Pending Plans")
    print()

    # List all plan files in Plans/ folder and root
    plan_files = []
    plan_files.extend(list(plans_dir.glob("Plan_*.md")))
    plan_files.extend(list(project_root.glob("Plan_*.md")))

    if plan_files:
        print("Pending plans found:")
        for file_path in plan_files:
            # Try to read the plan to check its status
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract status from YAML frontmatter if available
                status = "unknown"
                lines = content.split('\n')
                in_frontmatter = False
                for line in lines:
                    if line.strip() == '---' and not in_frontmatter:
                        in_frontmatter = True
                    elif line.strip() == '---' and in_frontmatter:
                        break
                    elif in_frontmatter and line.startswith('status:'):
                        status = line.split(':', 1)[1].strip()
                        break

                status_display = f" (status: {status})" if status != "unknown" else ""
                print(f"- {file_path.name}{status_display}")
            except:
                print(f"- {file_path.name} (could not read status)")

        print()
    else:
        print("No pending plans found.")
        print()

    print("## Summary")
    print(f"- Tasks in Needs_Action/: {len(needs_action_files)}")
    print(f"- Plans in system: {len(plan_files)}")

    return True


def main():
    list_pending_tasks()


if __name__ == "__main__":
    main()