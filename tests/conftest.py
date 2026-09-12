# tests/conftest.py
import sys
import os

# Ensure the project root (the directory that contains the `backend` package)
# is on PYTHONPATH when pytest runs.
project_root = os.path.abspath(os.path.join(__file__, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)