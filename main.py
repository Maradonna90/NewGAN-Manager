import re
import os
from tkinter import *
import tkinter as tk
import tkinter.filedialog as fdlg
import json
import tkinter.ttk as ttk
import random
#TODO: map Nat and 2nd Nat to random image
#TODO: store UID mapping to image in JSON in .config => avoid double assigning
#TODO: create profiles to have assignments per savegame and switch active profiles
#TODO: NAT -> ethnicity mapping config file

class NEWGAN_Manager(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        os.makedirs(".config", exist_ok=True)
        self.cfg_path = ".config/cfg.json"
        self.config = self._load_config(self.cfg_path)
        self.create_widgets()

    def create_widgets(self):
        panel = Frame(self)
        panel.pack(side=TOP, fill=BOTH, expand=Y)
        #TODO: TOP Profiles
        frame_prf = tk.Frame(panel)
        frame_prf_sel = tk.Frame(panel)
        self.combo_prf = ttk.Combobox(frame_prf_sel, values=list(self.config["Profile"].keys()), state='readonly')
        self.combo_prf.current(list(self.config["Profile"].values()).index(True))
        self.combo_prf.bind("<<ComboboxSelected>>", self._set_profile_status)
        ent_prf = tk.Entry(frame_prf, width=20)
        btn_prf = tk.Button(frame_prf, text='Create', command=lambda e=ent_prf, c=self.combo_prf: self._create_profile(e, c))
        ent_prf.pack(side=LEFT, expand=Y, fill=X)
        btn_prf.pack(side=LEFT, padx=5)
        frame_prf.pack(fill=X, padx='1c', pady=3)
        self.combo_prf.pack(side=LEFT)
        #TODO Delete Profile
        btn_prf_act = tk.Button(frame_prf_sel, text='Delete', command=lambda e=ent_prf, c=self.combo_prf : self._delete_profile(e, c))
        btn_prf_act.pack(side=LEFT, padx=5)
        frame_prf_sel.pack(fill=X, padx='1c', pady=3)
        #TODO: MID PATHS
        frame_rtf = tk.Frame(panel)
        lbl_rtf = tk.Label(frame_rtf, width=20, text='RTF File')
        ent_rtf = tk.Entry(frame_rtf, width=40)
        btn_rtf = tk.Button(frame_rtf, text='...', command=lambda t='file', e=ent_rtf: self._file_dialog(t, e))
        lbl_rtf.pack(side=LEFT)
        ent_rtf.pack(side=LEFT, expand=Y, fill=X)
        btn_rtf.pack(side=LEFT, padx=5)
        frame_rtf.pack(fill=X, padx='1c', pady=3)

        frame_img = tk.Frame(panel)
        lbl_img = tk.Label(frame_img, width=20, text='Newgen Image Folder')
        ent_img = tk.Entry(frame_img, width=40)
        btn_img = tk.Button(frame_img, text='...', command=lambda t='dir', e=ent_img: self._file_dialog(t, e))
        lbl_img.pack(side=LEFT)
        ent_img.pack(side=LEFT, expand=Y, fill=X)
        btn_img.pack(side=LEFT, padx=5)
        frame_img.pack(fill=X, padx='1c', pady=3)

        #TODO: BOTTOM: Generation
        frame_gen = tk.Frame(panel)
        #TODO Generate Button
        btn_gen = tk.Button(frame_gen, text='Replace Faces', command=lambda r=ent_rtf.get(), i=ent_img.get(), p=self.combo.get(): 
                            self._replace_faces(r, i, p))
        btn_gen.pack(side=BOTTOM)
        #TODO Progressbar
        frame_img.pack(fill=X, padx='1c', pady=3)

    def _file_dialog(self, type, ent):
        # triggered when the user clicks a 'Browse' button
        fn = None

        if type == 'file':
            opts = {'initialfile': ent.get(),
                'filetypes': (("RTF files", ".rtf"),
                            ("All files", "*.*"))}
            opts['title'] = 'Select a file to open...'
            fn = fdlg.askopenfilename(**opts)
        elif type == 'dir':
            ops = {'title' : 'Select folder...'}
            fn = fdlg.askdirectory()
        #else:
            # this should only return a filename; however,
            # under windows, selecting a file and hitting
            # 'Save' gives a warning about replacing an
            # existing file; although selecting 'Yes' does
            # not actually cause a 'Save'; the filename
            # is simply returned
         #   opts['title'] = 'Select a file to save...'
         #   fn = fdlg.asksaveasfilename(**opts)

        if fn:
            print(fn)
            ent.delete(0, END)
            ent.insert(END, fn)
    def _replace_faces(self, rtf, img_dir, profile):
        #TODO parse rtf
        rtf_data = self.parse_rtf(rtf)
        with open(".config/config_template", "r") as fp:
            config_template = fp.read()
        #TODO: walk all img subdirs and get all filenames. Create map
        all_ethnicies = ["East European", "Scandinavian", "Mediterranean", "Arabian",
                         "African", "South East Asian", "East Asian", "Central Asian", "UK",
                         "Carribean"]
        all_images = []
        for eth in all_ethnicities.keys():
            [all_images.append(f.name) for f in os.scandir(eth+"/") if f.is_file()]
        prf_cfg = self._load_config(".config/"+profile+".json")
        prf_imgs = set(prf_cfg["imgs"])
        #TODO map rtf_data to ethnicities
        xml_string = []
        for player in rtf_data:
            if player[2]:
                p_ethnic = self.config["Ethnics"][player[2]]
            else:
                p_ethnic = self.config["Ethnics"][player[1]]
            #TODO: choose picture
            eth_imgs = set([all_images.append(f.name) for f in os.scandir(p_ethnic+"/") if f.is_file()])
            selection_pool = eth_imgs - prf_imgs
            player_img = random.choice(tuple(selection_pool))
            prf_imgs.add(player_img)

        #TODO create config file entry
            xml_string.append("<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>".format(player_img, player[0]))
        #save profile metadata (used pics and config.xml)
        xml_players = "\n".join(xml_string)
        xml_config = config_template.replace("[players]", xml_players)
        with open("config.xml", 'w') as fp:
            fp.write(xml_config)
        prf_cfg["imgs"] = list(prf_imgs)
        self._write_config(".config/"+profile+".json", prf_cfg)

    def _load_config(self, path):
        with open(path, 'r') as fp:
            data = json.load(fp)
            return data

    def _write_config(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)

    def _set_profile_status(self, event):
        #TODO: when profile switch, switch xml files
        name = self.combo_prf.get()
        for prf, status in self.config["Profile"].items():
            print(status)
            if status:
                self.config["Profile"][prf] = False
        self.config["Profile"][name] = True
        self._write_config(self.cfg_path, self.config)

    def _refresh_combo(self, combo):
        combo['values'] =list(self.config["Profile"].keys())
        combo.current(list(self.config["Profile"].values()).index(True))


    def _create_profile(self, ent, c):
        name = ent.get()
        self.config["Profile"][name] = False
        self._write_config(self.cfg_path, self.config)
        self._write_config(".config/"+name+".json", {"imgs" : []})
        ent.delete(0, 'end')
        self._refresh_combo(c)

    def _delete_profile(self, ent, c):
        #TODO: delete profile and remove entry from combobox
        prf = self.combo_prf.get()
        if prf == "No Profile":
            print("Can't delte no profile")
            return
        del self.config["Profile"][prf]
        self.config["Profile"]["No Profile"] = True
        self._write_config(self.cfg_path, self.config)
        os.remove(".config/"+prf+".json")
        os.remove(".config/"+prf+".xml")
        self._refresh_combo(self.combo_prf)

    def parse_rtf(self, path):
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

root = tk.Tk()
app = NEWGAN_Manager(master=root)
app.mainloop()
