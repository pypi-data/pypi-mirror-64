def read_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value == 0:
            return False
        if value == 1:
            return True
    if isinstance(value, str):
        if value in ('true', 't', 'True', 'T', 'Y', 'y'):
            return True
        if value in ('false', 'f', 'False', 'F', 'N', 'n'):
            return False
    raise ValueError(f'Could not convert {repr(value)} to bool')


def read_list(value, split_char: str = None) -> list:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        if split_char is not None:
            if value.startswith(split_char) is False:
                out = value.split(split_char)
                if value.endswith(split_char) is True:
                    out.pop(-1)
                return out
    raise ValueError(f'Could not convert {repr(value)} to list')


def read_str(value):
    if isinstance(value, str):
        return value
    raise ValueError(f'Could not convert {repr(value)} to str')
