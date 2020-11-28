import re


class XML_Parser:
    def __init__(self):
        pass

    def parse_xml(self, path):
        UID_regex = re.compile('([0-9]{10}(?=\/))')
        eth_img_regex = re.compile('((?<=from=\").*(?=\" to))')
        result_data = []
        xml = open(path, 'r', encoding="UTF-8")
        # self.logger.info(rtf)
        result_data = []
        for line in xml:
            if UID_regex.search(line):
                uid = UID_regex.search(line).group(0).strip()
                eth_img = eth_img_regex.search(line)
                eth_img = eth_img.group(0).strip().split("/")
                img = eth_img[1]
                eth = eth_img[0]
                # self.logger.info(line.strip())
                result_data.append([uid, eth, img])
        xml.close()
        return result_data
