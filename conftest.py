"""Root conftest.py for pytest.

Ensures the examples package is importable from tests.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
