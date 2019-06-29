from abc import ABCMeta, abstractmethod
import datetime
from ..fs import read_file
from ..models import UniqueWithin30daysEntity, UniqueEntity, DistinctEntity, \
                        SaveFieldEntity, SumFieldEntity
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
            unique = UniqueEntity.objects.filter(field=field).first()
            if unique is None:
                return True

            return False
        except Exception as e:
            print(e)
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
            entity = DistinctEntity.objects.filter(~Q(field=field)).first()
            if entity is None:
                ret = True

            if ret:
                # add current field to table
                entity = DistinctEntity(field=field)
                entity.save()
            
            return ret
        except Exception:
            return False


# Validate if field value is same than third header's field
# receives the field
# returns True if value match with third header's field
#         False if value does not match with third header's field
class SameAsHeader3CustomValidation(CustomValidation):
    def validate(self, field):
        return EqualFields.verify(field, 3, 'header')


# Validate if field value is same than sixth header's field
# receives the field
# returns True if value match with sixth header's field
#         False if value does not match with sixth header's field
class SameAsHeader6CustomValidation(CustomValidation):
    def validate(self, field):
        return EqualFields.verify(field, 6, 'header')


# Validate if field value is the sum of detalhe's seventh field
# receives the field
# returns True if value match with sum of detalhe's seventh field
#         False if value does not match with sum of detalhe's seventh field
class SumDetalhe7CustomValidation(CustomValidation):
    def validate(self, field):
        try:
   
            # get the value 
            entity = SumFieldEntity.objects.filter(
                position=7, registro='detalhe').first()
            if entity is None:
                # if there is no value, return false
                return False

            else:
                # check if the value is the same
                return entity.field == int(field)

        except Exception:
            return False


# Helper function to check if the fields are equal
# receives the field, the position in the map and the registro
# returns True if value match
#         False if value does not match
class EqualFields():
    @staticmethod
    def verify(field, position, registro):
        try:
                        
            # get the value 
            entity = SaveFieldEntity.objects.filter(
                position=position, registro=registro).first()
            if entity is None:
                # if there is no value, return false
                return False

            else:
                # check if the value is the same
                return entity.field == int(field)

        except Exception:
            return False
