from django.shortcuts import render
from rest_framework import views, response
from edi import settings
from . import helpers
from .fs import save_upload

class ApiParser(views.APIView):

    def post(self, request, format=None):
        status = 200
        data = { 'response': 'OK', 'valid': False, 'messages': [] }

        # check for parameters
        if 'file' in request.FILES and 'id' in request.POST:

                # load layout id from request
                id = request.POST.get('id', '0')

                # upload the file to a folder
                file_path = save_upload(request.FILES['file'])

                # Find selected layout
                layout = next((item for item in settings.EDI_LAYOUTS if item['id'] == id), None)
                if layout is not None:

                    # Processing layout
                    data['messages'].append('Processing layout: {}'.format(layout['type']))

                    # Regex matching validation
                    is_valid, messages = helpers.regex_match(layout, file_path)
                    # updating messages log
                    data['messages'] = [ *data['messages'], *messages ]

                    # Mandatory fields validation
                    if is_valid:
                        is_valid, messages = helpers.mandatory_check(layout, file_path)
                        # updating messages log
                        data['messages'] = [ *data['messages'], *messages ]

                    # Custom actions
                    if is_valid:
                        is_valid, messages = helpers.custom_actions(layout, file_path)
                        # updating messages log
                        data['messages'] = [ *data['messages'], *messages ]

                    # Custom rules validation
                    if is_valid:
                        is_valid, messages = helpers.custom_rules(layout, file_path)
                        # updating messages log
                        data['messages'] = [ *data['messages'], *messages ]

                    # updating validate status
                    data['valid'] = is_valid
                    if not is_valid:
                        data['response'] = 'FAIL'

                else:
                    # If layout not found
                    status = 400
                    data['response'] = 'FAIL'
                    data['messages'].append('Layout id not found')
        else:
            # If parameters mismatch
            status = 400
            data['response'] = 'FAIL'
            data['messages'].append('Invalid parameters')

        # return response
        return response.Response(status=status, data=data)


