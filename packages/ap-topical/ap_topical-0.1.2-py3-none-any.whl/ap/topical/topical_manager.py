import asyncio
from collections import defaultdict

class TopicalManager:
    def __init__(self):
        self.__event_map = defaultdict(list)

    def subscribe(self, event, callback):
        self.__event_map[event].append(callback)

    def subscribe_many(self, mapping):
        [self.subscribe(e, c) for e, c in mapping.items()]

    def publish(self, event, payload):
        [callback(payload) for callback in self.__event_map[event] if not asyncio.iscoroutinefunction(callback)]

    async def publish_async(self, event, payload):
        [await callback(payload) for callback in self.__event_map[event] if asyncio.iscoroutinefunction(callback)]
