from django.shortcuts import render
from rest_framework import views, response
from django.core.files.storage import FileSystemStorage
from edi import settings
from . import helpers


class ApiParser(views.APIView):

    def post(self, request, format=None):
        status = 200
        data = { 'response': 'OK', 'valid': False, 'messages': [] }

        # check for parameters
        if 'file' in request.FILES and 'id' in request.POST:

                # load layout id from request
                id = request.POST.get('id', '0')

                # upload the file to a folder
                myfile = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                media_path = settings.MEDIA_ROOT

                # Find selected layout
                layout = next((item for item in settings.EDI_LAYOUTS if item['id'] == id), None)
                if layout is not None:

                    # Processing layout
                    data['messages'].append('Processing layout: {}'.format(layout['type']))
                    
                    # Regex matching
                    allLinesMatch, messages = helpers.regex_match(layout, media_path + '\\' + filename)

                    # updating validate status
                    data['valid'] = allLinesMatch
                    data['messages'] = [ *data['messages'], *messages ]

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


