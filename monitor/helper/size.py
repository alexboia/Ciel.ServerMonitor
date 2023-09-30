import re
import math

DEFAULT_SIZE_SPEC = '0'
DEFAULT_UNIT_SPEC = 'B'
VALID_SIZE_REGEX = '^(?P<sizespec>[0-9]+)(?P<unitspec>(B|K|M|G))?$'

VALID_SIZE_UNIT_EXPONENTS = {
    'B': 0,
    'K': 1,
    'M': 2,
    'G': 3
}

def strtoint_byte_size(str_byte_size:str):
    if str_byte_size is None:
        return 0;

    match = re.search(VALID_SIZE_REGEX, str_byte_size)
    if match is None:
        return 0

    size_spec = match.group('sizespec') or DEFAULT_SIZE_SPEC
    unit_spec = match.group('unitspec') or DEFAULT_UNIT_SPEC
    unit_exp = VALID_SIZE_UNIT_EXPONENTS.get(unit_spec) or 0

    return int(size_spec) * math.pow(1024, unit_exp)