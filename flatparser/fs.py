from django.core.files.storage import FileSystemStorage
from edi import settings


# Save the upload to filesystem
def save_upload(myfile):
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    media_path = settings.MEDIA_ROOT
    return media_path + '\\' + filename


# Open a file for reading and yield a line
def read_file(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield line
