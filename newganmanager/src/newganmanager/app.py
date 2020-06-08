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


        main_box = toga.Box()
        
        #TODO: TOP Profiles
        

        prf_box = toga.Box()
        prf_inp = toga.TextInput()
        prf_btn = toga.Button(label="Create")
        main_box.add(prf_box)
        prf_box.add(prf_inp)
        prf_box.add(prf_btn)

        prfsel_box = toga.Box()
        prfsel_lst = toga.Selection()
        prfsel_btn = toga.Button(label="Delete")
        main_box.add(prfsel_box)
        prfsel_box.add(prfsel_lst)
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
def main():
    return NewGANManager()
