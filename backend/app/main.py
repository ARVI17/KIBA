from backend.app.config import create_app
import os


app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["1", "true", "t", "yes"]
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
