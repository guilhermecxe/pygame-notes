_next_id = 0


def new_entity():
    global _next_id
    _next_id += 1
    return _next_id
