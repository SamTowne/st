# st
notes, workspaces, and helpful commands.

- [.workspace](./workspace), workspaces for building, testing, learning
- [brain](./brain/), older notes
- the .gitignore is aggresive, to add someting new, exclude it from the wild card ignore like `!my_file.sh`

### New workspace
`make workspace my-workspace` or `python make_workspace.py my-workspace`

### Setup
- Please install the githooks to reduce risk before pushing to the git remote
```sh
pip install -r requirements.txt
pre-commit install
```

### Adding new requirements
- Add to requirements.in
- Run `pip-compile requirements.in`
- This ensures all dependencies (including sub-dependencies) are pinned for reproducible installs.
- Only packages listed in requirements.in will be included; packages installed directly into the .venv will not be captured unless added to requirements.in
