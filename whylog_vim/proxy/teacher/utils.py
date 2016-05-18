from functools import partial


def naturals_generator():
    i = 0
    while True:
        yield i
        i += 1


parser_ids = naturals_generator()
get_next_parser_id = partial(next, parser_ids)
constraint_ids = naturals_generator()
get_next_constraints_id = partial(next, constraint_ids)
