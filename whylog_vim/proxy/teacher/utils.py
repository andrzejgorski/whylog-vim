from functools import partial
from itertools import count

get_next_parser_id = partial(next, count(0))
get_next_constraints_id = partial(next, count(0))
