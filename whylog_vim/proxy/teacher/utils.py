from functools import partial
from itertools import count


parser_ids = count(0)
get_next_parser_id = partial(next, parser_ids)
constraint_ids = count()
get_next_constraints_id = partial(next, constraint_ids)
