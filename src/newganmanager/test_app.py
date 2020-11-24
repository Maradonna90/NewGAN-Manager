import unittest
from app import NewGANManager

class Test_Parsing(unittest.TestCase):
    def test_parse_rtf(self):
        res_data = NewGANManager.parse_rtf(None, "test3.rtf")
        self.assertSequenceEqual(res_data[0], ["1915714540", "ESP", "BAS", "1"])
        self.assertSequenceEqual(res_data[1], ["1915576430", "KSA", "ARG", "2"])


class Test_GenerationModes(unittest.TestCase):
    
    def test_parse_rtf(self):
        pass

    def test_generate_replacement(self):
        pass

    def test_preserve_replacement(self):
        pass

    def test_overwrite_repalcement(self):
        pass


class Test_Profile(unittest.TestCase):

    def test_create_profile(self):
        pass

    def test_load_profile(self):
        pass

    def test_delete_profile(self):
        pass

    def test_set_profile_status(self):
        pass


class Test_Report(unittest.TestCase):

    def test_send_report(self):
        pass

    def test_change_image(self):
        pass


if __name__ == '__main__':
    unittest.main()
