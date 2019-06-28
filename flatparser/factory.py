from abc import ABCMeta, abstractmethod
import datetime


class CustomValidation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self, field):
        pass


class DateCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            datetime.datetime.strptime(field, '%d/%m/%Y')
            return True
        except Exception:
            return False
