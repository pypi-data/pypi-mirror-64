import argparse

def positive(value):
    """Check if argument provided is a positive int."""
    try:
        value = int(value)
    except:
        raise argparse.ArgumentTypeError("must be of type int")

    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")

    return value


def add_arguments(parser):
    parser.add_argument(
        "-ln",
        "--length",
        type=positive,
        help="password length"
        )
    parser.add_argument(
        "-a",
        "--any",
        const=True,
        nargs="?",
        type=positive,
        help="include any character",
    )
    parser.add_argument(
        "-l",
        "--lowercase",
        const=True,
        nargs="?",
        type=positive,
        help="include lowercase",
    )
    parser.add_argument(
        "-u",
        "--uppercase",
        const=True,
        nargs="?",
        type=positive,
        help="include uppercase",
    )
    parser.add_argument(
        "-d",
        "--digits",
        const=True,
        nargs="?",
        type=positive,
        help="include digits"
    )
    parser.add_argument(
        "-s",
        "--symbols",
        const=True,
        nargs="?",
        type=positive,
        help="include symbols"
    )
    parser.add_argument(
        "-x",
        "--hexdigits",
        const=True,
        nargs="?",
        type=positive,
        help="include hexadecimal",
    )
    parser.add_argument(
        "-an",
        "--alphanumeric",
        const=True,
        nargs="?",
        type=positive,
        help="include alphanumeric",
    )
    parser.add_argument(
        "-lt",
        "--letters",
        const=True,
        nargs="?",
        type=positive,
        help="include letters"
    )

