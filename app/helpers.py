from pathlib import Path


def getProjectRoot() -> Path:
    return Path(__file__).parent
