import mongoengine
import os

class File(mongoengine.Document):
    name = mongoengine.StringField()
    path = mongoengine.StringField()
    created = mongoengine.DecimalField()
    modified = mongoengine.DecimalField()
    description = mongoengine.StringField()

def connect():
    mongoengine.connect('db', host='mongodb://root:example@localhost:27017')

def disconnect():
    mongoengine.disconnect()

def index_file(file_path, description):
    file = File(
        name=os.path.basename(file_path),
        path=file_path,
        created=os.path.getctime(file_path),
        modified=os.path.getmtime(file_path),
        description=description
    )
    file.save()

def get_file_outdated(file_path):
    file = File.objects(path=file_path).first()
    if file is None:
        return None
    file_modified = os.path.getatime(file_path)
    if file_modified > file.modified.timestamp():
        return file
    return None

def get_all_files():
    return File.objects

def get_all_files_caches():
    return {file.path: file.description for file in File.objects}
