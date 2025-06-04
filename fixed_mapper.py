import os
import random
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

        logger = logging.getLogger('NewGAN App')
        self.logger = logger

    def generate_mapping(self, rtf_data, mode, duplicates=False):
        mapping = []
        prf_imgs = []
        xml_data = {}

        if mode in ["Preserve", "Overwrite"]:
            xml_parser = XML_Parser()
            xml_data = xml_parser.parse_xml(self.img_dir+"config.xml")
            prf_imgs = self.get_xml_images(xml_data)

            if not duplicates:
                for eth in self.eth_map:
                    self.eth_map[eth] = self.eth_map[eth] - set(prf_imgs)

        # Ülke kodlarının etnik köken eşleştirmeleri
        country_ethnicity_map = {
            # Avrupa
            "ALM": "Europeans", "AUS": "Europeans", "AZE": "Europeans", "BEL": "Europeans", "BLR": "Europeans", 
            "BOS": "Europeans", "BUL": "Europeans", "CEZ": "Europeans", "DAN": "Europeans", "EST": "Europeans",
            "FRA": "Europeans", "HIR": "Europeans", "HOL": "Europeans", "LET": "Europeans", "LİT": "Europeans",
            "LÜK": "Europeans", "MAC": "Europeans", "MOL": "Europeans", "NOR": "Scandinavians", "POL": "Europeans",
            "POR": "Europeans", "ROM": "Europeans", "RUS": "Europeans", "SVK": "Europeans", "SVN": "Europeans",
            "UKR": "Europeans", "YUN": "Europeans", "ÇEK": "Europeans", "İSV": "Scandinavians", "İTA": "Europeans",
            "İRL": "British_Irish", "İNG": "British_Irish", "GAL": "British_Irish", "İSK": "British_Irish", "FİN": "Scandinavians",
            "AND": "Europeans", "LİH": "Europeans", "İZL": "Scandinavians", "SMR": "Europeans", "SUI": "Europeans",

            # İspanyolca konuşan ülkeler
            "İSP": "South Americans", "ARJ": "South Americans", "BOL": "South Americans", "ŞİL": "South Americans", 
            "KOL": "South Americans", "EKV": "South Americans", "PAR": "South Americans", "PER": "South Americans", 
            "URU": "South Americans", "VEN": "South Americans", "MEK": "South Americans", "KÜB": "South Americans",
            "DOM": "South Americans", "HON": "South Americans", "SLV": "South Americans", "NİK": "South Americans", 
            "KOS": "South Americans", "PAN": "South Americans", "PUR": "South Americans", "GUA": "South Americans",
            
            # Asya ülkeleri
            "ÇİN": "Asians", "JPN": "Asians", "KOR": "Asians", "VİE": "Asians", "TPE": "Asians",
            "MYA": "Asians", "FİL": "Asians", "MAS": "Asians", "END": "Asians", "SUA": "Asians",
            "PAK": "Asians", "HİN": "Asians", "NEP": "Asians", "TJK": "Asians", "KGZ": "Asians",
            "MDV": "Asians", "BHU": "Asians", "SGP": "Asians", "BRU": "Asians", "KAZ": "Asians",
            "ÖZB": "Asians", "TLS": "Asians", "MİK": "Asians", "KİR": "Asians", "FİJ": "Asians",
            "TGA": "Asians", "SMN": "Asians", "COK": "Asians", "GUM": "Asians", "BAN": "Asians",
            "LAO": "Asians", "THAİ": "Asians", "MOĞ": "Asians",
            
            # Kuzey Afrika ve Orta Doğu
            "FAS": "North Africans", "TUN": "North Africans", "CEZ": "North Africans", "MIS": "North Africans", 
            "SUD": "North Africans", "ÜRD": "North Africans", "LÜB": "North Africans", "SRY": "North Africans", 
            "İSR": "North Africans", "TÜR": "North Africans", "IRK": "North Africans", "BAE": "North Africans",
            "İRN": "North Africans", "KUV": "North Africans", "KAT": "North Africans", "BHR": "North Africans", 
            "YEM": "North Africans", "UMA": "North Africans", "LBY": "North Africans", "ERİ": "North Africans",

            # Afrika
            "GAN": "Africans", "SEN": "Africans", "FİL": "Africans", "NİA": "Africans", "KAM": "Africans", 
            "ANG": "Africans", "CFA": "Africans", "KDC": "Africans", "GAB": "Africans", "GAM": "Africans", 
            "KDĞ": "Africans", "KEN": "Africans", "MLİ": "Africans", "UGA": "Africans", "ZİM": "Africans",
            "AFG": "Africans", "BEN": "Africans", "BFA": "Africans", "BDI": "Africans", "ÇAD": "Africans", 
            "ETİ": "Africans", "GİN": "Africans", "GNB": "Africans", "LBR": "Africans", "MOZ": "Africans", 
            "NAM": "Africans", "NİE": "Africans", "SLE": "Africans", "TOG": "Africans", "ZAN": "Africans",
            "ZAM": "Africans", "BOT": "Africans", "SOM": "Africans", "TAN": "Africans", "MWİ": "Africans",
            "MAD": "Africans", "STP": "Africans", "SEY": "Africans", "KMA": "Africans", "LES": "Africans",
            "MOR": "Africans"
        }

        for i, player in enumerate(rtf_data):
            p_ethnic = None
            n2_ethnic = None
            
            if player[2]:
                n2_ethnic = self.profile_manager.get_ethnic(player[2])
                
            n1_ethnic = self.profile_manager.get_ethnic(player[1])
            
            # Eğer get_ethnic bir değer döndürmediyse, kendi mapping'imizi kullanabiliriz
            if n1_ethnic is None:
                if player[1] in country_ethnicity_map:
                    n1_ethnic = country_ethnicity_map[player[1]]
                    self.logger.info("Using custom mapping for {} -> {}. Processing player {}".format(player[1], n1_ethnic, player[0]))
                else:
                    self.logger.info("Mapping for {} is missing. Skipping player {}".format(player[1], player[0]))
                    continue
                    
            # Eski tekil formdan çoğul forma çevirme
            if n1_ethnic == "Scandinavian":
                n1_ethnic = "Scandinavians"
            elif n1_ethnic == "European":
                n1_ethnic = "Europeans"
                
            if n2_ethnic == "Scandinavian":
                n2_ethnic = "Scandinavians"
            elif n2_ethnic == "European":
                n2_ethnic = "Europeans"
                
            self.logger.info("{}/{}: {}, {}, {}".format(i, len(rtf_data), player, n1_ethnic, n2_ethnic))
            
            if int(player[3]) > 10:
                self.logger.info("Ethnic value {} is invalid. Most likely a bug in the view. Skipping player {}".format(player[3], player[0]))
                continue
                
            # if player is in config.xml and we use preserver or overwrite handle it properly
            if player[0] in xml_data:
                if mode == "Preserve":
                    self.logger.info("Preserve: {} {} {}".format(player[0], xml_data[player[0]]["ethnicity"], xml_data[player[0]]["image"]))
                    continue
                elif mode == "Overwrite":
                    prf_imgs.remove(xml_data[player[0]]["image"])
                    del xml_data[player[0]]
                    
            # Oyuncu etnik kökeni tespit et
            if player[3] == "1":
                if "Scandinavians" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "Asians" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "Europeans" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "British_Irish" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "Africans" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "North Africans" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "MESA" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
                if "South Americans" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "South Americans"
            elif player[3] in ["3", "6", "8", "9"]:
                p_ethnic = "Africans"
            elif player[3] == "7":
                # South Americans with 7 is light-skinned
                if "South Americans" == n1_ethnic:
                    p_ethnic = "South Americans"
                else:
                    p_ethnic = "Africans"
            elif player[3] == "10":
                if "South Americans" == n1_ethnic:
                    p_ethnic = "South Americans"
                else:
                    p_ethnic = "Asians"
            elif player[3] == "2":
                p_ethnic = "North Africans"
            elif player[3] == "5":
                p_ethnic = "Asians"
            elif player[3] == "0":
                p_ethnic = "Europeans"
                if "Scandinavians" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "Scandinavians"
                elif "British_Irish" in [n1_ethnic, n2_ethnic]:
                    p_ethnic = "British_Irish"
            elif player[3] == "4":
                p_ethnic = "North Africans"

            # pick image based on p_ethnic
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
        # Eski etnik köken isimlerini yeni klasör adlarına eşleştirme
        ethnicity_map = {
            "Central European": "Europeans",
            "EECA": "Europeans", 
            "Caucasian": "British_Irish",
            "SpanMed": "South Americans", 
            "Italmed": "Europeans",
            "SAMed": "South Americans", 
            "YugoGreek": "Europeans",
            "MENA": "North Africans",
            "MESA": "North Africans",
            "Seasian": "Asians", 
            "African": "Africans",
            "Asian": "Asians",
            "South American": "South Americans",
            "Scandinavian": "Scandinavians",
            # Tekil formları da ekleyelim
            "European": "Europeans",
            "Scandinavians": "Scandinavians",
            "British_Irish": "British_Irish",
            "South Americans": "South Americans",
            "North African": "North Africans",
            "North Africans": "North Africans",
            "Africans": "Africans",
            "Asians": "Asians"
        }
        
        # None değerlerini işle veya eski isimleri yenileriyle değiştir
        if ethnicity is None:
            self.logger.info("Ethnicity is None, using Europeans as fallback")
            ethnicity = "Europeans"  # Fallback olarak Europeans kullan
        elif ethnicity in ethnicity_map:
            ethnicity = ethnicity_map[ethnicity]
            
        # Eşleşmeyen bir etnik köken adı varsa, güvenli bir alternatif seç
        if ethnicity not in self.eth_map:
            self.logger.info(f"Unknown ethnicity {ethnicity}, using Europeans as fallback")
            ethnicity = "Europeans"  # Eşleşmeyen bir etnik köken için fallback
            
            # ethnicity'nin eth_map içinde olup olmadığını kontrol et
            if ethnicity not in self.eth_map:
                self.logger.info(f"'{ethnicity}' not found in eth_map, using Europeans as fallback")
                ethnicity = "Europeans"  # Fallback olarak Europeans kullan
                # Eğer Europeans de yoksa, None döndür
                if ethnicity not in self.eth_map:
                    self.logger.info("Europeans folder not found. Check folder structure.")
                    return None

        selection_pool = self.eth_map[ethnicity]
        if len(selection_pool) == 0:
            self.logger.info(f"No faces left in {ethnicity}. Using Europeans as fallback.")
            # Europeans klasöründen seçmeyi dene
            if "Europeans" in self.eth_map and len(self.eth_map["Europeans"]) > 0:
                selection_pool = self.eth_map["Europeans"]
            else:
                # Hiç resim kalmadı
                return None

        choice = random.choice(tuple(selection_pool)) if len(selection_pool) > 0 else None
        if choice is not None and not duplicates:
            selection_pool.remove(choice)
        return choice

    def post_rtf_hook(self, mapping, prf_imgs, xml_data):
        for uid, values in xml_data.items():
            p_ethnic = values["ethnicity"]
            player_img = values["image"]
            mapping.append([uid, p_ethnic, player_img])
