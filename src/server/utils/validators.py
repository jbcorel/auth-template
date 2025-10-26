def empty_string_to_none[T](value: T) -> T | None:
    if isinstance(value, str) and value == "":
        return None
    return value
