from time import time
from .simulation import Simulation
from requests import post
from zipfile import ZipFile
from tempfile import gettempdir
from os import remove, path


class ComputeContext(Simulation):
    def __init__(self, execution_id, upload, data):
        Simulation.__init__(self, {}, data)
        self.id = execution_id
        self.upload = upload

    def package_files(self):
        package_path = None
        if 0 < len(self.files):
            package_path = path.join(gettempdir(), 'constructio-sdk-simulation-' + self.id + '-files.zip')
            with ZipFile(package_path, 'w') as zip_file:
                for k, v in self.files.items():
                    if 'inline' == v['type']:
                        zip_file.writestr(k, v['content'])
                    if 'file' == v['type']:
                        zip_file.write(v.path, k)
        return package_path

    def send(self):
        r = self.pack()
        t = int(time())
        i = len(r['steps'])
        if i > 0:
            previous = r['steps'][i - 1]
            previous['endTime'] = t
            previous['duration'] = t - previous['endTime']
        if self.upload and 'url' in self.upload:
            package_path = self.package_files()
            if package_path is not None:
                files = {'file': open(package_path, 'rb')}
                post(self.upload['url'], data=self.upload['fields'] if 'fields' in self.upload else {}, files=files)
                remove(package_path)
            else:
                r['files'] = []
        else:
            r['files'] = []
        r['output'] = r['data']
        r.pop('data', None)
        self.reset()
        return r
