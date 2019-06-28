import re
from .factory import DateCustomValidation
from .models import EdiFile


def read_file(filepath):
     # open file for reading
    with open(filepath, 'r') as f:
        for line in f:
            yield line


def register_data(layout, filepath):

    try:

        for line in read_file(filepath):

            for registro in layout['layout']:
                # Regex search for a match
                match = re.search(registro['regex'], line)
                if match is not None:
                    edi_file = EdiFile(
                        resumo_operacoes = \
                            line[registro['positions'][registro['data'] - 1][0] - 1:\
                                 registro['positions'][registro['data'] - 1][1] - 1],
                        valor_venda = \
                            line[registro['positions'][registro['data'] - 1][0] - 1:\
                                 registro['positions'][registro['data'] - 1][1] - 1],

                        tipo_registro = registro['registro']
                    )
                    break

                # 'registro': 'header',
                # 'regex': r'^00\d{8}\d{7}.{10}\d{3}\d{10}$',
                # 'positions': ( {1, 2}, {3, 8}, {11, 7}, {18, 10}, {28, 3}, {31, 10}, ),
                # 'formato': ( 'N', 'N', 'N', 'X', 'N', 'N', ),
                # 'obrigatorio': ( True, True, True, False, False, True, ),
                # 'custom_validation': ( None, 'Date', 'NewerThan30days', None, None, )
        
        return (True, [ 'Data persisted in the database' ])

    except Exception as e:
        return (False, [ str(e) ],)


def regex_match(layout, filepath):

    try:

        # Processing lines
        allLinesMatch = True
        count = 1
        messages = []

        for line in read_file(filepath):
            # print(line)
            
            # Matching for header, detalhe or trailler
            foundMatch = False
            for registro in layout['layout']:
                messages.append('Validating #{} for {}'.format(count, registro['registro']))

                # Regex search for a match
                match = re.search(registro['regex'], line)
                if match is not None:
                    # Found a match
                    foundMatch = True
                    messages.append('Line #{} OK for {}!'.format(count, registro['registro']))
                    break

            # check for found match
            # otherwise there is no point in continue
            if not foundMatch:
                allLinesMatch = False
                messages.append('Found layout mismatch in line #{}'.format(count))
                break 

            # update line count    
            count += 1
        
        return (allLinesMatch, messages,)

    except Exception as e:
        return (False, [ str(e) ],)



def mandatory_check(layout, filepath):
    allLinesMatch = True
    messages = []

    return (allLinesMatch, messages,)


def custom_rules(layout, filepath):

    try:
        
        # Processing lines
        allLinesMatch = True
        count = 1
        messages = []

        for line in read_file(filepath):
            # print(line)
            
            # Matching for header, detalhe or trailler
            foundMatch = False
            for registro in layout['layout']:
                
                validation = DateCustomValidation()
                ret = validation.validate('')

            # check for found match
            # otherwise there is no point in continue
            if not foundMatch:
                allLinesMatch = False
                messages.append('Found custom validation mismatch in line #{}'.format(count))
                break 

            # update line count    
            count += 1
        
        return (allLinesMatch, messages,)

    except Exception as e:
        return (False, [ str(e) ],)
