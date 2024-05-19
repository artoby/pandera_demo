import re
from typing import Tuple, Union

SYMBOL_PARSE_PATTERN = re.compile(r"""^t?(?P<sym1>[^:]*):?(?P<sym2>(USD|USDT))$""", re.VERBOSE)


def extract_pair_symbols(text: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    sym1 = None
    sym2 = None

    match = SYMBOL_PARSE_PATTERN.match(text)
    if match is not None:
        sym1 = match.group('sym1')
        sym2 = match.group('sym2')
    return sym1, sym2
