from requests import get, Response, RequestException
from json import loads

from Logger import Logger
from cfg import API_PATH

class ApiManager():
    @classmethod
    def __sendRequest(cls, addr: str):
        try:
            resp = get(url=addr, timeout=10)
        except RequestException as e:
            Logger.printLog(f"{e}", error=True)
            return False
        if not resp.ok:
            return False

        return loads(resp.text.encode('utf8'))
    @classmethod
    def getOnlineList(cls, ip: str, port: str):
        addr = 'http://' + ip + ':' + port + API_PATH
        return cls.__sendRequest(addr)