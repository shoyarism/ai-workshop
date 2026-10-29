"""
Workshop OS Central CLI entrypoint.
"""
from scripts.workshop import main, build_parser

__all__ = ["main", "build_parser"]

if __name__ == "__main__":
    main()
