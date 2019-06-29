import re
from .factory.validation import DateCustomValidation, NumberCustomValidation, TextCustomValidation, \
                            UniqueWithin30daysCustomValidation, UniqueCustomValidation, \
                            GreaterThanOrEqualTo16CustomValidation, DistinctCustomValidation, \
                            SameAsHeader3CustomValidation, SumDetalhe7CustomValidation, \
                            SameAsHeader6CustomValidation
from .factory.action import SaveFieldCustomAction, SumFieldCustomAction
from .fs import read_file
from .models import UniqueEntity, DistinctEntity, SaveFieldEntity, SumFieldEntity


# Regex match for validate positional file
# receives a layout and filepath
# returns a tuple containing if it is a match and a message array
def regex_match(layout, filepath):

    try:

        # Processing lines
        is_valid = True
        count = 1
        messages = []

        for line in read_file(filepath):
            # print(line)
            
            # Matching for header, detalhe or trailler
            found_match = False
            for registro in layout['layout']:
                messages.append('Validating line #{} for {}'.format(count, registro['registro']))

                # Regex search for a match
                match = re.search(registro['regex'], line)
                if match is not None:
                    # Found a match
                    found_match = True
                    messages.append('Line #{} OK for {}!'.format(count, registro['registro']))
                    break

            # check for found match
            # otherwise there is no point in continue
            if not found_match:
                is_valid = False
                messages.append('Found layout mismatch in line #{}'.format(count))
                break 

            # update line count    
            count += 1
        
        return (is_valid, messages,)

    except Exception as e:
        return (False, [ str(e) ],)


# Check for mandatory fields
# receives a layout and filepath
# returns a tuple containing if it is valid and a message array
def mandatory_check(layout, filepath):

    try:

        # Processing lines
        is_valid = True
        count = 1
        messages = []

        for line in read_file(filepath):
            # print(line)
            
            # Matching for header, detalhe or trailler
            for registro in layout['layout']:

                # Regex search for a match
                match = re.search(registro['regex'], line)
                if match is not None:
                    # Found a match
                    messages.append('Mandatory fields for line #{} for {}'.format(count, registro['registro']))

                    # Iterate through the fields
                    i = 0
                    for position_start, position_len in registro['positions']:

                        # Check if it is mandatory
                        if registro['obrigatorio'][i]:

                            # First we get the field
                            # from its coordinates
                            field = line[position_start - 1:position_start + position_len - 1]

                            # Then we check its format
                            # N for number
                            # X for text
                            if registro['formato'][i] == 'N':
                                # finally check its contents for number
                                is_valid = NumberCustomValidation().validate(field)
                            else:
                                # and check its contents for text
                                is_valid = TextCustomValidation().validate(field)

                            messages.append('Mandatory field #{} for line #{} is {}!'\
                                    .format(i + 1, count, 'OK' if is_valid else 'ERROR'))

                        # check for is_valid is still true
                        # otherwise there is no point in continue
                        if not is_valid:
                            break

                        # increment field index
                        i += 1
                    
                    # Break because we found a match already
                    break
                
                # check for is_valid is still true
                # otherwise there is no point in continue
                if not is_valid:
                    break

            # update line count    
            count += 1
        
        return (is_valid, messages,)

    except Exception as e:
        return (False, [ str(e) ],)


# Run custom actions to support some custom validations later
# receives a layout and filepath
# returns a tuple containing if it is valid and a message array
def custom_actions(layout, filepath):

    try:

        # Processing lines
        count = 1
        messages = []

        # Clean previous data
        SaveFieldEntity.objects.all().delete()
        SumFieldEntity.objects.all().delete()

        for line in read_file(filepath):
            # print(line)
            
            # Matching for header, detalhe or trailler
            for registro in layout['layout']:

                # Regex search for a match
                match = re.search(registro['regex'], line)
                if match is not None:
                    # Found a match
                    messages.append('Running custom actions for line #{} for {}'.format(count, registro['registro']))

                    # Iterate through the fields
                    i = 0
                    for action_key in registro['custom_action']:

                        # Check if it is mandatory
                        if action_key is not None:

                            # First we get the field
                            # from its coordinates
                            position_start, position_len = registro['positions'][i]
                            field = line[position_start - 1:position_start + position_len - 1]

                            # Then we run actions
                            if action_key == 'SaveField':
                                # Save the field
                                SaveFieldCustomAction().run(field, i + 1, registro['registro'])
                            elif action_key == 'SumField':
                                # Sum the field
                                SumFieldCustomAction().run(field, i + 1, registro['registro'])
                                
                            else:
                                # there is no action configured for this key
                                raise Exception('There is no action ' + \
                                    'configured for this key {}'.format(action_key))

                            messages.append('Done run custom action {} for field #{} in line #{}!'\
                                    .format(action_key, i + 1, count))

                        # increment field index
                        i += 1
                    
                    # Break because we found a match already
                    break

            # update line count    
            count += 1
        
        return (True, messages,)

    except Exception as e:
        return (False, [ str(e) ],)


# Check for custom rules
# receives a layout and filepath
# returns a tuple containing if it is valid and a message array
def custom_rules(layout, filepath):

    try:

        # Processing lines
        is_valid = True
        count = 1
        messages = []

        # cleaning aux table before begin
        UniqueEntity.objects.all().delete()
        DistinctEntity.objects.all().delete()

        for line in read_file(filepath):
            # print(line)
            
            # Matching for header, detalhe or trailler
            for registro in layout['layout']:

                # Regex search for a match
                match = re.search(registro['regex'], line)
                if match is not None:
                    # Found a match
                    messages.append('Custom validation fields for line #{} for {}'.format(count, registro['registro']))

                    # Iterate through the fields
                    i = 0
                    for validation_key in registro['custom_validation']:

                        # Check if it has custom validation
                        if validation_key is not None:

                            # First we get the field
                            # from its coordinates
                            position_start, position_len = registro['positions'][i]
                            field = line[position_start - 1:position_start + position_len - 1]

                            # Then we check which validation we must run
                            if validation_key == 'Date':
                                # check for date formater
                                is_valid = DateCustomValidation().validate(field)
                            elif validation_key == 'UniqueWithin30days':
                                # check for unique within 30 days validator
                                is_valid = UniqueWithin30daysCustomValidation().validate(field)
                            elif validation_key == 'Unique':
                                # check for unique within 30 days validator
                                is_valid = UniqueCustomValidation().validate(field)
                            elif validation_key == 'GreaterThanOrEqualTo16':
                                # check for length of 16 minimum
                                is_valid = GreaterThanOrEqualTo16CustomValidation().validate(field)
                            elif validation_key == 'Distinct':
                                # check for only one type in the batch
                                is_valid = DistinctCustomValidation().validate(field)
                            elif validation_key == 'SameAsHeader3':
                                # check for match the value with third header file
                                is_valid = SameAsHeader3CustomValidation().validate(field)
                            elif validation_key == 'SameAsHeader6':
                                # check for match the value with third header file
                                is_valid = SameAsHeader6CustomValidation().validate(field)
                            elif validation_key == 'SumDetalhe7':
                                # check for match the value with sum of detalhe's seventh field
                                is_valid = SumDetalhe7CustomValidation().validate(field)
                                
                            else:
                                # there is no custom validator configured for this key
                                raise Exception('There is no custom validator ' + \
                                    'configured for this key {}'.format(validation_key))

                            messages.append('Custom validation type {} field #{} for line #{} is {}!'\
                                    .format(validation_key, i + 1, count, 'OK' if is_valid else 'ERROR'))

                        # check for is_valid is still true
                        # otherwise there is no point in continue
                        if not is_valid:
                            break

                        # increment field index
                        i += 1
                    
                    # Break because we found a match already
                    break
                
                # check for is_valid is still true
                # otherwise there is no point in continue
                if not is_valid:
                    break

            # update line count    
            count += 1
        
        return (is_valid, messages,)

    except Exception as e:
        return (False, [ str(e) ],)
