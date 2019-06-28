import re


def regex_match(layout, filepath):

    # open file for reading
    f = open(filepath, 'r')

    # Processing lines
    allLinesMatch = True
    count = 1
    messages = []

    for line in f:
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