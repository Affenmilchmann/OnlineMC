from datetime import datetime as dt

class Logger():
    @classmethod
    def __getTimeStamp(cls):
        return '{:%Y-%m-%d %H:%M:%S}'.format(dt.now())
    @classmethod
    def printLog(cls, text, error=False):
        if error:
            print(f"[{cls.__getTimeStamp()}] [ERROR] {text}")
        else:
            print(f"[{cls.__getTimeStamp()}] {text}")