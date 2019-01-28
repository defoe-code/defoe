"""
defoe.fmp.setup tests.
"""

from unittest import TestCase

from defoe.fmp.setup import filename_to_object
from defoe.file_utils import get_path
from defoe.test.fmp import fixtures


class TestSetup(TestCase):
    """
    defoe.fmp.setup tests.
    """

    def test_filename_to_object_bad_xml(self):
        """
        Tests filename_to_object with a bad ZIP file results in a
        tuple with a filename and an error message.
        """
        filename = get_path(fixtures, 'bad.zip')
        result = filename_to_object(filename)
        self.assertTrue(result[0] is not None)
        self.assertTrue(isinstance(result[0], str))
        self.assertEqual(filename, result[0])
        self.assertTrue(result[1] is not None)
        self.assertTrue(isinstance(result[1], str))
        self.assertTrue("File is not a zip file" in str(result[1]))

    def test_filename_to_object_no_such_file(self):
        """
        Tests filename_to_object with a non-existant file results in
        a tuple with a filename and an error message.
        """
        filename = get_path(fixtures, 'no-such-file.zip')
        result = filename_to_object(filename)
        self.assertTrue(result[0] is not None)
        self.assertTrue(isinstance(result[0], str))
        self.assertEqual(filename, result[0])
        self.assertTrue(result[1] is not None)
        self.assertTrue(isinstance(result[1], str))
        self.assertTrue("No such file or directory" in str(result[1]))
