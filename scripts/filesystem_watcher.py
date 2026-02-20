#!/usr/bin/env python3
"""
Bronze Tier Filesystem Watcher
Monitors Inbox/ folder and processes new files automatically.
"""

import sys
import time
from pathlib import Path
from datetime import datetime
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class InboxFileHandler(FileSystemEventHandler):
    """Handles new file events in the Inbox folder."""

    def __init__(self, inbox_path, needs_action_path):
        self.inbox_path = Path(inbox_path)
        self.needs_action_path = Path(needs_action_path)
        self.needs_action_path.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        """Called when a file is created in the watched directory."""
        if event.is_directory:
            return

        source_path = Path(event.src_path)

        # Ignore temporary files and metadata files
        if source_path.name.startswith('.') or source_path.suffix == '.tmp':
            return

        try:
            # Wait a moment to ensure file is fully written
            time.sleep(0.5)

            # Get file info
            original_name = source_path.name
            file_size = source_path.stat().st_size
            detected_time = datetime.utcnow().isoformat() + 'Z'

            # Copy file to Needs_Action with FILE_ prefix
            dest_filename = f"FILE_{original_name}"
            dest_path = self.needs_action_path / dest_filename

            shutil.copy2(source_path, dest_path)
            print(f"✓ Copied: {original_name} -> {dest_filename}")

            # Create metadata file
            metadata_filename = f"FILE_{original_name}.md"
            metadata_path = self.needs_action_path / metadata_filename

            metadata_content = f"""---
type: file_drop
original_name: {original_name}
size_bytes: {file_size}
detected_at: {detected_time}
status: pending
---
## Dropped File
Original: {original_name}
Copied to: {dest_filename}

New item ready for processing.
"""

            metadata_path.write_text(metadata_content, encoding='utf-8')
            print(f"✓ Created metadata: {metadata_filename}")

        except Exception as e:
            print(f"✗ Error processing {source_path.name}: {e}", file=sys.stderr)


def main():
    """Main entry point for the filesystem watcher."""
    # Get paths relative to script location
    script_dir = Path(__file__).parent.parent
    inbox_path = script_dir / "Inbox"
    needs_action_path = script_dir / "Needs_Action"

    # Ensure Inbox exists
    inbox_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Bronze Tier Filesystem Watcher")
    print("=" * 60)
    print(f"Watching: {inbox_path.absolute()}")
    print(f"Output:   {needs_action_path.absolute()}")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    # Set up watchdog observer
    event_handler = InboxFileHandler(inbox_path, needs_action_path)
    observer = Observer()
    observer.schedule(event_handler, str(inbox_path), recursive=False)

    try:
        observer.start()
        print("✓ Watcher started successfully\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping watcher...")
        observer.stop()

    observer.join()
    print("✓ Watcher stopped")


if __name__ == "__main__":
    main()
