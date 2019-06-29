from abc import ABCMeta, abstractmethod
from ..models import SaveFieldEntity, SumFieldEntity


class CustomAction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, field, position, registro):
        pass


# Save the field and its position
# receives the field, the position in the map and the registro
# returns None
class SaveFieldCustomAction(CustomAction):
    def run(self, field, position, registro):
        try:
            # First we check if it already exists
            save_field = SaveFieldEntity.objects.filter(
                field=field, position=position, registro=registro).first()

            if save_field is None:
                # if not exists, create
                save_field = SaveFieldEntity(field=field, position=position, registro=registro)
                save_field.save()
            else:
                # if exists, update the value
                save_field.field = field
                save_field.save()

            return None
        except:
            return None


# Sum value of the field
# receives the field, the position in the map and the registro
# returns None
class SumFieldCustomAction(CustomAction):
    def run(self, field, position, registro):
        try:
            # First we check if it already exists
            sum_field = SumFieldEntity.objects.filter(
                field=field, position=position, registro=registro).first()

            if sum_field is None:
                # if not exists, create
                sum_field = SumFieldEntity(field=field, position=position, registro=registro)
                sum_field.save()
            else:
                # if exists, update sum of the value
                sum_field.field += int(field)
                sum_field.save()

            return None
        except:
            return None
