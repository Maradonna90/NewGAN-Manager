"""
NewGAN Replacement Management Tool
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import random
from shutil import copyfileobj
import json
import re
import os

class SourceSelection(toga.Selection):
    def __init__(self, id=None, style=None, items=None, on_select=None, enabled=True, factory=None):
        super().__init__(id=id, style=style, items=items, on_select=on_select, enabled=enabled, factory=factory)

    def add_item(self, item):
        self._items.append(item)
        self._impl.add_item(item)

    def remove_item(self, item):
        self._items.remove(item)
        items = self._items

        if self._items is []:
            pass
        else:
            self._impl.remove_all_items()
            for itm in items:
                self._impl.add_item(itm)

class NewGANManager(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.mode_info = {"Overwrite" : "Overwrites already replaced faces",
                          "Preserve" :  "Preserves already replaced faces",
                          "Generate" : "Removes already replaced faces."}
        os.makedirs(".config", exist_ok=True)
        self.cfg_path = ".config/cfg.json"
        self.config = self._load_config(self.cfg_path)
        for k, v in self.config["Profile"].items():
            if v:
                self.cur_prf = k
                break

        self.prf_cfg = self._load_config(".config/"+self.cur_prf+".json")
        self.main_box = toga.Box()

        # TOP Profiles


        prf_box = toga.Box()
        prf_inp = toga.TextInput()

        self.prfsel_box = toga.Box()
        self.prfsel_lst = SourceSelection(items=list(self.config["Profile"].keys()), on_select=self._set_profile_status)
        self.prfsel_lst.value = self.cur_prf
        prfsel_btn = toga.Button(label="Delete", on_press=lambda e=None, c=self.prfsel_lst : self._delete_profile(c))
        prf_btn = toga.Button(label="Create", on_press=lambda e=None, d=prf_inp, c=self.prfsel_lst: self._create_profile(d, c))

        self.main_box.add(prf_box)
        prf_box.add(prf_inp)
        prf_box.add(prf_btn)
        self.main_box.add(self.prfsel_box)
        self.prfsel_box.add(self.prfsel_lst)
        self.prfsel_box.add(prfsel_btn)

        # MID Path selections
        dir_box = toga.Box()
        dir_lab = toga.Label(text="Select Image Directory: ")
        self.dir_inp = toga.TextInput(readonly=True, initial=self.prf_cfg['img_dir'])
        self.dir_btn = toga.Button(label="...", on_press=self.action_select_folder_dialog, enabled=False)

        rtf_box = toga.Box()
        rtf_lab = toga.Label(text="RTF File: ")
        self.rtf_inp = toga.TextInput(readonly=True, initial=self.prf_cfg['rtf'])
        self.rtf_btn = toga.Button(label="...", on_press=self.action_open_file_dialog, enabled=False)

        self.main_box.add(dir_box)
        self.main_box.add(rtf_box)
        dir_box.add(dir_lab)
        dir_box.add(self.dir_inp)
        dir_box.add(self.dir_btn)
        rtf_box.add(rtf_lab)
        rtf_box.add(self.rtf_inp)
        rtf_box.add(self.rtf_btn)

        
        gen_mode_box = toga.Box()
        self.genmde_lab = toga.Label(text="Mode: ")
        self.genmdeinfo_lab = toga.Label(text=self.mode_info["Generate"])
        self.genmde_lst = SourceSelection(items=list(self.mode_info.keys()), on_select=self.update_label)
        self.genmde_lst.value = "Generate"
        gen_mode_box.add(self.genmde_lab)
        gen_mode_box.add(self.genmde_lst)
        gen_mode_box.add(self.genmdeinfo_lab)
        self.main_box.add(gen_mode_box)
        # BOTTOM Generation
        gen_box = toga.Box()
        self.gen_btn = toga.Button(label="Replace Faces", on_press=self._replace_faces, enabled=False)
        self.gen_prg = toga.ProgressBar(max=110)
        gen_box.add(self.gen_btn)
        gen_box.add(self.gen_prg)
        self.main_box.add(gen_box)
        # END configs
        gen_mode_box.style.update(direction=ROW, padding=20)
        prf_box.style.update(direction=ROW, padding=20)
        self.prfsel_box.style.update(direction=ROW, padding=20)
        dir_box.style.update(direction=ROW, padding=20)
        rtf_box.style.update(direction=ROW, padding=20)
        gen_box.style.update(direction=COLUMN, padding=20, alignment='left')
        self.main_box.style.update(direction=COLUMN, padding=10, alignment='left', width=120)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def update_label(self, widget):
        self.genmdeinfo_lab.text = self.mode_info[widget.value]

    def _load_config(self, path):
        with open(path, 'r') as fp:
            data = json.load(fp)
            return data

    def _write_config(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)

    def _set_profile_status(self, e):
        print("switch profile:", e.value)
        if e.value == None:
            print("catch none", self.cur_prf)
        elif e.value == self.cur_prf:
            print("catch same values")
        #if e.value == "No Profile":

        else:
            name = e.value
            self.config["Profile"][self.cur_prf] = False
            if os.path.isfile(self.prf_cfg['img_dir']+"config.xml"):
                with open('.config/'+self.cur_prf+'.xml', 'wb') as output, open(self.prf_cfg['img_dir']+'config.xml', 'rb') as input:
                    copyfileobj(input, output)

            self.config["Profile"][name] = True
            self.cur_prf = name
            self.prf_cfg = self._load_config(".config/"+self.cur_prf+".json")
            with open(self.prf_cfg['img_dir']+'config.xml', 'wb') as output, open('.config/'+name+'.xml', 'rb') as input:
                copyfileobj(input, output)
            self._refresh_inp()
            if self.cur_prf == "No Profile":
                self.gen_btn.enabled = False
                self.dir_btn.enabled = False
                self.rtf_btn.enabled = False
            else:
                self.gen_btn.enabled = True
                self.dir_btn.enabled = True
                self.rtf_btn.enabled = True
            self._write_config(self.cfg_path, self.config)
    
    def _refresh_inp(self, clear=False):
        if clear:
            self.dir_inp.clear()
            self.rtf_inp.clear()
        else:
            self.dir_inp.value = self.prf_cfg['img_dir']
            self.rtf_inp.value = self.prf_cfg['rtf']

    def _create_profile(self, ent, c):
        name = ent.value
        self.config["Profile"][name] = False
        self._write_config(self.cfg_path, self.config)
        self._write_config(".config/"+name+".json", {"imgs" : {},
                                                     "ethnics" : {},
                                                     "img_dir" : "",
                                                     "rtf" : ""})
        ent.clear()
        open('.config/'+name+'.xml', 'a').close
        #self.cur_prf = name
        c.add_item(name)

    def _delete_profile(self, c):
        prf = c.value
        if prf == "No Profile":
            print("Can't delet no profile")
            self._throw_error("Can't delete 'No Profile'")
            return
        del self.config["Profile"][prf]
        self.config["Profile"]["No Profile"] = True
        os.remove(self.prf_cfg['img_dir']+"config.xml")
        self.cur_prf = "No Profile"
        self._write_config(self.cfg_path, self.config)
        os.remove(".config/"+prf+".json")
        os.remove(".config/"+prf+".xml")
        c.remove_item(prf)
        self._refresh_inp(True)

    def parse_rtf(self, path):
        #TODO: fix parser for advanced view
        UID_regex = re.compile('([0-9]){10}')
        result_data = []
        rtf = open(path, 'r')
        rtf_data = []
        for line in rtf:
            if UID_regex.search(line):
                rtf_data.append(line.strip())
        for newgen in rtf_data:
            data_fields = newgen.split('|')
            sec_nat = data_fields[5].strip()
            if sec_nat == '':
                sec_nat = None
            result_data.append([data_fields[3].strip(), data_fields[4].strip(), sec_nat])
        return result_data

    def _throw_error(self, msg):
        self.main_window.error_dialog('Error', msg)
    
    def action_select_folder_dialog(self, widget):
        try:
            path_names = self.main_window.select_folder_dialog(
                title="Select image root folder"
            )
            self.dir_inp.value = path_names[0]+"/"
            self.prf_cfg['img_dir'] = path_names[0]+"/"
            self._write_config(".config/"+self.cur_prf+".json", self.prf_cfg)

        except:
            pass

    def action_open_file_dialog(self, widget):
        try:
            fname = self.main_window.open_file_dialog(
                title="Open RTF file",
                multiselect=False,
                file_types=['rtf']
            )
            if fname is not None:
                self.rtf_inp.value = fname
                self.prf_cfg['rtf'] = fname
                self._write_config(".config/"+self.cur_prf+".json", self.prf_cfg)
            else:
                self.prf_cfg['rtf'] = ""
                self.rtf_inp.value = ""
                self._write_config(".config/"+self.cur_prf+".json", self.prf_cfg)
        except ValueError:
            pass

    def _replace_faces(self, widget):
        print("rtf:", self.prf_cfg['rtf'])
        print("img_dir:", self.prf_cfg['img_dir'])
        print("profile:", self.cur_prf)
        print("mode:", self.genmde_lst.value)
        #get values from UI elements
        rtf = self.prf_cfg['rtf']
        img_dir = self.prf_cfg['img_dir']
        profile = self.cur_prf
        mode = self.genmde_lst.value
        #parse rtf
        if '' in [rtf, img_dir]:
            self._throw_error("Select RTF and/or image directory!")
            print("Select RTF and/or image directory!")
            return
        self.gen_prg.start()
        rtf_data = self.parse_rtf(rtf)
        self.gen_prg.max = len(rtf_data)+10
        with open(".config/config_template", "r") as fp:
            config_template = fp.read()
        #walk all img subdirs and get all filenames. Create map
        all_ethnicities = ["East European", "Scandinavian", "Mediterranean", "Arabian",
                         "African", "East Asian", "Central Asian", "Central European"]
        all_images = []
        print("Load profile config and create image set...")
        prf_cfg = self._load_config(".config/"+profile+".json")
        if mode == "Generate":
            prf_cfg['imgs'] = {}
            prf_cfg['ethnics'] = {}
        prf_map = prf_cfg["imgs"]
        prf_eth_map = prf_cfg['ethnics']
        prf_imgs = set(prf_cfg["imgs"].values())
        xml_string = []
        print("Restore already replaced faces if applicable...")
        for k, v in prf_map.items():
            xml_string.append("<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>".format(prf_eth_map[k]+"/"+v, k))

        #map rtf_data to ethnicities
        print("Map player to ethnicity...")
        for i, player in enumerate(rtf_data):
            #print("2nd:", player[2])
            if player[2]:
                #print("DO 2nd!")
                p_ethnic = self.config["Ethnics"][player[2]]
            else:
                p_ethnic = self.config["Ethnics"][player[1]]
            if player[0] in prf_map:
                if mode == "Preserve":
                    print("Preserve:", i, p_ethnic)
                    continue
                elif mode == "Overwrite":
                    print("Overwrite:", i, p_ethnic)
                    player_img = prf_map[player[0]]
                    prf_imgs.remove(player_img)
            eth_imgs = set([f.name for f in os.scandir(self.prf_cfg['img_dir']+p_ethnic) if f.is_file()])
            selection_pool = eth_imgs - prf_imgs
            #print("eth_imgs:", eth_imgs)
            #print("prf_imgs:", prf_imgs)
            #print("sel pool:", selection_pool)
            player_img = random.choice(tuple(selection_pool))
            prf_map[player[0]] = player_img
            prf_eth_map[player[0]] = p_ethnic
            prf_imgs.add(player_img)
            player_img = player_img.split('.')[0]

        #create config file entry
            xml_string.append("<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>".format(p_ethnic+"/"+player_img, player[0]))
            self.gen_prg.value += 1
            print(i, p_ethnic)

        #save profile metadata (used pics and config.xml)
        print("Generate config.xml...")
        xml_players = "\n".join(xml_string)
        xml_config = config_template.replace("[players]", xml_players)
        with open(self.prf_cfg['img_dir']+"config.xml", 'w') as fp:
            fp.write(xml_config)
        print("Save metadata for profile...")
        prf_cfg["imgs"] = prf_map
        self._write_config(".config/"+profile+".json", prf_cfg)
        self.gen_prg.value += 10
        print("Finished! :)")

def main():
    return NewGANManager()
