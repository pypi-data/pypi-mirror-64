import argparse

from stark.args import add_arguments
from stark.password import PasswordGen
from stark.validate import validate


# Create a custom help formatter class to disable  disaplying metavar in help message
# https://github.com/python/cpython/blob/master/Lib/argparse.py
class CustomFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            parts.extend(action.option_strings)
            return ", ".join(parts)


def main():
    # create parser
    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter,
        usage="stark [options]",
        description="stark generates random and strong passwords",
    )
    # add all arguments
    add_arguments(parser)
    args = parser.parse_args().__dict__
    # get the length of the password
    length = args.pop("length")
    # validate arguments
    validate(length, args, parser)
    # create PasswordGen object
    generator = PasswordGen(args, length)
    generator.create_map()
    # generate apssword
    password = generator.generate()
    print(password)


if __name__ == "__main__":
    main()
