"""
Compatibility shim for Python 3.13+ where stdlib imghdr was removed.
Only implements what() used by third-party dependencies.
"""


def what(file=None, h=None):
    if h is None:
        if file is None:
            return None
        with open(file, "rb") as fp:
            h = fp.read(32)
    else:
        h = h[:32]

    if h.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if h[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if h[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if h.startswith(b"BM"):
        return "bmp"
    if h[:4] == b"RIFF" and h[8:12] == b"WEBP":
        return "webp"
    if h[:2] in (b"II", b"MM") and h[2:4] in (b"\x2a\x00", b"\x00\x2a"):
        return "tiff"
    return None
