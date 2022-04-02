def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
