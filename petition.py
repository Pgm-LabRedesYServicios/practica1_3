from typing import List

class Petition:
    method: str
    arguments: List[str]
    keep_alive: bool

    def __init__(self, data: str):
        headers = data.split('\n\r')
        headers = list(filter(lambda x: x.strip() != '', headers))
        header_map = {}

        method = headers.pop(0).split(' ')

        self.method = method.pop(0)
        self.arguments = method

        for header in headers:
            kv = header.split(' ')
            key = kv.pop(0)
            
            header_map[key] = kv

        self.header_map = header_map
