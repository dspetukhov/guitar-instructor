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
    """
    Load and return JSON config; exit on failure.
    """
    config_path = Path(path)
    if not config_path.exists():
        logging.error("Config file not found: {config_path}")
        sys.exit(1)
    with config_path.open() as file:
        config = json.load(file)
    return config


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG
    config = load_config(config_path)

    logging.info(f"Loaded config     : {config_path}")
    logging.info(f"Beat file         : {config.get('beat_file', '<not set>')}")
    logging.info(f"BPM amplitude     : ±{config.get('bpm_amplitude', 0)}")
    logging.info(f"Duration amplitude: ±{config.get('duration_amplitude', 0)} min")
    if config.get("segments"):
        logging.info(f"Segments          : {len(config['segments'])}")
        for i, seg in enumerate(config.get("segments", []), start=1):
            if seg.get("bpm", 0) <= 0:
                logging.warning(
                    f"Segment {i}: bpm must be > 0 (got {seg.get('bpm')})"
                )
                continue
            if seg.get("duration_minutes", 0) <= 0:
                logging.warning(
                    f"Segment {i}: duration_minutes must be > 0 "
                    f"(got {seg.get('duration_minutes')})"
                )
                continue

            logging.info(f"  [{i}] {seg['duration_minutes']} min - {seg['bpm']} BPM")
    else:
        raise ValueError("segments aren't specified - nothing to play")

    player = MetronomePlayer(config)
    player.run()


if __name__ == "__main__":
    main()
