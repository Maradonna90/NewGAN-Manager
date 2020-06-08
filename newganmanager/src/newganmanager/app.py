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


class NewGANManager(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        os.makedirs(".config", exist_ok=True)
        self.cfg_path = ".config/cfg.json"
        self.config = self._load_config(self.cfg_path)

        main_box = toga.Box()
        
        #TODO: TOP Profiles
        

        prf_box = toga.Box()
        prf_inp = toga.TextInput()

        prfsel_box = toga.Box()
        self.prfsel_lst = toga.Selection(items=list(self.config["Profile"].keys()))
        self.prfsel_lst.value = "No Profile"
        prfsel_btn = toga.Button(label="Delete")
        prf_btn = toga.Button(label="Create", on_press=lambda e=None, d=prf_inp, c=self.prfsel_lst: self._create_profile(d, c))

        main_box.add(prf_box)
        prf_box.add(prf_inp)
        prf_box.add(prf_btn)
        main_box.add(prfsel_box)
        prfsel_box.add(self.prfsel_lst)
        prfsel_box.add(prfsel_btn)

        #TODO MID Path selections
        #pth_box = toga.Box()
        dir_box = toga.Box()
        dir_lab = toga.Label(text="Select Image Directory:")
        dir_inp = toga.TextInput()
        dir_btn = toga.Button(label="...")

        rtf_box = toga.Box()
        rtf_lab = toga.Label(text="RTF File:")
        rtf_inp = toga.TextInput()
        rtf_btn = toga.Button(label="...")

        #main_box.add(pth_box)
        main_box.add(dir_box)
        main_box.add(rtf_box)
        dir_box.add(dir_lab)
        dir_box.add(dir_inp)
        dir_box.add(dir_btn)
        rtf_box.add(rtf_lab)
        rtf_box.add(rtf_inp)
        rtf_box.add(rtf_btn)


        #TODO BOTTOM Generation
        gen_box = toga.Box()
        gen_btn = toga.Button(label="Replace Faces")
        gen_prg = toga.ProgressBar(max=110)
        gen_prg.style.update()

        gen_box.add(gen_btn)
        gen_box.add(gen_prg)
        main_box.add(gen_box)
        #TODO END configs
        #pth_box.style.update(direction=COLUMN, padding_top=10)
        prf_box.style.update(direction=ROW, padding=20)
        prfsel_box.style.update(direction=ROW, padding=20)
        dir_box.style.update(direction=ROW, padding=20)
        rtf_box.style.update(direction=ROW, padding=20)
        gen_box.style.update(direction=COLUMN, padding=20, alignment='left')
        main_box.style.update(direction=COLUMN, padding=10, alignment='left', width=120)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def _load_config(self, path):
        with open(path, 'r') as fp:
            data = json.load(fp)
            return data

    def _write_config(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)

    def _set_profile_status(self, event):
        name = self.combo_prf.get()
        for prf, status in self.config["Profile"].items():
            if status:
                self.config["Profile"][prf] = False
                with open('.config/'+prf+'.xml', 'wb') as output, open('config.xml', 'rb') as input:
                    copyfileobj(input, output)

        self.config["Profile"][name] = True
        with open('config.xml', 'wb') as output, open('.config/'+name+'.xml', 'rb') as input:
            copyfileobj(input, output)
        print(self.config["Profile"])
        self._write_config(self.cfg_path, self.config)

    def _refresh_combo(self, combo):
        combo['items'] = list(self.config["Profile"].keys())
        combo.value = list(self.config["Profile"].values()).index(True)


    def _create_profile(self, ent, c):
        print(ent, c)
        name = ent.value
        self.config["Profile"][name] = False
        self._write_config(self.cfg_path, self.config)
        self._write_config(".config/"+name+".json", {"imgs" : {}})
        ent.clear()
        self._refresh_combo(c)

    def _delete_profile(self, ent, c):
        prf = self.combo_prf.get()
        if prf == "No Profile":
            print("Can't delet no profile")
            self._throw_error("Can't delete 'No Profile'")
            return
        del self.config["Profile"][prf]
        self.config["Profile"]["No Profile"] = True
        self._write_config(self.cfg_path, self.config)
        os.remove(".config/"+prf+".json")
        try:
            os.remove(".config/"+prf+".xml")
        except:
            pass
        self._refresh_combo(self.combo_prf)

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
        messagebox.showerror("Error", msg)

def main():
    return NewGANManager()
