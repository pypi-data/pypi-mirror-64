import datetime
from decimal import Decimal
import unittest
import tempfile

from stoqlib.lib.settings import UserSettings, _decode_list, _encode_object


class SettingsTest(unittest.TestCase):

    def test_settings_process(self):
        with tempfile.NamedTemporaryFile() as tmp:
            settings = UserSettings(filename=tmp.name)

            # Set a value and recover it.
            settings.set('value', 123)
            self.assertEqual(settings.get('value'), 123)

            # Get a non existing value with a default fallback
            self.assertEqual(settings.get('other_value', 456), 456)

            # Getting it again should have saved the value
            self.assertEqual(settings.get('other_value'), 456)

            # Now, lets remove that value.
            settings.remove('other_value')
            self.assertEqual(list(settings.items()), [('value', 123)])

            # Getting it again should return None
            self.assertEqual(settings.get('other_value'), None)

            # Flush
            settings.flush()

    def test_decode_list(self):
        value = [u'unicode', [123], {u'a': u'b'}]
        self.assertEqual(_decode_list(value), value)

    def test_encode_object(self):
        self.assertEqual(_encode_object(Decimal('0.99')), '0.99')
        self.assertEqual(_encode_object(datetime.date(2016, 2, 7)), '2016-02-07')
        self.assertEqual(_encode_object(datetime.datetime(2016, 2, 7, 19, 45, 30)),
                         '2016-02-07T19:45:30')
