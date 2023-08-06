import unittest
from constructio_sdk import PrepareContext
import constructio_sdk as sdk


class PrepareContextTestCase(unittest.TestCase):
    # noinspection PyMethodMayBeStatic
    def test_using_sdk(self):
        e = sdk.init_prepare({'id': 'zzz', 'b': 12.5})
        self.assertEqual(12.5, e.get('b'))
        response = e.send()
        self.assertEqual(0, len(response['simulations']))

    def test_basic_usage(self):
        e = PrepareContext('aaa', {})
        s1 = e.add_simulation()
        s1.set('key1', 34.567)
        response = e.send()
        self.assertEqual(1, len(response['simulations']))
        self.assertEqual(34.567, response['simulations'][0]['input']['key1'])
