from os import path
from mimetypes import guess_type
from time import time


class Simulation:
    def __init__(self, summary=None, data=None):
        self.summary = summary if summary is not None else {}
        self.data = data if data is not None else {}
        self.selected = False
        self.files = None
        self.response = None
        self.temp = None
        self.reset()

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def add_tag(self, tag):
        self.response['tags'].append(tag)

    def add_file(self, name, group=None):
        n = path.basename(name)
        self.files[n] = {'type': 'file', 'path': name}
        self.response['files'].append({'path': n, 'group': group, 'type': guess_type(name)[0]})

    def add_plot_file(self, name, plt, group=None, dpi=150):
        plt.savefig(name, dpi)
        self.add_file(name, group)

    def add_file_with(self, name, content, mime_type, group=None):
        n = path.basename(name)
        self.files[n] = {'type': 'inline', 'content': content}
        self.response['files'].append({'path': n, 'group': group, 'type': mime_type})

    def add_link(self, url, label=None):
        self.response['links'].append({'url': url, 'label': label})

    def add_message(self, message, level='info'):
        self.response['messages'].append({'message': message, 'level': level})

    def add_violation(self, variable, message, level='critical', params=None):
        self.response['violations'].append({'variable': variable, 'message': message, 'level': level, 'params': params})

    # noinspection PyMethodMayBeStatic
    def with_unit(self, value, unit):
        return {'value': value, 'unit': unit}

    def add_metadata(self, key, value):
        self.response['execution'][key] = value

    def set(self, key, value, summary=False):
        self.response['data'][key] = value
        if summary:
            self.response['summary'][key] = value

    def set_with_unit(self, key, value, unit, summary=False):
        self.set(key, self.with_unit(value, unit), summary)

    def set_temp(self, key, value):
        self.temp[key] = value

    def unset_temp(self, key):
        return self.temp.pop(key, None)

    def start_step(self, name):
        t = int(time())
        i = len(self.response['steps'])
        if i > 0:
            previous = self.response['steps'][i - 1]
            previous['endTime'] = t
            previous['duration'] = t - previous['endTime']
        self.response['steps'].append({'name': name, 'startTime': t})

    def get(self, key, value=None):
        if key in self.temp:
            return self.temp[key]
        if key in self.response['data']:
            return self.response['data']
        if key in self.data:
            return self.data[key]
        return value

    def reset(self):
        self.temp = {}
        self.files = {}
        self.response = {
            'summary': {},
            'data': {},
            'files': [],
            'links': [],
            'messages': [],
            'violations': [],
            'tags': [],
            'steps': [],
            'execution': {},
        }

    def pack(self):
        return self.response
