import unittest  # For writing unit tests


# Unit tests to validate the functionality
class TestMetadataFunctions(unittest.TestCase):

    def test_get_metadata_key_valid(self):
        # Assumes 'hostname' is a valid key in AWS metadata
        value = get_metadata_key("hostname")
        self.assertIsInstance(value, str)

    def test_get_metadata_key_invalid(self):
        # Tests behavior for an invalid key
        value = get_metadata_key("invalid-key")
        self.assertIsNone(value)

    def test_get_metadata(self):
        # Ensures metadata is returned as a dictionary
        metadata = get_metadata()
        self.assertIsInstance(metadata, dict)