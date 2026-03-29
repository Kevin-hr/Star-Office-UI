#!/usr/bin/env python3
"""Star Office UI - Backend State Service"""

from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import json
import os

# Paths - fixed!
# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
STATE_FILE = os.path.join(ROOT_DIR, "workspace", "state.json")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/static")

# Default state
DEFAULT_STATE = {
    "state": "idle",
    "detail": "等待任务中...",
    "progress": 0,
    "updated_at": datetime.now().isoformat()
}


def load_state():
    """Load state from file"""
    state = None
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = None

    if not isinstance(state, dict):
        state = dict(DEFAULT_STATE)

    return state


def save_state(state: dict):
    """Save state to file"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# Initialize state
if not os.path.exists(STATE_FILE):
    save_state(DEFAULT_STATE)


@app.route("/", methods=["GET"])
def index():
    """Serve the pixel office UI"""
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/shadowfiend.png", methods=["GET"])
def shadowfiend_icon():
    """Serve the hero icon directly"""
    return send_from_directory(FRONTEND_DIR, "shadowfiend.png")


@app.route("/status", methods=["GET"])
def get_status():
    """Get current state"""
    state = load_state()
    return jsonify(state)



@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    print("=" * 50)
    print("Star Office UI - Backend State Service")
    print("=" * 50)
    print(f"State file: {STATE_FILE}")
    print(f"Frontend: {FRONTEND_DIR}")
    print("Listening on: http://0.0.0.0:18888")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=18888, debug=False)
