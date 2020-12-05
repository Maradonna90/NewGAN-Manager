import unittest
from rtfparser import RTF_Parser
from config_manager import Config_Manager
from profile_manager import Profile_Manager
from xmlparser import XML_Parser
import os
import shutil


class Test_XML_Parser(unittest.TestCase):
    def test_parse_xml(self):
        test_xml = XML_Parser.parse_xml(None, "newganmanager/test/test.xml")
        self.assertDictEqual(test_xml, {"0123456789": {"ethnicity": "African", "image": "African1"}})


class Test_RTF_Parser(unittest.TestCase):

    def test_parse_rtf(self):
        test_simple = RTF_Parser.parse_rtf(None, "newganmanager/test/test_simple.rtf")
        self.assertSequenceEqual(test_simple[0], ["1915714540", "ESP", "BAS", "1"])
        self.assertSequenceEqual(test_simple[1], ["1915576430", "KSA", "ARG", "2"])
        self.assertEqual(len(test_simple), 2)

    def test_parse_rtf_with_short_UIDs(self):
        test_simple_UID = RTF_Parser.parse_rtf(None, "newganmanager/test/test_simple_UID.rtf")
        self.assertSequenceEqual(test_simple_UID[0], ["1915576430", "KSA", "ARG", "2"])
        self.assertEqual(len(test_simple_UID), 1)


class Test_Config_Manager(unittest.TestCase):

    def test_get_latest_prf(self):
        latest_prf = Config_Manager().get_latest_prf("newganmanager/test/simple_cfg.json")
        self.assertEqual(latest_prf, "Profile2")


class Test_Xml_Writing(unittest.TestCase):
    def setUp(self):
        self.pm = Profile_Manager("No Profile", "newganmanager/testing/")
        self.pm.prf_cfg["img_dir"] = "newganmanager/test/"
        self.data = [
            ["African", "African1", "1915714540"],
            ["Caucasian", "Caucasian2", "1915576430"]
        ]
        self.xml_data = self.pm.write_xml(self.data)

    def test_write_xml_template_string_formatting(self):
        for xml_player, player in zip(self.xml_data, self.data):
            self.assertEqual("<record from=\""+player[1]+"/"+player[2]+"\" to=\"graphics/pictures/person/"+player[0]+"/portrait\"/>", xml_player)

    def test_write_xml_players_mapped_in_file(self):
        with open(self.pm.prf_cfg['img_dir']+"config.xml", 'r', encoding="UTF-8") as fp:
            xml_file = fp.read()
        for player in self.data:
            self.assertIn("<record from=\""+player[1]+"/"+player[2]+"\" to=\"graphics/pictures/person/"+player[0]+"/portrait\"/>", xml_file)

    def test_write_xml_no_file_endings(self):
        with open(self.pm.prf_cfg['img_dir']+"config.xml", 'r', encoding="UTF-8") as fp:
            xml_file = fp.read()
        self.assertNotIn(".png", xml_file)

    def tearDown(self):
        shutil.rmtree("newganmanager/testing/.config/")
        shutil.copytree("newganmanager/.config/", "newganmanager/testing/.config/")
        shutil.rmtree("newganmanager/testing/.user/")
        shutil.copytree("newganmanager/.user/", "newganmanager/testing/.user/")
        with open("newganmanager/test/config.xml", "w") as cfg:
            cfg.write('OUTSIDE')


class Test_Profile_Manager(unittest.TestCase):
    def setUp(self):
        self.pm = Profile_Manager("No Profile", "newganmanager/testing/")

    def test_delete_profile(self):
        pass

    def test_create_profile(self):

        self.pm.create_profile("test")
        cfg = Config_Manager().load_config("newganmanager/testing/.user/cfg.json")
        self.assertFalse(cfg["Profile"]["test"])
        self.assertTrue(os.path.isfile("newganmanager/testing/.user/test.json"))
        self.assertTrue(os.path.isfile("newganmanager/testing/.user/test.xml"))
        prf_cfg = Config_Manager().load_config("newganmanager/testing/.user/test.json")
        self.assertEqual(prf_cfg["imgs"], {})
        self.assertEqual(prf_cfg["ethnics"], {})
        self.assertEqual(prf_cfg["img_dir"], "")
        self.assertEqual(prf_cfg["rtf"], "")

    def test_load_profile(self):
        pass

    def test_swap_xml(self):
        self.pm.swap_xml("test", "No Profile", "newganmanager/test/", "newganmanager/test/")
        with open("newganmanager/testing/.user/test.xml", "r") as test_xml:
            self.assertEqual(test_xml.read(), "OUTSIDE")
        with open("newganmanager/test/config.xml", "r") as config_xml:
            self.assertEqual(config_xml.read(), "")

    def test_get_ethnic(self):
        self.assertEqual(self.pm.get_ethnic("GER"), "Central European")
        self.assertEqual(self.pm.get_ethnic("ZZZ"), None)

    def test_switching_profiles_with_invalid_path(self):

        self.pm.swap_xml("test", "No Profile", "newganmanager/invalid/", "newganmanager/test/")
        self.pm.swap_xml("No Profile", "test", "newganmanager/test/", "newganmanager/invalid/")

    def test_migrate_function(self):
      newganmanager/testing/
        cfg = Config_Manager().load_config("newganmanager/testing/.config/cfg.json")
        cfg["Profile"] = {"testmig" : False, "No Profile": True}
        Config_Manager().save_config("newganmanager/testing/.config/cfg.json", cfg)
        self.pm.eth_cfg = cfg
        f = open("newganmanager/testing/.config/testmig.xml", "a")
        f.write("TESTMIGXML!")
        f.close()
        f = open("newganmanager/testing/.config/testmig.json", "a")
        f.write("{'text': 'TESTMIGJSON!'}")
        f.close()
        self.pm.migrate_config()
        res_cfg = Config_Manager().load_config("newganmanager/testing/.config/cfg.json")
        self.assertNotIn("Profile", res_cfg)
        self.assertIn("Ethnics", res_cfg)
        usr_cfg = Config_Manager().load_config("newganmanager/testing/.user/cfg.json")
        self.assertNotIn("Ethnics", usr_cfg)
        self.assertIn("Profile", usr_cfg)
        self.assertTrue(os.path.isfile("newganmanager/testing/.user/testmig.json"))
        self.assertTrue(os.path.isfile("newganmanager/testing/.user/testmig.xml"))
        self.assertFalse(os.path.isfile("newganmanager/testing/.config/testmig.json"))
        self.assertFalse(os.path.isfile("newganmanager/testing/.config/testmig.xml"))

    def tearDown(self):
        shutil.rmtree("newganmanager/testing/.config/")
        shutil.copytree("newganmanager/.config/", "newganmanager/testing/.config/")
        shutil.rmtree("newganmanager/testing/.user/")
        shutil.copytree("newganmanager/.user/", "newganmanager/testing/.user/")
        with open("newganmanager/test/config.xml", "w") as cfg:
            cfg.write('OUTSIDE')


if __name__ == '__main__':
    unittest.main()
