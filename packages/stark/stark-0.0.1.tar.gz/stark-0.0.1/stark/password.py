import random
import secrets
import string


def filterDict(filter, dict):
    """Return a dictionary with items for which filter(item) is False."""
    result = {}
    for key, value in dict.items():
        if not filter(key, value):
            result[key] = value
    return result


def filterString(filter, str):
    """Return a string with characters for which filter(char) is False."""
    result = ""
    for i in range(len(str)):
        if not filter(str[i]):
            result += str[i]
    return result


def valueNone(key, value):
    """Check if a dictionary value is None."""
    return value == None


def valueNotInt(key, value):
    """Check if a dictionary value is not int."""
    return type(value) != int


def valueInt(key, value):
    """Check if a dictionary value is int."""
    return type(value) == int


def shuffle(s):
    """Return a randomly shuffled version of string s."""
    s = list(s)
    random.shuffle(s)
    return "".join(s)


def pick(source, n):
    """Return a string with n randomly picked characters source string."""
    return "".join(secrets.choice(source) for i in range(n))


def random_partition(keys, p):
    """Return a dict with keys such that values are a random partition of p.

    Parameters:
    ----------
    keys : list of str
    p : int

    Notes:
    -----
    each value of the dict should be greater than or equals one

    Example:
    ---------
    >>> partition(['alphanumeric','hexdigits','symbols'],7)
    {'alphanumeric': 1, 'hexdigits': 2, 'symbols': 4}
    """
    n = len(keys)
    # each key should at least have one character
    values = [1] * n
    p -= n
    for _ in range(p):
        i = secrets.randbelow(n)
        values[i] += 1
    result = {keys[i]: values[i] for i in range(n)}
    return result


def sumValues(dict):
    """Return the sum of int values of a dict."""
    result = 0
    for value in dict.values():
        if type(value) == int:
            result += value
    return result


class PasswordGen:
    def __init__(self, args, length):
        self.args = filterDict(valueNone, args)
        self.sum = sumValues(self.args)
        # The sum of the length of types provided
        # Example : generate -l 10 -u 5 -d 7 --> self.sum = 10 + 5 + 7 = 22
        self.length = length or self.sum
        # If the password length is not privded then it will have the value of self.sum
        self.rest = self.length - self.sum
        self.empty = list(filterDict(valueInt, self.args).keys())
        self.is_default = self.args == dict()
        # Default password settings
        self.default_type = "alphanumeric"
        self.default_length = self.length or 25
        self.type = {
            "lowercase": string.ascii_lowercase,
            "uppercase": string.ascii_uppercase,
            "digits": string.digits,
            "symbols": string.punctuation,
            "letters": string.ascii_letters,
            "alphanumeric": string.ascii_letters + string.digits,
            "hexdigits": string.hexdigits,
            "any": string.ascii_letters + string.digits + string.punctuation,
        }

    def create_map(self):
        """Create a map for the password.

        if the password length is not provided and no options are provided generate a password with default settings.
        if the password length is provided while the sum of the lengths of each type provided is less than the password length, complete the rest with a default password.
        if the length of each type is provided, the password length is optional.
        """
        if self.is_default:
            self.args = {self.default_type: self.default_length}
        else:
            if self.empty == []:
                self.args[self.default_type] = self.rest
            else:
                partition = random_partition(self.empty, self.rest)
                # merge the partition with self.args
                self.args.update(partition)

        self.map = {self.type[key]: value for key, value in self.args.items()}

    def generate(self):
        """Generate a random password from a map of strings."""
        result = ""
        for key, value in self.map.items():
            result += pick(key, value)
        return shuffle(result)
