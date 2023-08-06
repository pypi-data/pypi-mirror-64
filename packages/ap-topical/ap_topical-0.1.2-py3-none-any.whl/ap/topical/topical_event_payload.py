from uuid import uuid4
import copy
import datetime

class TopicalEventPayload:
    def __init__(self):
        self.__idempotency_token = uuid4()

        self.__created = datetime.datetime.now()
        self.__access_log = []

        self.__metadata = {}

    @property
    def idempotency_token(self):
        return self.__idempotency_token

    @property
    def audit_log(self):
        return self.__access_log

    def set_metadata(self, key, value):
        self.__metadata[key] = value

    def get_metadata(self, key, default=None):
        return self.__metadata.get(key, default)

    def access_by(self, target):
        self.__access_log.append(datetime.datetime.now(), target)

    def todict(self):
        return {
            'idempotency_token': self.idempotency_token,
            'created_on': self.__created,
            'audit_log': self.audit_log,
            'metadata': self.__metadata,
        }
