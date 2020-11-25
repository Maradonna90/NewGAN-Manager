import random


class Mapper:
    def __init__(self):
        pass

    def generate_mapping(self, rtf_data, mode, prf_map, prf_imgs):
        for i, player in enumerate(rtf_data):
            n2_ethnic = None
            if player[2]:
                # print("DO 2nd!")
                n2_ethnic = self.config["Ethnics"][player[2]]
            n1_ethnic = self.config["Ethnics"][player[1]]
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
            eth_imgs = set([f.name for f in os.scandir(self.prf_cfg['img_dir']+p_ethnic) if f.is_file()])
            selection_pool = eth_imgs - prf_imgs
            player_img = random.choice(tuple(selection_pool))
            prf_map[player[0]] = player_img
            prf_eth_map[player[0]] = p_ethnic
            prf_imgs.add(player_img)
            player_img = player_img.split('.')[0]
            return generate_mapping

