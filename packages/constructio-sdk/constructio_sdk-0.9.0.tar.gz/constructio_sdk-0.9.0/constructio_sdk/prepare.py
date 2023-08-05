from .simulation import Simulation


class PrepareContext:
    def __init__(self, preparation_id, data):
        self.id = preparation_id
        self.data = data
        self.response = None
        self.reset()

    def get(self, key, value=None):
        if key in self.data:
            return self.data[key]
        return value

    def add_simulation(self, summary=None, data=None):
        s = Simulation(summary, data)
        self.response['simulations'].append(s)
        return s

    def reset(self):
        self.response = {
            'simulations': [],
        }

    def send(self):
        r = self.response
        self.reset()
        for i, s in enumerate(r['simulations']):
            s = s.pack()
            s['input'] = s['data']
            s.pop('data', None)
            r['simulations'][i] = s
        return r
