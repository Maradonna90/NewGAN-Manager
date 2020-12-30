import config_manager
import os
from shutil import copyfileobj
import shutil


class Profile_Manager(config_manager.Config_Manager):
    def __init__(self, name, root_dir):
        self.config = self.load_config(root_dir+"/.user/cfg.json")
        self.prf_cfg = self.load_config(root_dir+"/.user/"+name+".json")
        self.eth_cfg = self.load_config(root_dir+"/.config/cfg.json")
        self.cur_prf = name
        self.root_dir = root_dir

    def migrate_config(self):
        if os.path.isfile("../.config/cfg.json"):
            old_cfg = self.load_config("../.config/cfg.json")
            if "Profile" in old_cfg:
                profiles = {}
                profiles["Profile"] = old_cfg["Profile"]
                self.save_config(self.root_dir+"/.user/cfg.json", profiles)
                del old_cfg["Profile"]
                self.save_config(self.root_dir+"/.config/cfg.json", old_cfg)
                for profile in profiles["Profile"].keys():
                    with open(self.root_dir+"/.user/"+profile+'.xml', 'wb') as output, open('../.config/'+profile+'.xml', 'rb') as input:
                        copyfileobj(input, output)
                        os.remove('../.config/'+profile+'.xml')
                    with open(self.root_dir+"/.user/"+profile+'.json', 'wb') as output, open('../.config/'+profile+'.json', 'rb') as input:
                        copyfileobj(input, output)
                        os.remove('../.config/'+profile+'.json')
                shutil.rmtree("../.config/")

    def delete_profile(self, name):
        # self.logger.info("Delete profile: {}".format(name))
        if name == "No Profile":
            # self.logger.info("Can't delet no profile")
            self._throw_error("Can't delete 'No Profile'")
            return
        del self.config["Profile"][name]
        try:
            os.remove(self.prf_cfg['img_dir']+"config.xml")
        except OSError:
            pass
        try:
            os.remove(self.root_dir+"/.user/"+name+".json")
            os.remove(self.root_dir+"/.user/"+name+".xml")
        except OSError:
            pass
        self.save_config(self.root_dir+"/.user/cfg.json", self.config)
        self.load_profile("No Profile")

    def create_profile(self, name):
        # self.logger.info("Create new profile: {}".format(name))
        self.config["Profile"][name] = False
        self.save_config(self.root_dir+"/.user/cfg.json", self.config)
        self.save_config(self.root_dir+"/.user/"+name+".json", {"imgs": {},
                                                   "ethnics": {},
                                                   "img_dir": "",
                                                   "rtf": ""})
        open(self.root_dir+'/.user/'+name+'.xml', 'a').close()

    def load_profile(self, name):
        deact_img_dir = self.prf_cfg['img_dir']
        self.prf_cfg = self.load_config(self.root_dir+"/.user/"+name+".json")
        act_img_dir = self.prf_cfg['img_dir']
        self.swap_xml(self.cur_prf, name, deact_img_dir, act_img_dir)
        for key in self.config["Profile"].keys():
            if key == name:
                self.config["Profile"][key] = True
            else:
                self.config["Profile"][key] = False
        self.cur_prf = name

    def write_xml(self, data):
        with open(self.root_dir+"/.config/config_template", "r", encoding="UTF-8") as fp:
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
            with open(self.root_dir+'/.user/'+deact_name+'.xml', 'wb') as output, open(deact_img_dir+'config.xml', 'rb') as input:
                copyfileobj(input, output)

        if os.path.isfile(act_img_dir+"config.xml"):
            with open(act_img_dir+'config.xml', 'wb') as output, open(self.root_dir+'/.user/'+act_name+'.xml', 'rb') as input:
                copyfileobj(input, output)

    def get_ethnic(self, nation):
        return self.eth_cfg["Ethnics"].get(nation, None)
