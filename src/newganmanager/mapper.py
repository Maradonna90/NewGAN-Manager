import random
import os
from xmlparser import XML_Parser

class Mapper:
    def __init__(self, img_dir, prf_manager):
        self.img_dir = img_dir
        self.prf_manager = prf_manager
        self.eth_map = {}
        eth_dirs = [f.name for f in os.scandir(img_dir) if f.is_dir()]
        for dir in eth_dirs:
            dir_imgs = set([f.name for f in os.scandir(img_dir+dir) if f.is_file()])
            self.eth_map[dir] = dir_imgs

    def generate_mapping(self, rtf_data, mode, prf_map, prf_imgs, prf_eth_map):
        mapping = []
        # TODO: create Parser for config.xml in img_dir to retrieve already mapped players
        # if preserve or overwrite: append to mapping file
        prf_uids = []
        if mode in ["Preserve", "Overwrite"]:
            xml_parser = XML_Parser()
            xml_data = xml_parser.parse_xml(self.img_dir+"config.xml")
            # pick random image
            prf_imgs = [i[2] for i in xml_data]
            prf_uids = [i[0] for i in xml_data]
            mapping.append(xml_data)

        for i, player in enumerate(rtf_data):
            n2_ethnic = None
            if player[2]:
                n2_ethnic = self.profile_manager.get_ethnic(player[2])
            n1_ethnic = self.profile_manager.get_ethnic(player[1])
            if n1_ethnic is None:
                self.logger.info("Mapping for {} is missing. Skipping player {}".format(player[1], player[0]))
                continue
            if player[3] == "1":
                if "EECA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "EECA"
                if "Italmed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "Italmed"
                if "SAMed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "SAMed"
                if "South American" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South American"
                if "SpanMed" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "SpanMed"
                if "YugoGreek" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "YugoGreek"
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
            if player[0] in prf_map:
                if mode == "Preserve":
                    self.logger.info("Preserve: {} {}".format(i, p_ethnic))
                    self.gen_prg.value += 1
                    continue
                elif mode == "Overwrite":
                    self.logger.info("Overwrite: {} {}".format(i, p_ethnic))
                    player_img = prf_map[player[0]]
                    prf_imgs.remove(player_img)
            prf_map[player[0]] = player_img
            prf_eth_map[player[0]] = p_ethnic
            player_img = self.pick_image(p_ethnic, prf_imgs)
            if player_img is None:
                self.logger.info("Ethnicity {} has no faces left for mapping. Skipping player {}".format(p_ethnic, player[0]))
                continue
            prf_imgs.add(player_img)
            player_img = player_img.split('.')[0]
            mapping.append([player[0], p_ethnic, player_img])
        return mapping

        def pick_image(self, ethnicity, profile_images, img_dir):
            eth_imgs = self.eth_map[ethnicity]
            selection_pool = eth_imgs - prf_imgs
            return random.choice(tuple(selection_pool))
