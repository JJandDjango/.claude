"""Entry point for running as a module: python -m prompt_lang"""

import sys

from .validate import main

if __name__ == "__main__":
    sys.exit(main())
