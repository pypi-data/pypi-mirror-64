from time import time
from .simulation import Simulation


class ComputeContext(Simulation):
    def __init__(self, execution_id, upload_url, data):
        Simulation.__init__(self, {}, data)
        self.id = execution_id
        self.upload_url = upload_url

    def send(self):
        r = self.pack()
        t = int(time())
        i = len(r['steps'])
        if i > 0:
            previous = r['steps'][i - 1]
            previous['endTime'] = t
            previous['duration'] = t - previous['endTime']
        # @todo pack files into zip then use self.upload_url to post the one big zip file
        r['output'] = r['data']
        r.pop('data', None)
        self.reset()
        return r
