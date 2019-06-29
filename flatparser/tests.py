from django.test import TestCase
from .models import UniqueWithin30daysEntity, UniqueEntity, DistinctEntity, SaveFieldEntity, \
                    SumFieldEntity
from .factory.validation import UniqueWithin30daysCustomValidation, NumberCustomValidation, \
                                TextCustomValidation, DateCustomValidation, UniqueCustomValidation, \
                                GreaterThanOrEqualTo16CustomValidation, DistinctCustomValidation, \
                                SameAsHeader3CustomValidation, SameAsHeader6CustomValidation, \
                                SumDetalhe7CustomValidation
from .factory.action import SaveFieldCustomAction, SumFieldCustomAction
from edi import settings
from .helpers import regex_match, mandatory_check, custom_actions, custom_rules
import os

class UniqueWithin30daysTestCase(TestCase):
    def setUp(self):
        UniqueWithin30daysEntity.objects.create(field=9999999)

    def test_uniqueness_within_30days(self):
        self.assertFalse(UniqueWithin30daysCustomValidation().validate(9999999),
                            msg="Trying to duplicate unique field within 30 days")

    def test_different_key_within_30days(self):
        self.assertTrue(UniqueWithin30daysCustomValidation().validate(9999998),
                            msg="Trying to create another field value within 30 days")


class NumberCustomValidatorTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_number_validation(self):
        self.assertTrue(NumberCustomValidation().validate(10), msg='Number validator test')

    def test_not_number_validation(self):
        self.assertFalse(NumberCustomValidation().validate('test'), msg='Not number validator test')
    
    def test_empty_number_validation(self):
        self.assertFalse(NumberCustomValidation().validate(0), msg='Empty number validator test')


class TextCustomValidatorTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_empty_text_validation(self):
        self.assertFalse(TextCustomValidation().validate(''), msg='Empty text validator test')

    def test_text_validation(self):
        self.assertTrue(TextCustomValidation().validate('test'), msg='Text validator test')


class DateCustomValidatorTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_not_date_validation(self):
        self.assertFalse(DateCustomValidation().validate('31022019'), msg='Not date validator test')

    def test_date_validation(self):
        self.assertTrue(DateCustomValidation().validate('01022019'), msg='Date validator test')


class UniqueCustomValidationTestCase(TestCase):
    def setUp(self):
        UniqueEntity.objects.all().delete()
        UniqueEntity.objects.create(field=2)
    
    def test_not_unique_validation(self):
        self.assertFalse(UniqueCustomValidation().validate(2), msg='Not unique validator test')

    def test_unique_validation(self):
        self.assertTrue(UniqueCustomValidation().validate(1), msg='Unique validator test')


class GreaterThanOrEqualTo16CustomValidationTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_not_gte16_validation(self):
        self.assertFalse(GreaterThanOrEqualTo16CustomValidation().validate(1), 
                         msg='Not gte16 validator test')

    def test_gte16_validation(self):
        self.assertTrue(GreaterThanOrEqualTo16CustomValidation().validate(1234567890123456), 
                        msg='Gte16 validator test')


class DistinctCustomValidationTestCase(TestCase):
    def setUp(self):
        DistinctEntity.objects.all().delete()
        DistinctEntity.objects.create(field=2)
    
    def test_not_distinct_validation(self):
        self.assertFalse(DistinctCustomValidation().validate(1), msg='Not distinct validator test')

    def test_distinct_validation(self):
        self.assertTrue(DistinctCustomValidation().validate(2), msg='Distinct validator test')


class SameAsHeader3CustomValidationTestCase(TestCase):
    def setUp(self):
        SaveFieldEntity.objects.all().delete()
        SaveFieldEntity.objects.create(field=2, position=3, registro='header')
    
    def test_not_same_validation(self):
        self.assertFalse(SameAsHeader3CustomValidation().validate(1), 
                         msg='Not same as header 3 validator test')

    def test_same_validation(self):
        self.assertTrue(SameAsHeader3CustomValidation().validate(2), 
                        msg='Same as header 3 validator test')


class SameAsHeader6CustomValidationTestCase(TestCase):
    def setUp(self):
        SaveFieldEntity.objects.all().delete()
        SaveFieldEntity.objects.create(field=2, position=6, registro='header')
    
    def test_not_same_validation(self):
        self.assertFalse(SameAsHeader6CustomValidation().validate(1), 
                         msg='Not same as header 6 validator test')

    def test_same_validation(self):
        self.assertTrue(SameAsHeader6CustomValidation().validate(2), 
                        msg='Same as header 6 validator test')


class SumDetalhe7CustomValidationTestCase(TestCase):
    def setUp(self):
        SumFieldEntity.objects.all().delete()
        SumFieldEntity.objects.create(field=2, position=7, registro='detalhe')
    
    def test_not_sum_validation(self):
        self.assertFalse(SumDetalhe7CustomValidation().validate(1), 
                         msg='Not sum detalhe 7 validator test')

    def test_sum_validation(self):
        self.assertTrue(SumDetalhe7CustomValidation().validate(2), 
                        msg='Sum detalhe 7 validator test')


class SaveFieldCustomActionTestCase(TestCase):
    def setUp(self):
        SaveFieldEntity.objects.all().delete()
    
    def test_false_validation(self):
        SaveFieldCustomAction().run(2, 6, 'header')
        field = SaveFieldEntity.objects.filter(position=6, registro='header').first()
        self.assertIsNotNone(field, msg='Save field custom action is not none')
        self.assertNotEqual(field.field, 1, msg='Different save field custom action')

    def test_true_validation(self):
        SaveFieldCustomAction().run(2, 6, 'header')
        field = SaveFieldEntity.objects.filter(position=6, registro='header').first()
        self.assertIsNotNone(field, msg='Save field custom action is not none')
        self.assertEqual(field.field, 2, msg='Equal save field custom action')


class SumFieldCustomActionTestCase(TestCase):
    def setUp(self):
        SumFieldEntity.objects.all().delete()
    
    def test_false_validation(self):
        SumFieldCustomAction().run(2, 7, 'detalhe')
        field = SumFieldEntity.objects.filter(position=7, registro='detalhe').first()
        self.assertIsNotNone(field, msg='Sum field custom action is not none')
        self.assertNotEqual(field.field, 1, msg='Different sum field custom action')

    def test_true_validation(self):
        SumFieldCustomAction().run(2, 7, 'detalhe')
        field = SumFieldEntity.objects.filter(position=7, registro='detalhe').first()
        self.assertIsNotNone(field, msg='Sum field custom action is not none')
        self.assertEqual(field.field, 2, msg='Equal sum field custom action')


class RegexHelperTestCase(TestCase):
    def setUp(self):
        pass

    def test_true_validation(self):
        is_valid, msg = regex_match(settings.EDI_LAYOUTS[0], 
                                    os.path.join(settings.BASE_DIR, 'test_file.txt'))
        self.assertTrue(is_valid, msg='Regex is_valid')


class MandatoryHelperTestCase(TestCase):
    def setUp(self):
        pass

    def test_true_validation(self):
        is_valid, msg = mandatory_check(settings.EDI_LAYOUTS[0], 
                                    os.path.join(settings.BASE_DIR, 'test_file.txt'))
        self.assertTrue(is_valid, msg='Mandatory is_valid')


class CustomActionsHelperTestCase(TestCase):
    def setUp(self):
        pass

    def test_true_validation(self):
        is_valid, msg = custom_actions(settings.EDI_LAYOUTS[0], 
                                    os.path.join(settings.BASE_DIR, 'test_file.txt'))
        self.assertTrue(is_valid, msg='Custom Actions is_valid')


class CustomRulesHelperTestCase(TestCase):
    def setUp(self):
        UniqueWithin30daysEntity.objects.all().delete()

    def test_true_validation(self):
        is_valid, msg = custom_actions(settings.EDI_LAYOUTS[0], 
                                    os.path.join(settings.BASE_DIR, 'test_file.txt'))
        self.assertTrue(is_valid, msg='Custom Actions before custom rules is_valid')
        is_valid, msg = custom_rules(settings.EDI_LAYOUTS[0], 
                                    os.path.join(settings.BASE_DIR, 'test_file.txt'))
        self.assertTrue(is_valid, msg='Custom Rules is_valid')
