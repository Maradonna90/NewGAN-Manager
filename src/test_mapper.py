import unittest
from mapper import Mapper
from rtfparser import RTF_Parser
from profile_manager import Profile_Manager
import shutil


class Test_Mapper_Generate_Mapping(unittest.TestCase):
    def setUp(self):
        # TODO: we need prf_map, prf_imgs and prf_eth_map
        self.rtfparser = RTF_Parser()
        self.pm = Profile_Manager("No Profile", "newganmanager/testing/")
        self.pm.prf_cfg["img_dir"] = "newganmanager/test/"
        self.mapper = Mapper("newganmanager/test/", self.pm)
        # data: UID, first_nat, sec_nat, eth-code
        self.data_simple = self.rtfparser.parse_rtf("newganmanager/test/test_simple.rtf")
        self.data_all_cases = self.rtfparser.parse_rtf("newganmanager/test/test_allcases.rtf")
        for eth in ["African", "Asian", "EECA", "Italmed", "SAMed", "South American", 
                    "SpanMed", "YugoGreek", "MENA", "MESA", "Caucasian", "Central European",
                    "Scandinavian", "Seasian"]:
            map = [eth+str(i)for i in range(20)]
            self.mapper.eth_map[eth] = map

    def tearDown(self):
        shutil.rmtree("newganmanager/testing/.config/")
        shutil.copytree("newganmanager/.config/", "newganmanager/testing/.config/")
        shutil.rmtree("newganmanager/testing/.user/")
        shutil.copytree("newganmanager/.user/", "newganmanager/testing/.user/")
        with open("newganmanager/test/config.xml", "w") as cfg:
            cfg.write('OUTSIDE')

    def test_generate_mapping_simple(self):
        mapping = self.mapper.generate_mapping(self.data_simple, "Generate")
        self.assertEqual("SpanMed", mapping[0][1])
        self.assertEqual("1915714540", mapping[0][0])
        self.assertEqual("MESA", mapping[1][1])
        self.assertEqual("1915576430", mapping[1][0])

    def test_generate_mapping_all_cases(self):
        mapping = self.mapper.generate_mapping(self.data_all_cases, "Generate")
        self.assertEqual("SpanMed", mapping[0][1])
        self.assertEqual("1915714540", mapping[0][0])
        self.assertEqual("MESA", mapping[1][1])
        self.assertEqual("1915576430", mapping[1][0])
        self.assertEqual("Italmed", mapping[2][1])
        self.assertEqual("1915576432", mapping[2][0])
        self.assertEqual("EECA", mapping[3][1])
        self.assertEqual("1915576433", mapping[3][0])
        self.assertEqual("SAMed", mapping[4][1])
        self.assertEqual("1915576434", mapping[4][0])
        self.assertEqual("South American", mapping[5][1])
        self.assertEqual("1915576435", mapping[5][0])
        self.assertEqual("YugoGreek", mapping[6][1])
        self.assertEqual("1915576436", mapping[6][0])
        self.assertEqual("African", mapping[7][1])
        self.assertEqual("1915576437", mapping[7][0])
        self.assertEqual("African", mapping[8][1])
        self.assertEqual("1915576438", mapping[8][0])
        self.assertEqual("African", mapping[9][1])
        self.assertEqual("1915576439", mapping[9][0])
        self.assertEqual("African", mapping[10][1])
        self.assertEqual("1915576440", mapping[10][0])
        self.assertEqual("African", mapping[11][1])
        self.assertEqual("1915576441", mapping[11][0])
        self.assertEqual("Asian", mapping[12][1])
        self.assertEqual("1915576442", mapping[12][0])
        self.assertEqual("MENA", mapping[13][1])
        self.assertEqual("1915576444", mapping[13][0])
        self.assertEqual("Seasian", mapping[14][1])
        self.assertEqual("1915576445", mapping[14][0])
        self.assertEqual("Scandinavian", mapping[15][1])
        self.assertEqual("1915576446", mapping[15][0])
        self.assertEqual("Caucasian", mapping[16][1])
        self.assertEqual("1915576447", mapping[16][0])
        self.assertEqual("Central European", mapping[17][1])
        self.assertEqual("1915576448", mapping[17][0])
        self.assertEqual("MESA", mapping[18][1])
        self.assertEqual("1915576450", mapping[18][0])

    def test_generate_mapping_double(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Generate")
        next_mapping = self.mapper.generate_mapping(self.data_simple, "Generate")
        self.assertNotEqual(simple_mapping, next_mapping)


class Test_Mapper_Preserve_Mapping(unittest.TestCase):
    def setUp(self):
        # TODO: we need prf_map, prf_imgs and prf_eth_map
        self.rtfparser = RTF_Parser()
        self.pm = Profile_Manager("No Profile", "newganmanager/testing/")
        self.mapper = Mapper("newganmanager/test/", self.pm)
        self.pm.prf_cfg["img_dir"] = "newganmanager/test/"
        # data: UID, first_nat, sec_nat, eth-code
        self.data_simple = self.rtfparser.parse_rtf("newganmanager/test/test_simple.rtf")
        self.data_all_cases = self.rtfparser.parse_rtf("newganmanager/test/test_allcases.rtf")
        self.data_subset1 = self.rtfparser.parse_rtf("newganmanager/test/allcases_subset1.rtf")
        self.data_subset2 = self.rtfparser.parse_rtf("newganmanager/test/allcases_subset2.rtf")
        self.data_exclusive = self.rtfparser.parse_rtf("newganmanager/test/test_exclusive.rtf")
        for eth in ["African", "Asian", "EECA", "Italmed", "SAMed", "South American", 
                    "SpanMed", "YugoGreek", "MENA", "MESA", "Caucasian", "Central European",
                    "Scandinavian", "Seasian"]:
            map = [eth+str(i)for i in range(20)]
            self.mapper.eth_map[eth] = map

    def tearDown(self):
        shutil.rmtree("newganmanager/testing/.config/")
        shutil.copytree("newganmanager/.config/", "newganmanager/testing/.config/")
        shutil.rmtree("newganmanager/testing/.user/")
        shutil.copytree("newganmanager/.user/", "newganmanager/testing/.user/")
        with open("newganmanager/test/config.xml", "w") as cfg:
            cfg.write('OUTSIDE')

    def test_preserve_mapping_simple(self):
        mapping = self.mapper.generate_mapping(self.data_simple, "Preserve")
        self.assertEqual("SpanMed", mapping[0][1])
        self.assertEqual("1915714540", mapping[0][0])
        self.assertEqual("MESA", mapping[1][1])
        self.assertEqual("1915576430", mapping[1][0])

    def test_preserve_mapping_all_cases(self):
        mapping = self.mapper.generate_mapping(self.data_all_cases, "Preserve")
        self.assertEqual("SpanMed", mapping[0][1])
        self.assertEqual("1915714540", mapping[0][0])
        self.assertEqual("MESA", mapping[1][1])
        self.assertEqual("1915576430", mapping[1][0])
        self.assertEqual("Italmed", mapping[2][1])
        self.assertEqual("1915576432", mapping[2][0])
        self.assertEqual("EECA", mapping[3][1])
        self.assertEqual("1915576433", mapping[3][0])
        self.assertEqual("SAMed", mapping[4][1])
        self.assertEqual("1915576434", mapping[4][0])
        self.assertEqual("South American", mapping[5][1])
        self.assertEqual("1915576435", mapping[5][0])
        self.assertEqual("YugoGreek", mapping[6][1])
        self.assertEqual("1915576436", mapping[6][0])
        self.assertEqual("African", mapping[7][1])
        self.assertEqual("1915576437", mapping[7][0])
        self.assertEqual("African", mapping[8][1])
        self.assertEqual("1915576438", mapping[8][0])
        self.assertEqual("African", mapping[9][1])
        self.assertEqual("1915576439", mapping[9][0])
        self.assertEqual("African", mapping[10][1])
        self.assertEqual("1915576440", mapping[10][0])
        self.assertEqual("African", mapping[11][1])
        self.assertEqual("1915576441", mapping[11][0])
        self.assertEqual("Asian", mapping[12][1])
        self.assertEqual("1915576442", mapping[12][0])
        self.assertEqual("MENA", mapping[13][1])
        self.assertEqual("1915576444", mapping[13][0])
        self.assertEqual("Seasian", mapping[14][1])
        self.assertEqual("1915576445", mapping[14][0])
        self.assertEqual("Scandinavian", mapping[15][1])
        self.assertEqual("1915576446", mapping[15][0])
        self.assertEqual("Caucasian", mapping[16][1])
        self.assertEqual("1915576447", mapping[16][0])
        self.assertEqual("Central European", mapping[17][1])
        self.assertEqual("1915576448", mapping[17][0])
        self.assertEqual("MESA", mapping[18][1])
        self.assertEqual("1915576450", mapping[18][0])

    def test_preserve_mapping_double(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Preserve")
        self.pm.write_xml(simple_mapping)
        next_mapping = self.mapper.generate_mapping(self.data_simple, "Preserve")
        self.pm.write_xml(next_mapping)
        self.assertSequenceEqual(simple_mapping, next_mapping)

    def test_preserve_mapping_double_exclusive(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Preserve")
        self.pm.write_xml(simple_mapping)
        next_mapping = self.mapper.generate_mapping(self.data_exclusive, "Preserve")
        self.pm.write_xml(next_mapping)
        self.assertEqual(simple_mapping, next_mapping[2:])
        self.assertEqual(len(next_mapping), 4)

    def test_preserve_mapping_complete_subset(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Preserve")
        self.pm.write_xml(simple_mapping)
        next_mapping = self.mapper.generate_mapping(self.data_all_cases, "Preserve")
        self.pm.write_xml(next_mapping)
        self.assertEqual(simple_mapping, next_mapping[:2])

    def test_preserve_mapping_complete_subset_reverse(self):
        next_mapping = self.mapper.generate_mapping(self.data_all_cases, "Preserve")
        self.pm.write_xml(next_mapping)
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Preserve")
        self.pm.write_xml(simple_mapping)
        self.assertEqual(simple_mapping, next_mapping)

    def test_preserve_mapping_partial_subset(self):
        sub2_mapping = self.mapper.generate_mapping(self.data_subset2, "Preserve")
        self.pm.write_xml(sub2_mapping)
        sub1_mapping = self.mapper.generate_mapping(self.data_subset1, "Preserve")
        self.pm.write_xml(sub1_mapping)
        self.assertEqual(sub1_mapping[:5], sub2_mapping[:5])
        self.assertIn(sub2_mapping[5], sub1_mapping)
        self.assertIn(sub2_mapping[6], sub1_mapping)
        self.assertIn(sub2_mapping[7], sub1_mapping)
        self.assertIn(sub2_mapping[8], sub1_mapping)
        self.assertIn(sub2_mapping[9], sub1_mapping)
        self.assertEqual(len(sub1_mapping), 12)

    def test_preserve_mapping_partial_subset_reverse(self):
        sub1_mapping = self.mapper.generate_mapping(self.data_subset1, "Preserve")
        self.pm.write_xml(sub1_mapping)
        sub2_mapping = self.mapper.generate_mapping(self.data_subset2, "Preserve")
        self.pm.write_xml(sub2_mapping)
        self.assertEqual(sub1_mapping[:5], sub2_mapping[:5])
        self.assertEqual(len(sub2_mapping), 12)


class Test_Mapper_Overwrite_Mapping(unittest.TestCase):
    def setUp(self):
        # TODO: we need prf_map, prf_imgs and prf_eth_map
        self.rtfparser = RTF_Parser()
        self.pm = Profile_Manager("No Profile", "newganmanager/testing/")
        self.mapper = Mapper("newganmanager/test/", self.pm)
        self.pm.prf_cfg["img_dir"] = "newganmanager/test/"
        # data: UID, first_nat, sec_nat, eth-code
        self.data_simple = self.rtfparser.parse_rtf("newganmanager/test/test_simple.rtf")
        self.data_all_cases = self.rtfparser.parse_rtf("newganmanager/test/test_allcases.rtf")
        self.data_subset1 = self.rtfparser.parse_rtf("newganmanager/test/allcases_subset1.rtf")
        self.data_subset2 = self.rtfparser.parse_rtf("newganmanager/test/allcases_subset2.rtf")
        self.data_exclusive = self.rtfparser.parse_rtf("newganmanager/test/test_exclusive.rtf")

        for eth in ["African", "Asian", "EECA", "Italmed", "SAMed", "South American",
                    "SpanMed", "YugoGreek", "MENA", "MESA", "Caucasian", "Central European",
                    "Scandinavian", "Seasian"]:
            map = [eth+str(i)for i in range(20)]
            self.mapper.eth_map[eth] = map

    def tearDown(self):
        shutil.rmtree("newganmanager/testing/.config/")
        shutil.copytree("newganmanager/.config/", "newganmanager/testing/.config/")
        shutil.rmtree("newganmanager/testing/.user/")
        shutil.copytree("newganmanager/.user/", "newganmanager/testing/.user/")
        with open("newganmanager/test/config.xml", "w") as cfg:
            cfg.write('OUTSIDE')

    def test_overwrite_mapping_simple(self):
        mapping = self.mapper.generate_mapping(self.data_simple, "Overwrite")
        self.assertEqual("SpanMed", mapping[0][1])
        self.assertEqual("1915714540", mapping[0][0])
        self.assertEqual("MESA", mapping[1][1])
        self.assertEqual("1915576430", mapping[1][0])

    def test_overwrite_mapping_all_cases(self):
        mapping = self.mapper.generate_mapping(self.data_all_cases, "Overwrite")
        self.assertEqual("SpanMed", mapping[0][1])
        self.assertEqual("1915714540", mapping[0][0])
        self.assertEqual("MESA", mapping[1][1])
        self.assertEqual("1915576430", mapping[1][0])
        self.assertEqual("Italmed", mapping[2][1])
        self.assertEqual("1915576432", mapping[2][0])
        self.assertEqual("EECA", mapping[3][1])
        self.assertEqual("1915576433", mapping[3][0])
        self.assertEqual("SAMed", mapping[4][1])
        self.assertEqual("1915576434", mapping[4][0])
        self.assertEqual("South American", mapping[5][1])
        self.assertEqual("1915576435", mapping[5][0])
        self.assertEqual("YugoGreek", mapping[6][1])
        self.assertEqual("1915576436", mapping[6][0])
        self.assertEqual("African", mapping[7][1])
        self.assertEqual("1915576437", mapping[7][0])
        self.assertEqual("African", mapping[8][1])
        self.assertEqual("1915576438", mapping[8][0])
        self.assertEqual("African", mapping[9][1])
        self.assertEqual("1915576439", mapping[9][0])
        self.assertEqual("African", mapping[10][1])
        self.assertEqual("1915576440", mapping[10][0])
        self.assertEqual("African", mapping[11][1])
        self.assertEqual("1915576441", mapping[11][0])
        self.assertEqual("Asian", mapping[12][1])
        self.assertEqual("1915576442", mapping[12][0])
        self.assertEqual("MENA", mapping[13][1])
        self.assertEqual("1915576444", mapping[13][0])
        self.assertEqual("Seasian", mapping[14][1])
        self.assertEqual("1915576445", mapping[14][0])
        self.assertEqual("Scandinavian", mapping[15][1])
        self.assertEqual("1915576446", mapping[15][0])
        self.assertEqual("Caucasian", mapping[16][1])
        self.assertEqual("1915576447", mapping[16][0])
        self.assertEqual("Central European", mapping[17][1])
        self.assertEqual("1915576448", mapping[17][0])
        self.assertEqual("MESA", mapping[18][1])
        self.assertEqual("1915576450", mapping[18][0])

    def test_overwrite_mapping_double(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Overwrite")
        self.pm.write_xml(simple_mapping)
        next_mapping = self.mapper.generate_mapping(self.data_simple, "Overwrite")
        self.pm.write_xml(next_mapping)
        self.assertNotEqual(simple_mapping, next_mapping)

    def test_overwrite_mapping_double_exclusive(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Overwrite")
        self.pm.write_xml(simple_mapping)
        next_mapping = self.mapper.generate_mapping(self.data_exclusive, "Overwrite")
        self.pm.write_xml(next_mapping)
        self.assertEqual(simple_mapping, next_mapping[2:])
        self.assertEqual(len(next_mapping), 4)

    def test_overwrite_mapping_complete_subset(self):
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Overwrite")
        self.pm.write_xml(simple_mapping)
        next_mapping = self.mapper.generate_mapping(self.data_all_cases, "Overwrite")
        self.pm.write_xml(next_mapping)
        self.assertNotEqual(simple_mapping, next_mapping[:2])

    def test_overwrite_mapping_complete_subset_reverse(self):
        next_mapping = self.mapper.generate_mapping(self.data_all_cases, "Overwrite")
        self.pm.write_xml(next_mapping)
        simple_mapping = self.mapper.generate_mapping(self.data_simple, "Overwrite")
        self.pm.write_xml(simple_mapping)
        self.assertNotEqual(simple_mapping, next_mapping[:2])
        self.assertEqual(next_mapping[2:], simple_mapping[2:])

    def test_overwrite_mapping_partial_subset(self):
        sub2_mapping = self.mapper.generate_mapping(self.data_subset2, "Overwrite")
        self.pm.write_xml(sub2_mapping)
        sub1_mapping = self.mapper.generate_mapping(self.data_subset1, "Overwrite")
        self.pm.write_xml(sub1_mapping)
        self.assertNotEqual(sub1_mapping[:5], sub2_mapping[:5])
        self.assertIn(sub2_mapping[5], sub1_mapping)
        self.assertIn(sub2_mapping[6], sub1_mapping)
        self.assertIn(sub2_mapping[7], sub1_mapping)
        self.assertIn(sub2_mapping[8], sub1_mapping)
        self.assertIn(sub2_mapping[9], sub1_mapping)
        self.assertEqual(len(sub1_mapping), 12)

    def test_overwrite_mapping_partial_subset_reverse(self):
        sub1_mapping = self.mapper.generate_mapping(self.data_subset1, "Overwrite")
        self.pm.write_xml(sub1_mapping)
        sub2_mapping = self.mapper.generate_mapping(self.data_subset2, "Overwrite")
        self.pm.write_xml(sub2_mapping)
        self.assertNotEqual(sub1_mapping[:5], sub2_mapping[:5])
        self.assertEqual(len(sub2_mapping), 12)


if __name__ == '__main__':
    unittest.main()
