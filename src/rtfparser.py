import re


class RTF_Parser:
    def __init__(self):
        pass

    def parse_rtf(self, path):
        UID_regex = re.compile('([0-9]){10}')
        result_data = []
        rtf = open(path, 'r', encoding="UTF-8")
        # self.logger.info(rtf)
        rtf_data = []
        for line in rtf:
            if UID_regex.search(line):
                # self.logger.info(line.strip())
                rtf_data.append(line.strip())
        for newgen in rtf_data:
            data_fields = newgen.split('|')
            sec_nat = data_fields[3].strip()
            if sec_nat == '':
                sec_nat = None
            result_data.append([data_fields[1].strip(), data_fields[2].strip(), sec_nat, data_fields[7].strip()])
        rtf.close()
        return result_data
