def sumValues(dict):
    """Return the sum of int values of a dict."""
    result = 0
    for value in dict.values():
        if type(value) == int:
            result += value
    return result


def validate(length, args, parser):
    # check if the sum of the length of each type exceeds the password length
    if length and sumValues(args) > length:
        parser.error("password length exceeded")
    # check if password length is not specified there is a type with no specified length
    if not length and any(type(value) == bool for value in args.values()):
        parser.error("length not specified")
