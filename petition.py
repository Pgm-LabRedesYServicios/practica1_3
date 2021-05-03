class Petition:
    method: str
    keep_alive: bool

    def __init__(data: str):
        headers = data.split('\r\n')
        header_map = {}

        for header in headers:
            kv = header.split(' ')
            key = kv.pop(0)
            
            header_map[key] = kv
    
        self.method

