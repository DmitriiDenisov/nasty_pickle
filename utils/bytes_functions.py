# UTILITY FUNCTIONS TO BUILD OPCODES


def _unicode_op(string: str) -> bytes:
    """Put string into stack"""
    try:
        hexlen = bytes([len(string)])
    except ValueError:
        hexlen = None
    if hexlen is None or len(hexlen) > 4:
        return b"V" + string.encode("utf8") + b"\n"
    if len(hexlen) == 1:
        return b"\x8c" + hexlen + string.encode("utf8")
    elif len(hexlen) < 5:
        return b"X" + hexlen + string.encode("utf8")


def _import_op(module, attr, attr_reversed=False) -> bytes:
    """Import module.attr and put it into stack"""
    return b"".join([
        _unicode_op(module),
        _unicode_op(attr) if not attr_reversed else _reversed_unicode_op(attr),
        b"\x93"
    ])


def _import_builtin(attr) -> bytes:
    """Put builtin attr into stack"""
    return _import_op("builtins", attr)


def _tuple(*args) -> bytes:
    """Put tuple of args into stack"""
    return b"(" + b"".join(args) + b"t"


def _reversed_unicode_op(string: str) -> bytes:
    """Put string into stack so that it will be reversed in bytestream
    builtins.exec("{string}[::-1]")
                 str.__add__({string}, "[::-1]")
                 builtins.getattr(builtins.str, "__add__")"""
    rev_string_op = _unicode_op("\"{}\"".format(string[::-1]))
    return b"".join([
        _import_builtin("eval"),
        _tuple(
            _import_builtin("getattr"),
            _tuple(_import_builtin("str"), _unicode_op("__add__")),
            b"R",
            _tuple(rev_string_op, _unicode_op("[::-1]")),
            b"R"
        ),
        b"R"
    ])
