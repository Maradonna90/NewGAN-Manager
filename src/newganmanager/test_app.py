import unittest
from app import NewGANManager
from rtfparser import RTF_Parser
from config_manager import Config_Manager
from profile_manager import Profile_Manager
import os
import shutil


class Test_RTF_Parser(unittest.TestCase):

    def test_parse_rtf(self):
        test_simple = RTF_Parser.parse_rtf(None, "test/test_simple.rtf")
        self.assertSequenceEqual(test_simple[0], ["1915714540", "ESP", "BAS", "1"])
        self.assertSequenceEqual(test_simple[1], ["1915576430", "KSA", "ARG", "2"])
        self.assertEqual(len(test_simple), 2)

    def test_parse_rtf_with_short_UIDs(self):
        test_simple_UID = RTF_Parser.parse_rtf(None, "test/test_simple_UID.rtf")
        self.assertSequenceEqual(test_simple_UID[0], ["1915576430", "KSA", "ARG", "2"])
        self.assertEqual(len(test_simple_UID), 1)

class Test_Config_Manager(unittest.TestCase):

    def test_get_latest_prf(self):
        latest_prf = Config_Manager().get_latest_prf("test/simple_cfg.json")
        self.assertEqual(latest_prf, "Profile2")


class Test_Profile_Manager(unittest.TestCase):
    def setUp(self):
        self.pm = Profile_Manager(".config/cfg.json", "No Profile")

    def test_delete_profile(self):
        pass

    def test_create_profile(self):

        self.pm.create_profile("test")
        cfg = Config_Manager().load_config(".config/cfg.json")
        self.assertFalse(cfg["Profile"]["test"])
        self.assertTrue(os.path.isfile(".config/test.json"))
        self.assertTrue(os.path.isfile(".config/test.xml"))
        prf_cfg = Config_Manager().load_config(".config/test.json")
        self.assertEqual(prf_cfg["imgs"], {})
        self.assertEqual(prf_cfg["ethnics"], {})
        self.assertEqual(prf_cfg["img_dir"], "")
        self.assertEqual(prf_cfg["rtf"], "")

    def test_load_profile(self):
        pass

    def test_write_xml(self):
        pass

    def test_swap_xml(self):
        self.pm.swap_xml("test", "No Profile", "test/", "test/")
        with open(".config/test.xml", "r") as test_xml:
            self.assertEqual(test_xml.read(), "OUTSIDE")
        with open("test/config.xml", "r") as config_xml:
            self.assertEqual(config_xml.read(), "")

    def test_get_ethnic(self):
        self.assertEqual(self.pm.get_ethnic("GER"), "Central European")
        self.assertEqual(self.pm.get_ethnic("ZZZ"), None)

    def tearDown(self):
        shutil.rmtree(".config/")
        shutil.copytree("../../.config/", ".config/")
        with open("test/config.xml", "w") as cfg:
            cfg.write('OUTSIDE')


class Test_Mapper(unittest.TestCase):

    def test_generate_mapping_generate(self):
        pass

    def test_generate_mapping_preserve(self):
        pass

    def test_generate_mapping_overwrite(self):
        pass


if __name__ == '__main__':
    unittest.main()
