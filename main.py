import re
import os
from tkinter import *
import tkinter as tk
import tkinter.filedialog as fdlg
from tkinter import messagebox
import json
import tkinter.ttk as ttk
import random
from shutil import copyfileobj
#TODO: store UID mapping to image in JSON in .config => avoid double assigning
#TODO: create profiles to have assignments per savegame and switch active profiles
#TODO: NAT -> ethnicity mapping config file

class NEWGAN_Manager(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("NEWGAN Manager")
        self.pack()
        os.makedirs(".config", exist_ok=True)
        self.cfg_path = ".config/cfg.json"
        self.config = self._load_config(self.cfg_path)
        self.create_widgets()

    def create_widgets(self):
        panel = Frame(self)
        panel.pack(side=TOP, fill=BOTH, expand=Y)
        #TODO: TOP Profiles
        labelframe_prf = tk.LabelFrame(panel, text="Profiles")
        frame_prf = tk.Frame(labelframe_prf)
        frame_prf_sel = tk.Frame(labelframe_prf)
        self.combo_prf = ttk.Combobox(frame_prf_sel, values=list(self.config["Profile"].keys()), state='readonly')
        self.combo_prf.current(list(self.config["Profile"].values()).index(True))
        self.combo_prf.bind("<<ComboboxSelected>>", self._set_profile_status)
        ent_prf = tk.Entry(frame_prf, width=20)
        btn_prf = tk.Button(frame_prf, text='Create', command=lambda e=ent_prf, c=self.combo_prf: self._create_profile(e, c))
        ent_prf.pack(side=LEFT, expand=Y, fill=X)
        btn_prf.pack(side=LEFT, padx=5)
        frame_prf.pack(fill=X, padx='1c', pady=3)
        self.combo_prf.pack(side=LEFT)
        #Delete Profile
        btn_prf_act = tk.Button(frame_prf_sel, text='Delete', command=lambda e=ent_prf, c=self.combo_prf : self._delete_profile(e, c))
        btn_prf_act.pack(side=LEFT, padx=5)
        frame_prf_sel.pack(fill=X, padx='1c', pady=3)
        labelframe_prf.pack(fill=X, padx='1c', pady=3)
        #MID PATHS
        labelframe_pth = tk.LabelFrame(panel, text="Paths")
        frame_rtf = tk.Frame(labelframe_pth)
        lbl_rtf = tk.Label(frame_rtf, width=20, text='RTF File')
        ent_rtf = tk.Entry(frame_rtf, width=40)
        btn_rtf = tk.Button(frame_rtf, text='...', command=lambda t='file', e=ent_rtf: self._file_dialog(t, e))
        lbl_rtf.pack(side=LEFT)
        ent_rtf.pack(side=LEFT, expand=Y, fill=X)
        btn_rtf.pack(side=LEFT, padx=5)
        frame_rtf.pack(fill=X, padx='1c', pady=3)

        frame_img = tk.Frame(labelframe_pth)
        lbl_img = tk.Label(frame_img, width=20, text='Newgen Image Folder')
        ent_img = tk.Entry(frame_img, width=40)
        btn_img = tk.Button(frame_img, text='...', command=lambda t='dir', e=ent_img: self._file_dialog(t, e))
        lbl_img.pack(side=LEFT)
        ent_img.pack(side=LEFT, expand=Y, fill=X)
        btn_img.pack(side=LEFT, padx=5)
        frame_img.pack(fill=X, padx='1c', pady=3)
        labelframe_pth.pack(fill=X, padx='1c', pady=3)


        #TODO: BOTTOM: Generation
        labelframe_gen = tk.LabelFrame(panel, text="Generation")
        frame_gen = tk.Frame(labelframe_gen)
        #TODO Generate Button
        progress = ttk.Progressbar(frame_gen, orient = HORIZONTAL, length = 110)
        progress.pack(side=BOTTOM)
        btn_gen = tk.Button(frame_gen, text='Replace Faces', command=lambda r=ent_rtf, i=ent_img, p=self.combo_prf,
                            prog=progress :
                            self._replace_faces(r, i, p, prog))
        btn_gen.pack(side=TOP)
        #TODO Progressbar
        frame_gen.pack(fill=X, padx='1c', pady=3)
        labelframe_gen.pack(fill=X, padx='1c', pady=3)


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
    def _replace_faces(self, rtf, img_dir, profile, prog):
        print("rtf:", rtf.get())
        print("img_dir:", img_dir.get())
        print("profile:", profile.get())
        #get values from UI elements
        rtf = rtf.get()
        img_dir = img_dir.get()
        profile = profile.get()

        #parse rtf
        if profile == "No Profile":
            self._throw_error("Please select a profile!")
            print("Please select a profile!")
            return
        if '' in [rtf, img_dir]:
            self._throw_error("Select RTF and/or image directory!")
            print("Select RTF and/or image directory!")
            return
        rtf_data = self.parse_rtf(rtf)
        with open(".config/config_template", "r") as fp:
            config_template = fp.read()
        #walk all img subdirs and get all filenames. Create map
        all_ethnicities = ["East European", "Scandinavian", "Mediterranean", "Arabian",
                         "African", "South East Asian", "East Asian", "Central Asian", "UK",
                         "Carribean", "South American"]
        all_images = []
        print("Load profile config and create image set...")
        prf_cfg = self._load_config(".config/"+profile+".json")
        prf_map = prf_cfg["imgs"]
        prf_imgs = set(prf_cfg["imgs"].values())
        #map rtf_data to ethnicities
        print("Map player to ethnicity...")
        xml_string = []
        for i, player in enumerate(rtf_data):
            #print("2nd:", player[2])
            if player[2]:
                #print("DO 2nd!")
                p_ethnic = self.config["Ethnics"][player[2]]
            else:
                p_ethnic = self.config["Ethnics"][player[1]]
            print(i, p_ethnic)
            if player[0] in prf_map:
                playre_img = prf_map[player[0]].split('.')[0]
                xml_string.append("<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>".format(p_ethnic+"/"+player_img, player[0]))
                prog["value"] += 1
                continue
            eth_imgs = set([f.name for f in os.scandir(p_ethnic) if f.is_file()])
            selection_pool = eth_imgs - prf_imgs
            #print("eth_imgs:", eth_imgs)
            #print("prf_imgs:", prf_imgs)
            #print("sel pool:", selection_pool)
            player_img = random.choice(tuple(selection_pool))
            prf_imgs.add(player_img)
            player_img = player_img.split('.')[0]

        #create config file entry
            xml_string.append("<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>".format(p_ethnic+"/"+player_img, player[0]))
            prog["value"] += 1
        #save profile metadata (used pics and config.xml)
        print("Generate config.xml...")
        xml_players = "\n".join(xml_string)
        xml_config = config_template.replace("[players]", xml_players)
        with open("config.xml", 'w') as fp:
            fp.write(xml_config)
        print("Save metadata for profile...")
        prf_cfg["imgs"] = list(prf_imgs)
        self._write_config(".config/"+profile+".json", prf_cfg)
        prog["value"] = 110
        print("Finished! :)")

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
        combo['values'] =list(self.config["Profile"].keys())
        combo.current(list(self.config["Profile"].values()).index(True))


    def _create_profile(self, ent, c):
        name = ent.get()
        self.config["Profile"][name] = False
        self._write_config(self.cfg_path, self.config)
        self._write_config(".config/"+name+".json", {"imgs" : {}})
        ent.delete(0, 'end')
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

root = tk.Tk()
app = NEWGAN_Manager(master=root)
app.mainloop()
