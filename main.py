import re
import os
from tkinter import *
import tkinter as tk
import tkinter.filedialog as fdlg
import json
import tkinter.ttk as ttk
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
        if not os.path.isfile(self.cfg_path):
            print("No config!")
            self._write_config(self.cfg_path, {"No Profile" : True})
        self.config = self._load_config(self.cfg_path)
        self.create_widgets()

    def create_widgets(self):
        panel = Frame(self)
        panel.pack(side=TOP, fill=BOTH, expand=Y)
        #TODO: TOP Profiles
        frame_prf = tk.Frame(panel)
        #TODO: Create Profile LineEdit + Create Buttun
        frame_prf_sel = tk.Frame(panel)
        self.combo_prf = ttk.Combobox(frame_prf_sel, values=list(self.config.keys()), state='readonly')
        self.combo_prf.current(list(self.config.values()).index(True))
        self.combo_prf.bind("<<ComboboxSelected>>", self._set_profile_status)
        ent_prf = tk.Entry(frame_prf, width=20)
        btn_prf = tk.Button(frame_prf, text='Create', command=lambda e=ent_prf, c=self.combo_prf: self._create_profile(e, c))
        ent_prf.pack(side=LEFT, expand=Y, fill=X)
        btn_prf.pack(side=LEFT, padx=5)
        frame_prf.pack(fill=X, padx='1c', pady=3)
        #TODO Select Profile: Combobox
        #TODO: select profile with True as default
        self.combo_prf.pack(side=LEFT)
        #TODO Deactivate Profile
        btn_prf_act = tk.Button(frame_prf_sel, text='Delete', command=lambda e=ent_prf : self._delete_profile(e))
        btn_prf_act.pack(side=LEFT, padx=5)
        frame_prf_sel.pack(fill=X, padx='1c', pady=3)
        #TODO: MID PATHS
        frame_rtf = tk.Frame(panel)
        lbl_rtf = tk.Label(frame_rtf, width=20, text='RTF File')
        ent_rtf = tk.Entry(frame_rtf, width=40)
        btn_rtf = tk.Button(frame_rtf, text='Browse...', command=lambda t='file', e=ent_rtf: self._file_dialog(t, e))
        lbl_rtf.pack(side=LEFT)
        ent_rtf.pack(side=LEFT, expand=Y, fill=X)
        btn_rtf.pack(side=LEFT, padx=5)
        frame_rtf.pack(fill=X, padx='1c', pady=3)

        frame_img = tk.Frame(panel)
        lbl_img = tk.Label(frame_img, width=20, text='Newgen Image Folder')
        ent_img = tk.Entry(frame_img, width=40)
        btn_img = tk.Button(frame_img, text='Browse...', command=lambda t='dir', e=ent_img: self._file_dialog(t, e))
        lbl_img.pack(side=LEFT)
        ent_img.pack(side=LEFT, expand=Y, fill=X)
        btn_img.pack(side=LEFT, padx=5)
        frame_img.pack(fill=X, padx='1c', pady=3)

        #TODO: BOTTOM: Generation
        
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
    def _load_config(self, path):
        with open(path, 'r') as fp:
            data = json.load(fp)
            return data

    def _write_config(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp)

    def _set_profile_status(self, event):
        name = self.combo_prf.get()
        for prf, status in self.config.items():
            print(status)
            if status:
                self.config[prf] = False
        self.config[name] = True
        self._write_config(self.cfg_path, self.config)

    def _refresh_combo(self, combo):
        combo['values'] =list(self.config.keys())
        combo.current(list(self.config.values()).index(True))


    def _create_profile(self, ent, c):
        self.config[ent.get()] = False
        self._write_config(self.cfg_path, self.config)
        ent.delete(0, 'end')
        self._refresh_combo(c)

    def _delete_profile(self, ent, c):
        #TODO: delete profile and remove entry from combobox
        pass
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




#def main():
#    parse_rtf("newgens-Willem.rtf")



#if __name__ == "__main__":
#    main()
