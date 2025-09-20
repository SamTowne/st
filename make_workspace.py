import sys
from datetime import datetime
from pathlib import Path

# Accept optional input
suffix = sys.argv[1] if len(sys.argv) > 1 else ""
date_str = datetime.now().strftime("%Y%m%d")

if suffix:
    title = f"{date_str}-{suffix}"
else:
    title = date_str

dir_name = f".workspace/{title}"
notes_path = Path(dir_name) / "notes.md"

# Create directory and notes.md
notes_path.parent.mkdir(parents=True, exist_ok=True)
notes_path.touch(exist_ok=True)

# Write the title as a Markdown heading in notes.md
with notes_path.open("w") as f:
    f.write(f"# {title}\n")

# Print the created dir and filename for quick access in IDE
print(f"Created: {notes_path.resolve()}")