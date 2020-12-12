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
        logger = logging.getLogger('NewGAN Logger')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('newgan.log')
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        self.logger = logger

    def generate_mapping(self, rtf_data, mode):
        mapping = []
        prf_imgs = []
        xml_data = {}

        if mode in ["Preserve", "Overwrite"]:
            xml_parser = XML_Parser()
            xml_data = xml_parser.parse_xml(self.img_dir+"config.xml")
            prf_imgs = self.get_xml_images(xml_data)

        for i, player in enumerate(rtf_data):
            n2_ethnic = None
            if player[2]:
                n2_ethnic = self.profile_manager.get_ethnic(player[2])
            n1_ethnic = self.profile_manager.get_ethnic(player[1])
            if n1_ethnic is None:
                self.logger.info("Mapping for {} is missing. Skipping player {}".format(player[1], player[0]))
                continue
            # self.logger.info("{}, {}, {}".format(player, n1_ethnic, n2_ethnic))
            if player[3] == "1":
                if "EECA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "EECA"
                elif "Italmed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "Italmed"
                elif "SAMed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "SAMed"
                elif "SpanMed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "SpanMed"
                elif "YugoGreek" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "YugoGreek"
                else:
                    p_ethnic = "South American"
            elif player[3] in ["3", "6", "7", "8", "9"]:
                p_ethnic = "African"
            elif player[3] == "10":
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

            player_img = self.pick_image(p_ethnic, prf_imgs)
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

    def pick_image(self, ethnicity, profile_images):
        eth_imgs = self.eth_map[ethnicity]
        selection_pool = set(eth_imgs) - set(profile_images)
        if len(selection_pool) == 0:
            return None
        return random.choice(tuple(selection_pool))

    def post_rtf_hook(self, mapping, prf_imgs, xml_data):
        for uid, values in xml_data.items():
            p_ethnic = values["ethnicity"]
            player_img = values["image"]
            mapping.append([uid, p_ethnic, player_img])
