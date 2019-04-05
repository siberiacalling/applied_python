from unittest import TestCase
import os
import shutil

from dict import DirDict


class DirBaseTest(TestCase):
    def setUp(self):
        os.makedirs("test_dir/1/2")


    def tearDown(self):
        try:
            shutil.rmtree("test_dir")
        except Exception:
            pass

    def test_base(self):
        d = DirDict("test_dir")
        d['key1'] = 'value1'
        d['key2'] = 'value2'

        self.assertEqual(['key1', '1', 'key2'], list(d))

    def test_update(self):
        d = DirDict("test_dir")
        d['key1'] = 'value1'
        d['key2'] = 'value2'

        self.assertEqual('value1', d.__getitem__('key1'))
        self.assertEqual('value2', d.__getitem__('key2'))

        d['key1'] = 'value3'
        d['key2'] = 'value4'

        self.assertEqual('value3', d.__getitem__('key1'))
        self.assertEqual('value4', d.__getitem__('key2'))

    def test_delete(self):
        d = DirDict("test_dir")
        d['key1'] = 'value1'
        d['key2'] = 'value2'
        d['key3'] = 'value3'

        d.__delitem__('key1')
        self.assertEqual(['1', 'key3', 'key2'], list(d))

        d.__delitem__('key2')
        self.assertEqual(['1', 'key3'], list(d))

        d.__delitem__('key3')
        self.assertEqual(['1'], list(d))

    def test_nested_dictionary(self):
        with open("test_dir/key1", "w") as f:
            f.write("first_file_string")
        with open("test_dir/1/key2", "w") as f:
            f.write("second_file_string")
        with open("test_dir/1/2/key3", "w") as f:
            f.write("third_file_string")

        d = DirDict("test_dir")

        self.assertEqual('first_file_string', d['key1'])
        self.assertEqual('second_file_string', d['1']['key2'])
        self.assertEqual('third_file_string', d['1']['2']['key3'])