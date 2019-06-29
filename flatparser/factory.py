from abc import ABCMeta, abstractmethod
import datetime
from .fs import read_file
from .models import UniqueWithin30daysEntity, UniqueEntity, DistinctEntity
import datetime
from django.db.models import Q


class CustomValidation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self, field):
        pass


# Validate Number format
# receives the field
# returns True if is number
#         False if is not number
class NumberCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            # trying to parse number as int
            # in python 3 int has unlimited size
            num = int(field)
            # If it is mandatory, so must be greater then zero
            if num > 0: 
                return True

            return False
        except Exception:
            return False


# Validate Text format
# receives the field
# returns True if is not empty
#         False if is empty
class TextCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            # for text string is enough to test it 
            # if is false (or empty)
            if field: 
                return True

            return False
        except Exception:
            return False


# Validate Date format DDMMYYYY
# receives the field
# returns True if date is valid
#         False if date is invalid
class DateCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            datetime.datetime.strptime(field, '%d%m%Y')
            return True
        except Exception:
            return False


# Validate is there is not field within last 30 days
# receives the field
# returns True if there is not found field
#         False if field were found
class UniqueWithin30daysCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            # back 30 days in the past
            data_limite = datetime.datetime.now() - datetime.timedelta(days=30)
            
            # search for field where date_created 
            # greater than or equal to 30 days old
            newer = UniqueWithin30daysEntity.objects.filter(field=field, 
                                                        date_created__gte=data_limite).first()
            
            # check if there is a field in the database
            if newer is None:
                # register the field in the database
                # to avoid be used within 30 days
                burned = UniqueWithin30daysEntity(field=field)
                burned.save()

                # if there isn't, return True,
                # meaning that is ok to create one
                return True

            # otherwise if there is already a field
            # within last 30 days, the validation fails
            return False
        except Exception as e:
            # print(str(e))
            return False


# Validate Unique format
# receives the field
# returns True if is Unique
#         False if is not Unique
class UniqueCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            # checking if it is unique against the database
            unique = UniqueEntity.objects.find(field=field).first()
            if unique is None:
                return True

            return False
        except Exception:
            return False


# Validate Length of 16 or greater format
# receives the field
# returns True if length is 16 at least
#         False if length is lesser than 16
class GreaterThanOrEqualTo16CustomValidation(CustomValidation):
    def validate(self, field):
        try:
            # checking if it has 16 digits at least
            return len(str(int(field))) >= 16
        except Exception:
            return False


# Validate if there is only one type in the batch
# receives the field
# returns True if type is unique
#         False if type is not unique
class DistinctCustomValidation(CustomValidation):
    def validate(self, field):
        try:
            ret = False
            
            # check if there is only one type of field
            # by checking if there is no other type
            field = DistinctEntity.objects.filter(~Q(field=field)).first()
            if field is None:
                ret = True

            if ret:
                # add current field to table
                field = DistinctEntity(field=field)
                field.save()
            
            return ret
        except Exception:
            return False
