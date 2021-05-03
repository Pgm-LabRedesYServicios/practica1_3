from typing import List


class Petition:
    """
    Parses a petition string into this object
    """
    method: str
    arguments: List[str]
    keep_alive: bool

    def __init__(self, data: str):
        headers = data.split('\r\n')
        headers = list(filter(lambda x: x.strip() != '', headers))
        header_map = {}

        method = headers.pop(0).split(' ')

        self.method = method.pop(0)
        self.arguments = method

        for header in headers:
            kv = header.split(' ')
            key = kv.pop(0)
            key = list(key)
            key.pop(-1)
            key = str(key)

            header_map[key] = kv

        self.header_map = header_map

        try:
            header_map['Keep-Alive']
            self.keep_alive = True
        except KeyError:
            self.keep_alive = False
