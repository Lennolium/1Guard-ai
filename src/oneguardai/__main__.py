#!/usr/bin/env python3

"""
__main__.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__build__ = "2023.1"
__date__ = "2023-11-07"
__status__ = "Prototype"

# Imports.
import argparse


def main():
    # Create argument parser for interactive shell.
    parser = argparse.ArgumentParser(
            prog="1Guard-ai",
            description=f"1Guard-ai v{__version__} ({__build__})\n\n"
                        "AI-Model for evaluating the trustworthiness"
                        "of a shopping website.",
            epilog="For more information: "
                   "https://github.com/Lennolium/1Guard-ai",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    # CLI argument.
    parser.add_argument(
            "-c", "--cli", action="store_true",
            help="starts in CLI mode (default)"
            )

    # Parse arguments.
    args = parser.parse_args()

    # Start GUI: We just import the GUI here, because it adds a lot of
    # dependencies, and the CLI should be as lightweight as possible.
    if args.cli:
        pass
        # TODO: Implement here the starting of model.


if __name__ == "__main__":
    main()
