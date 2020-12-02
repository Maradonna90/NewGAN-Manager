import config_manager
import os
from shutil import copyfileobj


class Profile_Manager(config_manager.Config_Manager):
    def __init__(self, path, name):
        self.config = self.load_config(path)
        self.prf_cfg = self.load_config(".config/"+name+".json")
        self.cur_prf = name

    def migrate_config(self):
        if "Profile" in self.config:
            profiles = self.config["Profile"]
            self.save_config(".user/cfg.json", profiles)
            del self.config["Profile"]
            self.save_config(".config/cfg.json", self.config)
            for profile in profiles.keys():
                with open(".user/"+profile+'.xml', 'wb') as output, open('.config/'+profile+'.xml', 'rb') as input:
                    copyfileobj(input, output)
                    os.remove('.config/'+profile+'.xml')
                with open(".user/"+profile+'.json', 'wb') as output, open('.config/'+profile+'.json', 'rb') as input:
                    copyfileobj(input, output)
                    os.remove('.config/'+profile+'.json')

    def delete_profile(self, name):
        # self.logger.info("Delete profile: {}".format(name))
        if name == "No Profile":
            # self.logger.info("Can't delet no profile")
            self._throw_error("Can't delete 'No Profile'")
            return
        del self.config[name]
        try:
            os.remove(self.prf_cfg['img_dir']+"config.xml")
        except OSError:
            pass
        try:
            os.remove(".config/"+name+".json")
            os.remove(".config/"+name+".xml")
        except OSError:
            pass
        self.load_profile("No Profile")

    def create_profile(self, name):
        # self.logger.info("Create new profile: {}".format(name))
        self.config["Profile"][name] = False
        self.save_config(".config/cfg.json", self.config)
        self.save_config(".config/"+name+".json", {"imgs": {},
                                                   "ethnics": {},
                                                   "img_dir": "",
                                                   "rtf": ""})
        open('.config/'+name+'.xml', 'a').close()

    def load_profile(self, name):
        deact_img_dir = self.prf_cfg['img_dir']
        self.prf_cfg = self.load_config(".config/"+name+".json")
        act_img_dir = self.prf_cfg['img_dir']
        self.swap_xml(self.cur_prf, name, deact_img_dir, act_img_dir)
        self.config[name] = True
        self.cur_prf = name

    def write_xml(self, data):
        with open(".config/config_template", "r", encoding="UTF-8") as fp:
            config_template = fp.read()
            xml_string = []

        for dat in data:
            xml_string.append("<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>".format(dat[1]+"/"+dat[2], dat[0]))

        xml_players = "\n".join(xml_string)
        xml_config = config_template.replace("[players]", xml_players)
        with open(self.prf_cfg['img_dir']+"config.xml", 'w') as fp:
            fp.write(xml_config)
        return xml_string

    def swap_xml(self, deact_name, act_name, deact_img_dir, act_img_dir):
        if os.path.isfile(deact_img_dir+"config.xml"):
            with open('.config/'+deact_name+'.xml', 'wb') as output, open(deact_img_dir+'config.xml', 'rb') as input:
                copyfileobj(input, output)

        if os.path.isfile(act_img_dir+"config.xml"):
            with open(act_img_dir+'config.xml', 'wb') as output, open('.config/'+act_name+'.xml', 'rb') as input:
                copyfileobj(input, output)

    def get_ethnic(self, nation):
        return self.config["Ethnics"].get(nation, None)
