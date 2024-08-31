#import redis
import datetime

class Memory:
    def __init__(self) -> None:
        self.data = {}

    def set(self, id:str, data: str, ex:int):
        self.data[id] = {
            'data': data,
            'ex': ex,
            'created': datetime.datetime.now()
        }


    def get(self, id:str):
        self.clear_memory()
        return self.data[id]['data']


    def is_expired(self, data) -> bool:
        spend = datetime.datetime.now() - data['created']
        if spend.seconds > data['ex']: return True
        return False

    def clear_memory(self):
        keys = []
        for k in self.data.keys():
            if self.is_expired(self.data[k]):
                keys.append(k)
        for k in keys:
            del self.data[k]


memory = Memory()


#memory = redis.Redis(host='localhost', port=6379, db=0)
