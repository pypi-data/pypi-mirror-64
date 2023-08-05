from pathlib import Path


def create(*args):
    """Function that creates multiple directories."""
    if args:
        for directory in args:
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
        return True
    return
