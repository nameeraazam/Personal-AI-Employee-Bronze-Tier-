#!/usr/bin/env python3
"""
File system watcher for AI Employee Bronze Tier
Monitors the Inbox folder and creates task files in Needs_Action when new files are detected.
"""

import time
import logging
from datetime import datetime
from pathlib import Path
import shutil
from zoneinfo import ZoneInfo  # Python 3.9+
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InboxHandler:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.inbox_dir = project_root / "Inbox"
        self.needs_action_dir = project_root / "Needs_Action"

        # Create directories if they don't exist
        self.needs_action_dir.mkdir(exist_ok=True)
        self.inbox_dir.mkdir(exist_ok=True)

        # Import watchdog here to handle the case where it's not installed
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            self.Observer = Observer
            self.FileSystemEventHandler = FileSystemEventHandler
        except ImportError:
            logger.error("watchdog library is not installed. Please install it with: pip install watchdog")
            raise

    def on_file_created_or_moved(self, file_path: Path):
        """Process a new file that was created or moved into Inbox."""
        try:
            # Only process files that are in the Inbox directory
            if self.inbox_dir not in file_path.parents and file_path.parent != self.inbox_dir:
                return

            original_name = file_path.name
            logger.info(f"Detected new file: Inbox/{original_name}")

            # Get file size
            try:
                size_bytes = file_path.stat().st_size
            except OSError as e:
                logger.error(f"Could not get file size for {file_path}: {e}")
                return

            # Generate timestamp in Asia/Karachi timezone
            try:
                karachi_tz = ZoneInfo("Asia/Karachi")
                detected_at = datetime.now(karachi_tz).strftime("%Y-%m-%dT%H:%M:%S+05:00")
            except Exception:
                # Fallback to UTC if timezone is not available
                detected_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

            # Create new filename with FILE_ prefix
            new_filename = f"FILE_{original_name}"
            new_file_path = self.needs_action_dir / new_filename

            # Copy the original file to Needs_Action/
            try:
                shutil.copy2(file_path, new_file_path)
                logger.info(f"Copied original file to Needs_Action/{new_filename}")
            except FileExistsError:
                logger.warning(f"File already exists: {new_file_path}")
                # Add a number suffix to make it unique
                counter = 1
                base_name = new_filename.rsplit('.', 1)[0] if '.' in new_filename else new_filename
                extension = f".{new_filename.split('.', 1)[1]}" if '.' in new_filename else ""

                while new_file_path.exists():
                    new_filename = f"{base_name}_{counter}{extension}"
                    new_file_path = self.needs_action_dir / new_filename
                    counter += 1

                shutil.copy2(file_path, new_file_path)
                logger.info(f"Copied original file to Needs_Action/{new_filename} (with unique name)")
            except PermissionError:
                logger.error(f"Permission denied when copying {file_path} to {new_file_path}")
                return
            except Exception as e:
                logger.error(f"Error copying {file_path} to {new_file_path}: {e}")
                return

            # Create the companion metadata file
            metadata_content = f"""---
type: file_drop
original_name: {original_name}
size_bytes: {size_bytes}
detected_at: {detected_at}
status: pending
---

## Dropped File
Original filename: {original_name}
Copied to: {new_filename}

New item ready for AI agent processing.
"""

            metadata_file_path = self.needs_action_dir / f"{new_filename}.md"
            try:
                with open(metadata_file_path, 'w', encoding='utf-8') as f:
                    f.write(metadata_content)
                logger.info(f"Created task: Needs_Action/{new_filename}.md")
            except PermissionError:
                logger.error(f"Permission denied when creating metadata file: {metadata_file_path}")
            except Exception as e:
                logger.error(f"Error creating metadata file {metadata_file_path}: {e}")

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

    def run(self):
        """Start the file system watcher."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class Handler(FileSystemEventHandler):
            def __init__(self, inbox_handler):
                self.inbox_handler = inbox_handler

            def on_created(self, event):
                if event.is_directory:
                    return
                file_path = Path(event.src_path)
                self.inbox_handler.on_file_created_or_moved(file_path)

            def on_moved(self, event):
                if event.is_directory:
                    return
                # Check if the destination is in the Inbox directory
                dest_path = Path(event.dest_path)
                if self.inbox_handler.inbox_dir in dest_path.parents or dest_path.parent == self.inbox_handler.inbox_dir:
                    self.inbox_handler.on_file_created_or_moved(dest_path)

        event_handler = Handler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.inbox_dir), recursive=False)

        logger.info(f"Starting file system watcher for {self.inbox_dir}")
        logger.info("Watching for new files in Inbox folder...")

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping file system watcher...")
            observer.stop()
        observer.join()


def main():
    project_root = Path.cwd()
    watcher = InboxHandler(project_root)
    watcher.run()


if __name__ == "__main__":
    main()