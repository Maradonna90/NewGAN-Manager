import random
import os
from xmlparser import XML_Parser
import logging


class Mapper:
    def __init__(self, img_dir, prf_manager):
        self.img_dir = img_dir
        self.profile_manager = prf_manager
        self.eth_map = {}
        eth_dirs = [f.name for f in os.scandir(img_dir) if f.is_dir()]
        for dir in eth_dirs:
            dir_imgs = set([f.name.split('.')[0] for f in os.scandir(img_dir+dir) if f.is_file()])
            self.eth_map[dir] = dir_imgs

        formatter = logging.Formatter("%(asctime)s | %(name)s: %(message)s")
        fh = logging.FileHandler('newgan.log')
        fh.setFormatter(formatter)
        logger = logging.getLogger('NewGAN Mapper')
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        self.logger = logger

    def generate_mapping(self, rtf_data, mode, duplicates=False):
        mapping = []
        prf_imgs = []
        xml_data = {}

        if mode in ["Preserve", "Overwrite"]:
            xml_parser = XML_Parser()
            xml_data = xml_parser.parse_xml(self.img_dir+"config.xml")
            prf_imgs = self.get_xml_images(xml_data)

            for eth in self.eth_map:
                self.eth_map[eth] = self.eth_map[eth] - set(prf_imgs)

        for i, player in enumerate(rtf_data):
            p_ethnic = None
            n2_ethnic = None
            if player[2]:
                n2_ethnic = self.profile_manager.get_ethnic(player[2])
            n1_ethnic = self.profile_manager.get_ethnic(player[1])
            if n1_ethnic is None:
                self.logger.info("Mapping for {} is missing. Skipping player {}".format(player[1], player[0]))
                continue
            self.logger.info("{}/{}: {}, {}, {}".format(i, len(rtf_data), player, n1_ethnic, n2_ethnic))
            if int(player[3]) > 10:
                self.logger.info("Ethnic value {} is invalid. Most likely a bug in the view. Skipping player {}".format(player[3], player[0]))
                continue
            if player[3] == "1":
                if "Scandinavian" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "Seasian" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "Central European" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "Caucasian" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "African" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "Asian" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "MENA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "MESA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "EECA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "EECA"
                if "Italmed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "Italmed"
                if "SAMed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "SAMed"
                if "SpanMed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "SpanMed"
                if "YugoGreek" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "YugoGreek"
                if "South American" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
            elif player[3] in ["3", "6", "7", "8", "9"]:
                # SAMed with 7 is light-skinned
                if "SAMed" == n1_ethnic and player[3] == "7":
                    p_ethnic = "SAMed"
                # South American with 7 is light-skinned
                elif "South American" == n1_ethnic and player[3] == "7":
                    p_ethnic = "South American"
                else:
                    p_ethnic = "African"
            elif player[3] == "10":
                if "South American" == n1_ethnic:
                    p_ethnic = "South American"
                else:
                    p_ethnic = "Asian"
            elif player[3] == "2":
                p_ethnic = "MENA"
                if "MESA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "MESA"
            elif player[3] == "5":
                p_ethnic = "Seasian"
            elif player[3] == "0":
                p_ethnic = "Central European"
                if "Scandinavian" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "Scandinavian"
                elif "Caucasian" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "Caucasian"
            elif player[3] == "4":
                p_ethnic = "MESA"
            if player[0] in xml_data:
                if mode == "Preserve":
                    # self.logger.info("Preserve: {} {} {}".format(player[0], p_ethnic, xml_data[player[0]]["image"]))
                    mapping.append([player[0], p_ethnic, xml_data[player[0]]["image"]])
                    del xml_data[player[0]]
                    continue
                elif mode == "Overwrite":
                    # self.logger.info("Overwrite: {} {}".format(player[0], p_ethnic))
                    prf_imgs.remove(xml_data[player[0]]["image"])
                    del xml_data[player[0]]
            player_img = self.pick_image(p_ethnic, duplicates)
            prf_imgs.append(player_img)
            if player_img is None:
                self.logger.info("Ethnicity {} has no faces left for mapping. Skipping player {}".format(p_ethnic, player[0]))
                continue
            mapping.append([player[0], p_ethnic, player_img])
        if mode in ["Overwrite", "Preserve"]:
            self.post_rtf_hook(mapping, prf_imgs, xml_data)
        return mapping

    def get_xml_images(self, xml_data):
        return [i["image"] for i in xml_data.values()]

    def pick_image(self, ethnicity, duplicates=False):
        selection_pool = self.eth_map[ethnicity]
        if len(selection_pool) == 0:
            return None
        choice = random.choice(tuple(selection_pool))

        if not duplicates:
            selection_pool.remove(choice)

        return choice

    def post_rtf_hook(self, mapping, prf_imgs, xml_data):
        for uid, values in xml_data.items():
            p_ethnic = values["ethnicity"]
            player_img = values["image"]
            mapping.append([uid, p_ethnic, player_img])
