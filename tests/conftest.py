import sys
import types
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

if "app" not in sys.modules:
    app_module = types.ModuleType("app")
    app_module.__path__ = [str(repo_root)]
    sys.modules["app"] = app_module
