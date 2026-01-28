import os
import sys

# Allow running directly (python backend/src/app.py)
if __name__ == "__main__":
    # Add project root to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    sys.path.append(project_root)

try:
    from backend.src.create_app import create_app
except ImportError:
    # Fallback for relative import if run as module
    from .create_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
