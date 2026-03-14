def safe_exec(code: str, global_namespace: dict | None = None) -> tuple[bool, str]:
    if global_namespace is None:
        global_namespace = {}

    try:
        exec(code, global_namespace)
        return True, ""
    except Exception as e:
        return False, str(e)
