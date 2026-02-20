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
    new_activity = f"   - [{timestamp}] {description}"

    # Find the position right after ## Recent Activity section
    lines = content.split('\n')
    new_content_lines = []
    activity_section_found = False
    activity_section_processed = False

    for i, line in enumerate(lines):
        new_content_lines.append(line)

        if line.strip() == "## Recent Activity":
            activity_section_found = True
            # Continue processing the rest of the file but mark that we found the section
            continue

        # After we've found the activity section, look for where it ends
        if activity_section_found and not activity_section_processed:
            # Check if this is the line after the last activity item
            # If the current line is not an activity item or empty line,
            # then we want to insert before this line
            if i > 0 and lines[i-1].strip() == "## Recent Activity":
                # This is the line right after the header
                if not line.startswith("   - [") and line.strip() != "":
                    # If there are no activities yet, insert after the header
                    insert_pos = len(new_content_lines) - 1  # Insert at current position (before this line)
                    new_content_lines.insert(insert_pos, new_activity)
                    activity_section_processed = True
            elif line.startswith("   - ["):
                # This is an activity line, continue looking
                continue
            elif line.strip() == "":
                # This is an empty line within the activity section, continue looking
                continue
            else:
                # This is a non-activity line after the activity section, insert the new activity before it
                if not activity_section_processed:
                    insert_pos = len(new_content_lines) - 1  # Insert before this line
                    new_content_lines.insert(insert_pos, new_activity)
                    activity_section_processed = True

    # If we reached the end and haven't inserted the activity yet, add it at the end of the activity section
    if activity_section_found and not activity_section_processed:
        new_content_lines.append(new_activity)
        activity_section_processed = True

    if not activity_section_found:
        print(f"Error: ## Recent Activity section not found in {dashboard_path}")
        return False

    # Write updated content back to file
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content_lines))

    # Handle potential Unicode encoding issues for console output
    try:
        print(f"Activity logged: [{timestamp}] {description}")
    except UnicodeEncodeError:
        # Fallback for console that doesn't support Unicode
        safe_description = description.encode('ascii', 'replace').decode('ascii')
        print(f"Activity logged: [{timestamp}] {safe_description}")

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