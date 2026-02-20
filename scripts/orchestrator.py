#!/usr/bin/env python3
"""
Bronze Tier Orchestrator
Processes tasks from Needs_Action/ using AI Agent Skills logic.
"""

import sys
import time
from pathlib import Path
from datetime import datetime
import shutil
import re


class BronzeTierOrchestrator:
    """Orchestrates task processing using agent skills."""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.needs_action = self.project_root / "Needs_Action"
        self.done = self.project_root / "Done"
        self.plans = self.project_root / "Plans"
        self.dashboard = self.project_root / "Dashboard.md"

        # Ensure directories exist
        self.needs_action.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.plans.mkdir(exist_ok=True)

    def read_metadata(self, file_path):
        """Extract frontmatter metadata from a markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')

            # Extract frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    metadata = {}
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    return metadata
        except Exception as e:
            print(f"✗ Error reading metadata from {file_path.name}: {e}")

        return {}

    def create_plan(self, task_file):
        """Create a plan file for the given task (basic-file-handler skill logic)."""
        try:
            plan_name = f"Plan_{task_file.stem}.md"
            plan_path = self.plans / plan_name

            created_time = datetime.utcnow().isoformat() + 'Z'

            plan_content = f"""---
task: {task_file.name}
created: {created_time}
---
# Plan for {task_file.name}
- [ ] Review file content
- [ ] Decide action (archive / escalate)
- [ ] Move to Done/
- [ ] Log to Dashboard
"""

            plan_path.write_text(plan_content, encoding='utf-8')
            print(f"✓ Created plan: {plan_name}")
            return plan_name

        except Exception as e:
            print(f"✗ Error creating plan: {e}")
            return None

    def move_to_done(self, file_path):
        """Move file from Needs_Action to Done."""
        try:
            dest_path = self.done / file_path.name
            shutil.move(str(file_path), str(dest_path))
            print(f"✓ Moved to Done: {file_path.name}")
            return True
        except Exception as e:
            print(f"✗ Error moving file: {e}")
            return False

    def update_dashboard(self, message):
        """Append activity log to Dashboard.md."""
        try:
            if not self.dashboard.exists():
                # Create dashboard if it doesn't exist
                self.dashboard.write_text("# AI Employee Dashboard\n\n## Recent Activity\n", encoding='utf-8')

            content = self.dashboard.read_text(encoding='utf-8')

            # Find the Recent Activity section
            if "## Recent Activity" in content:
                timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                log_entry = f"   - [{timestamp}] {message}\n"

                # Insert after "## Recent Activity" line
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.strip() == "## Recent Activity":
                        new_lines.append(log_entry.rstrip())

                new_content = '\n'.join(new_lines)
                self.dashboard.write_text(new_content, encoding='utf-8')
                print(f"✓ Updated Dashboard: {message}")
                return True
            else:
                print("✗ Dashboard.md missing '## Recent Activity' section")
                return False

        except Exception as e:
            print(f"✗ Error updating dashboard: {e}")
            return False

    def process_file_drop(self, metadata_file):
        """Process a file_drop type task (task-analyzer + basic-file-handler logic)."""
        print(f"\n📋 Processing: {metadata_file.name}")

        metadata = self.read_metadata(metadata_file)

        if metadata.get('type') == 'file_drop':
            original_name = metadata.get('original_name', 'unknown')
            print(f"   Type: file_drop")
            print(f"   Original: {original_name}")

            # Create plan
            plan_name = self.create_plan(metadata_file)

            # Move to Done
            if self.move_to_done(metadata_file):
                # Update dashboard
                self.update_dashboard(f"Processed {metadata_file.name} → plan created, moved to Done")
                return True

        return False

    def scan_and_process(self):
        """Scan Needs_Action folder and process all pending tasks."""
        print("\n" + "=" * 60)
        print("Bronze Tier Orchestrator - Scanning for tasks...")
        print("=" * 60)

        # Find all .md files in Needs_Action
        md_files = list(self.needs_action.glob("*.md"))

        if not md_files:
            print("No tasks found in Needs_Action/")
            return 0

        print(f"Found {len(md_files)} task(s) to process\n")

        processed = 0
        for md_file in md_files:
            try:
                metadata = self.read_metadata(md_file)

                # Route to appropriate handler based on type
                if metadata.get('type') == 'file_drop':
                    if self.process_file_drop(md_file):
                        processed += 1
                else:
                    # Generic handler for other types
                    print(f"\n📋 Processing: {md_file.name}")
                    plan_name = self.create_plan(md_file)
                    if self.move_to_done(md_file):
                        self.update_dashboard(f"Processed {md_file.name} → plan created, moved to Done")
                        processed += 1

            except Exception as e:
                print(f"✗ Error processing {md_file.name}: {e}")

        print(f"\n{'=' * 60}")
        print(f"✓ Processed {processed}/{len(md_files)} tasks successfully")
        print("=" * 60)

        return processed

    def run_loop(self, interval=60):
        """Run orchestrator in continuous loop."""
        print("Starting orchestrator in loop mode (Ctrl+C to stop)")
        print(f"Checking every {interval} seconds...\n")

        try:
            while True:
                self.scan_and_process()
                print(f"\nWaiting {interval} seconds...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nStopping orchestrator...")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent if Path(__file__).parent.name == "scripts" else Path(__file__).parent

    orchestrator = BronzeTierOrchestrator(project_root)

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        orchestrator.run_loop(interval)
    else:
        # Single run mode
        orchestrator.scan_and_process()


if __name__ == "__main__":
    main()
