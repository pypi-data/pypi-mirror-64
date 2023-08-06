
def bytes_to_hex(bytes_string, max_chars=None):
    suffix = ""
    if max_chars is not None and max_chars < len(bytes_string):
        suffix = "..."
    bytes_string = bytes_string[0:max_chars]
    result = " ".join(["%02x" % x for x in bytes_string])
    return result + suffix
