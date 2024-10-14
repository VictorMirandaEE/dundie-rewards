import argparse


def load(filepath: str):
    """Loads data from filepath to the database

    Args:
        filepath (str): path to the employees file
    """
    try:
        with open(filepath) as file:
            for line in file:
                print(line)
    except FileNotFoundError as msg:
        print(f"File not found {msg}")


subcommands = {
    "load": load,
}


def main():
    parser = argparse.ArgumentParser(
        description="Dunder Mifflin Rewards CLI",
        epilog="Enjoy and use with caution.",
    )
    parser.add_argument(
        "subcommand",
        type=str,
        help="The subcommand to run",
        choices=("load", "show", "send", "add"),
        default="help",
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="File path to load",
        default=None,
    )
    args = parser.parse_args()

    globals()[args.subcommand](args.filepath)


if __name__ == "__main__":
    main()
