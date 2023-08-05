import unittest
from constructio_sdk import ComputeContext
import constructio_sdk as sdk


class ComputeContextTestCase(unittest.TestCase):
    # noinspection PyMethodMayBeStatic
    def test_using_sdk(self):
        e = sdk.init_compute({'id': 'zzz', 'upload': {}, 'a': 45})
        e.add_message('my first message')
        e.add_message('my second message', 'error')
        e.add_file_with('test.txt', 'This is the content of the text file', 'text/plain')
        e.add_file_with('test2.csv', 'a,b,c', 'text/csv')
        self.assertEqual(45, e.get('a'))
        response = e.send()
        self.assertEqual(0, len(response['links']))
        self.assertEqual(2, len(response['messages']))
        self.assertEqual(0, len(response['files']))

    def test_basic_usage(self):
        e = ComputeContext('aaa', {}, {})
        e.add_link('https://link1.com')
        e.add_link('https://link2.com', 'some link')
        response = e.send()
        self.assertEqual(2, len(response['links']))

    def test_set(self):
        e = ComputeContext('aaa', {}, {})
        e.set('x', 12)
        e.set('y', 1.54321, True)
        e.set('z', [1, 2, 3, 4])
        response = e.send()
        self.assertEqual(12, response['output']['x'])
        self.assertEqual(1.54321, response['summary']['y'])
        self.assertEqual([1, 2, 3, 4], response['output']['z'])
