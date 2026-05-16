"""
metronome_main.py
-----------------
Entry point for the configurable metronome.

Usage
-----
  python main.py                     # uses config.json
  python main.py my_config.json      # custom config path
"""

import sys
import json
import logging
from pathlib import Path
from player import MetronomePlayer

DEFAULT_CONFIG = "config.json"


def load_config(path: str) -> dict:
    """Load and return JSON config; exit with message on failure."""
    config_path = Path(path)
    if not config_path.exists():
        logging.error("Config file not found: {config_path}")
        sys.exit(1)
    with config_path.open() as file:
        return json.load(file)


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG
    config = load_config(config_path)

    logging.info(f"Loaded config     : {config_path}")
    logging.info(f"Beat file         : {config.get('beat_file', '<not set>')}")
    logging.info(f"BPM amplitude     : ±{config.get('bpm_amplitude', 0)}")
    logging.info(f"Duration amplitude: ±{config.get('duration_amplitude', 0)} min")
    logging.info(f"Segments          : {len(config.get('segments', []))}")
    for i, seg in enumerate(config.get("segments", []), start=1):
        logging.info(f"  [{i}] {seg['duration_minutes']} min - {seg['bpm']} BPM")

    player = MetronomePlayer(config)
    player.run()


if __name__ == "__main__":
    main()
