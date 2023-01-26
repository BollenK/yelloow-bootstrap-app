from abc import ABC
from datetime import datetime


class IKPI(ABC):
    def get_data(self, from_dt: datetime, till_dt: datetime):
        ...

    def set_schedule(self):
        ...  # maybe remove this here and add to seperate interface Schedulee # noqa

    def transform_data(self, data):
        ...
