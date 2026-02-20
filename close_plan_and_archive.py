#!/usr/bin/env python3
"""
close-plan-and-archive skill
Marks a plan as completed, updates its status, and archives it to Archive/ folder.
"""

import sys
from datetime import datetime
from pathlib import Path
import shutil


def close_plan_and_archive(plan_filename=None):
    """
    Marks a plan as completed, updates its status, and archives it to Archive/ folder.

    Args:
        plan_filename (str): Name of the plan file to close, or None to process all pending plans
    """
    project_root = Path.cwd()
    plans_dir = project_root / "Plans"
    archive_dir = project_root / "Archive"
    dashboard_path = project_root / "Dashboard.md"

    # Create archive directory if it doesn't exist
    archive_dir.mkdir(exist_ok=True)

    # Determine which plan(s) to process
    plans_to_process = []

    if plan_filename:
        # Process specific plan
        plan_path = plans_dir / plan_filename
        if plan_path.exists():
            plans_to_process = [plan_path]
        else:
            # Also check in root directory
            plan_path = project_root / plan_filename
            if plan_path.exists():
                plans_to_process = [plan_path]
            else:
                print(f"Error: Plan file {plan_filename} not found in Plans/ or root directory")
                return False
    else:
        # Process all plan files
        plans_to_process = list(plans_dir.glob("Plan_*.md"))
        # Also include plan files in root directory
        plans_to_process.extend(list(project_root.glob("Plan_*.md")))

    if not plans_to_process:
        if plan_filename:
            print(f"Error: Plan file {plan_filename} not found")
            return False
        else:
            print("No plan files found to close.")
            return True

    success_count = 0

    for plan_path in plans_to_process:
        try:
            # Read the current plan content
            with open(plan_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the content to find and update the YAML frontmatter
            lines = content.split('\n')
            updated_lines = []
            in_frontmatter = False
            frontmatter_started = False
            frontmatter_ended = False
            status_updated = False
            completed_updated = False

            i = 0
            while i < len(lines):
                line = lines[i]

                if line.strip() == '---' and not frontmatter_started:
                    # Start of frontmatter
                    frontmatter_started = True
                    in_frontmatter = True
                    updated_lines.append(line)
                elif line.strip() == '---' and frontmatter_started and not frontmatter_ended and i > 0:
                    # End of frontmatter
                    frontmatter_ended = True
                    in_frontmatter = False
                    # Add status and completed fields if they weren't found in the frontmatter
                    if not status_updated:
                        updated_lines.append('status: completed')
                    if not completed_updated:
                        completed_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                        updated_lines.append(f'completed: {completed_time}')
                    updated_lines.append(line)
                elif in_frontmatter and line.strip().startswith('status:'):
                    # Update status to completed
                    updated_lines.append('status: completed')
                    status_updated = True
                elif in_frontmatter and line.strip().startswith('completed:'):
                    # Update completed timestamp
                    completed_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                    updated_lines.append(f'completed: {completed_time}')
                    completed_updated = True
                else:
                    updated_lines.append(line)

                i += 1

            # If no frontmatter exists, add it at the beginning
            if not frontmatter_started:
                completed_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                updated_lines = ['---', 'status: completed', f'completed: {completed_time}', '---', ''] + lines

            # Write the updated content back to the file
            updated_content = '\n'.join(updated_lines)

            # Write the updated content back to the file
            updated_content = '\n'.join(updated_lines)
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            # Create archived filename with timestamp
            stem = plan_path.stem
            suffix = plan_path.suffix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archived_filename = f"{stem}_completed_{timestamp}{suffix}"
            archived_path = archive_dir / archived_filename

            # Move the plan to the Archive folder with new name
            shutil.move(str(plan_path), str(archived_path))

            print(f"Plan {plan_path.name} marked as completed and archived to {archived_filename}")

            # Log activity to Dashboard.md
            log_to_dashboard = project_root / "update_dashboard_activity_fixed.py"
            if log_to_dashboard.exists():
                try:
                    import subprocess
                    task_name = stem.replace('Plan_', '').replace('_', ' ')
                    subprocess.run([sys.executable, str(log_to_dashboard), f"Closed and archived plan: {task_name}"],
                                 check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    # If the skill script fails, log manually
                    with open(dashboard_path, 'a', encoding='utf-8') as f:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        task_name = stem.replace('Plan_', '').replace('_', ' ')
                        f.write(f"\n   - [{timestamp}] Closed and archived plan: {task_name}")
            else:
                # Manual logging if the skill script doesn't exist
                if dashboard_path.exists():
                    with open(dashboard_path, 'a', encoding='utf-8') as f:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        task_name = stem.replace('Plan_', '').replace('_', ' ')
                        f.write(f"\n   - [{timestamp}] Closed and archived plan: {task_name}")

            success_count += 1

        except PermissionError:
            print(f"Error: Permission denied when processing {plan_path}")
            continue
        except Exception as e:
            print(f"Error processing {plan_path}: {str(e)}")
            continue

    print(f"Successfully closed and archived {success_count} plan(s)")
    return True


def main():
    if len(sys.argv) > 1:
        plan_filename = sys.argv[1]
        close_plan_and_archive(plan_filename)
    else:
        close_plan_and_archive()


if __name__ == "__main__":
    main()