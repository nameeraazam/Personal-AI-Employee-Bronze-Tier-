#!/usr/bin/env python3
"""
update-dashboard-activity skill
Appends a new line to Dashboard.md under ## Recent Activity with timestamp and short description.
"""

import sys
from datetime import datetime
from pathlib import Path


def update_dashboard_activity(description: str):
    """
    Appends a new line to Dashboard.md under ## Recent Activity with timestamp and description.

    Args:
        description (str): Short description of what was processed
    """
    project_root = Path.cwd()
    dashboard_path = project_root / "Dashboard.md"

    # Check if Dashboard.md exists
    if not dashboard_path.exists():
        print(f"Error: {dashboard_path} does not exist")
        return False

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Read existing content
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the ## Recent Activity section
    if "## Recent Activity" not in content:
        print(f"Error: ## Recent Activity section not found in {dashboard_path}")
        return False

    # Prepare the new activity line
    new_activity = f"   - [{timestamp}] {description}\n"

    # Split content to insert the new activity line
    lines = content.split('\n')
    new_content_lines = []

    for i, line in enumerate(lines):
        new_content_lines.append(line)
        if line.strip() == "## Recent Activity":
            # Add the new activity right after the header
            # Check if there are already activities below
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                # Insert before the next non-empty line
                # Find where the activity list ends
                insert_idx = i + 1
                while insert_idx < len(lines) and lines[insert_idx].startswith("   - "):
                    insert_idx += 1
                # Insert at the end of the existing list
                new_content_lines = new_content_lines[:insert_idx] + [new_activity.rstrip()] + new_content_lines[insert_idx:]
            else:
                # If no activities exist yet, just add the new one
                new_content_lines.append(new_activity.rstrip())

    # Write updated content back to file
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content_lines))

    print(f"Activity logged: [{timestamp}] {description}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python update-dashboard-activity.py \"description of what was processed\"")
        print("Example: python update-dashboard-activity.py \"Processed FILE_test.txt -> plan created and moved to Done\"")
        sys.exit(1)

    description = sys.argv[1]
    update_dashboard_activity(description)


if __name__ == "__main__":
    main()