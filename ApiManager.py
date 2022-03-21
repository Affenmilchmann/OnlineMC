from requests import get, Response, RequestException
from json import loads

from Logger import Logger
from cfg import API_PATH, TIMEOUT

class ApiManager():
    @classmethod
    def __sendRequest(cls, addr: str):
        try:
            resp = get(url=addr, timeout=TIMEOUT)
        except RequestException as e:
            Logger.writeApiFatalLog(f"{e}")
            return False
        if not resp.ok:
            Logger.writeApiFatalLog(f"[NOT OK] {resp.url} {resp.content}")
            return False

        return loads(resp.text.encode('utf8'))
    @classmethod
    def getOnlineList(cls, ip: str, port: str):
        addr = 'http://' + ip + ':' + port + API_PATH
        return cls.__sendRequest(addr)