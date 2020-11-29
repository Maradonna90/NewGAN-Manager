"""
NewGAN Replacement Management Tool
"""
import toga
from toga.style.pack import COLUMN, ROW
import os
import logging
from dhooks import Webhook, Embed, File
from config_manager import Config_Manager
from profile_manager import Profile_Manager
from mapper import Mapper
from rtfparser import RTF_Parser
from progressbar import Progressbar

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

    def __init__(self, log):
        super().__init__()
        self.logger = log

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.logger.info("Starting Application\n------------------------------------------------")

        self.mode_info = {"Overwrite": "Overwrites already replaced faces",
                          "Preserve":  "Preserves already replaced faces",
                          "Generate": "Generates mapping from scratch."}
        os.makedirs(".config", exist_ok=True)

        self.logger.info("Loading current profile")
        self.profile_manager = Profile_Manager(".config/cfg.json", Config_Manager().get_latest_prf(".config/cfg.json"))
        self.logger.info("Creating GUI")
        self.main_box = toga.Box()
        self.logger.info("Created main box")

        label_width = 125
        # TOP Profiles
        prf_box = toga.Box()
        self.logger.info("Created prf_box")

        prf_inp = toga.TextInput()
        self.logger.info("Created prf_inp")

        self.prfsel_box = toga.Box()
        prf_lab = toga.Label(text="Create Profile: ")
        prf_lab.style.update(width=label_width)

        prfsel_lab = toga.Label(text="Select Profile: ")
        prfsel_lab.style.update(width=label_width)
        self.prfsel_lst = SourceSelection(items=list(self.profile_manager.config["Profile"].keys()), on_select=self._set_profile_status)
        self.prfsel_lst.value = self.profile_manager.cur_prf
        prfsel_btn = toga.Button(label="Delete", on_press=lambda e=None, c=self.prfsel_lst : self._delete_profile(c))
        prf_btn = toga.Button(label="Create", on_press=lambda e=None, d=prf_inp, c=self.prfsel_lst: self._create_profile(d, c))

        self.main_box.add(prf_box)
        prf_box.add(prf_lab)
        prf_box.add(prf_inp)
        prf_box.add(prf_btn)
        prf_lab.style.update(padding_top=7) 
        prf_inp.style.update(direction=ROW, padding=(0, 20), flex=1)

        self.main_box.add(self.prfsel_box)
        self.prfsel_box.add(prfsel_lab)
        self.prfsel_box.add(self.prfsel_lst)
        self.prfsel_box.add(prfsel_btn)
        self.prfsel_lst.style.update(direction=ROW, padding=(0, 20), flex=1)
        prfsel_lab.style.update(padding_top=7)

        # MID Path selections
        dir_box = toga.Box()
        dir_lab = toga.Label(text="Select Image Directory: ")
        dir_lab.style.update(width=label_width)
        self.dir_inp = toga.TextInput(readonly=True, initial=self.profile_manager.prf_cfg['img_dir'])
        self.dir_inp.style.update(direction=ROW, padding=(0, 20), flex=1)
        self.dir_btn = toga.Button(label="...", on_press=self.action_select_folder_dialog, enabled=False)

        rtf_box = toga.Box()
        rtf_lab = toga.Label(text="RTF File: ")
        rtf_lab.style.update(width=label_width)
        self.rtf_inp = toga.TextInput(readonly=True, initial=self.profile_manager.prf_cfg['rtf'])
        self.rtf_inp.style.update(direction=ROW, padding=(0, 20), flex=1)
        self.rtf_btn = toga.Button(label="...", on_press=self.action_open_file_dialog, enabled=False)

        self.main_box.add(dir_box)
        self.main_box.add(rtf_box)
        dir_box.add(dir_lab)
        dir_box.add(self.dir_inp)
        dir_box.add(self.dir_btn)
        rtf_box.add(rtf_lab)
        rtf_box.add(self.rtf_inp)
        rtf_box.add(self.rtf_btn)
        dir_lab.style.update(padding_top=7)
        rtf_lab.style.update(padding_top=7)

        gen_mode_box = toga.Box()
        self.genmde_lab = toga.Label(text="Mode: ")
        self.genmde_lab.style.update(width=label_width)
        self.genmdeinfo_lab = toga.Label(text=self.mode_info["Generate"])
        self.genmde_lst = SourceSelection(items=list(self.mode_info.keys()), on_select=self.update_label)
        self.genmde_lst.value = "Generate"
        self.genmde_lst.style.update(direction=ROW, padding=(0, 20), flex=1)
        self.genmde_lab.style.update(padding_top=7)
        self.genmdeinfo_lab.style.update(padding_top=7)

        gen_mode_box.add(self.genmde_lab)
        gen_mode_box.add(self.genmde_lst)
        gen_mode_box.add(self.genmdeinfo_lab)
        self.main_box.add(gen_mode_box)
        # BOTTOM Generation
        gen_box = toga.Box()
        self.gen_btn = toga.Button(label="Replace Faces", on_press=self._replace_faces, enabled=False)
        self.gen_btn.style.update(padding_bottom=20)
        self.gen_lab = toga.Label(text="")

        # self.gen_prg = toga.ProgressBar(max=110)
        self.gen_prg = Progressbar(label=self.gen_lab)
        gen_box.add(self.gen_btn)
        gen_box.add(self.gen_lab)
        gen_box.add(self.gen_prg)
        self.main_box.add(gen_box)
        self.gen_lab.style.update(padding_top=20)

        # Report bad image
        rep_box = toga.Box()
        self.rep_lab = toga.Label(text="Player UID: ")
        self.rep_lab.style.update(width=label_width)
        self.rep_inp = toga.TextInput(on_change=self.change_image)
        self.rep_img = toga.ImageView(toga.Image("resources/logo.png"))
        self.rep_img.style.update(height=180)
        self.rep_img.style.update(width=180)
        self.rep_btn = toga.Button(label="Report", on_press=self.send_report, enabled=False)

        rep_box.add(self.rep_lab)
        rep_box.add(self.rep_inp)
        rep_box.add(self.rep_img)
        rep_box.add(self.rep_btn)
        self.main_box.add(rep_box)
        self.rep_lab.style.update(padding_top=10)
        self.rep_inp.style.update(direction=ROW, padding=(0, 20), flex=1)


        # END config
        self.prfsel_box.style.update(padding_bottom=20)
        dir_box.style.update(padding_bottom=20)
        prf_box.style.update(padding_bottom=20)
        rtf_box.style.update(padding_bottom=20)
        gen_mode_box.style.update(padding_bottom=20)
        rep_box.style.update(padding_top=20)
        gen_box.style.update(direction=COLUMN, alignment='center')
        self.main_box.style.update(direction=COLUMN, padding=30, alignment='center')

        self.main_window = toga.MainWindow(title=self.formal_name, size=(1000, 600))
        self.main_window.content = self.main_box
        self.main_window.show()

    def update_label(self, widget):
        self.logger.info("Updating generation label")
        self.genmdeinfo_lab.text = self.mode_info[widget.value]

    def set_btns(self, value):
        if self.profile_manager.cur_prf == "No Profile":
            self.gen_btn.enabled = False
            self.dir_btn.enabled = False
            self.rtf_btn.enabled = False
            self.rep_btn.enabled = False
        else:
            self.gen_btn.enabled = value
            self.dir_btn.enabled = value
            self.rtf_btn.enabled = value
            self.rep_btn.enabled = value

    def _set_profile_status(self, e):
        self.logger.info("switch profile: {}".format(e.value))
        if e.value is None:
            self.logger.info("catch none {}".format(self.profile_manager.cur_prf))
        elif e.value == self.profile_manager.cur_prf:
            self.logger.info("catch same values")
        # if e.value == "No Profile":

        else:
            name = e.value
            self.profile_manager.load_profile(name)
            self._refresh_inp()
            self.set_btns(True)
            Config_Manager().save_config(".config/cfg.json", self.profile_manager.config)

    def _refresh_inp(self, clear=False):
        self.logger.info("Refresh Input Buttons")
        if clear:
            self.dir_inp.clear()
            self.rtf_inp.clear()
        else:
            self.dir_inp.value = self.profile_manager.prf_cfg['img_dir']
            self.rtf_inp.value = self.profile_manager.prf_cfg['rtf']

    def _create_profile(self, ent, c):
        name = ent.value
        self.profile_manager.create_profile(name)
        ent.clear()
        c.add_item(name)

    def _delete_profile(self, c):
        prf = c.value
        self.profile_manager.delete_profile(prf)
        c.remove_item(prf)
        self._refresh_inp(True)
        self.set_btns(False)

    def _throw_error(self, msg):
        self.logger.info("Error window {}:".format(msg))
        self.main_window.error_dialog('Error', msg)

    def _show_info(self, msg):
        self.logger.info("Info window: {}".format(msg))
        self.main_window.info_dialog("Info", msg)

    def action_select_folder_dialog(self, widget):
        self.logger.info("Select Folder...")
        try:
            path_names = self.main_window.select_folder_dialog(
                title="Select image root folder"
            )
            self.dir_inp.value = path_names[0]+"/"
            self.prf_cfg['img_dir'] = path_names[0]+"/"
            Config_Manager.save_config(".config/"+self.profile_manager.cur_prf+".json", self.profile_manager.prf_cfg)

        except Exception:
            pass

    def action_open_file_dialog(self, widget):
        self.logger.info("Select File...")
        try:
            fname = self.main_window.open_file_dialog(
                title="Open RTF file",
                multiselect=False,
                file_types=['rtf']
            )
            self.logger.info("Created file-dialog")
            if fname is not None:
                self.rtf_inp.value = fname
                self.prf_cfg['rtf'] = fname
                Config_Manager.save_config(".config/"+self.profile_manager.cur_prf+".json", self.profile_manager.prf_cfg)
            else:
                self.prf_cfg['rtf'] = ""
                self.rtf_inp.value = ""
                Config_Manager.save_config(".config/"+self.profile_manager.cur_prf+".json", self.profile_manager.prf_cfg)
        except Exception:
            self.logger.error("Fatal error in main loop", exc_info=True)
            pass

    def _replace_faces(self, widget):
        self.logger.info("Start Replace Faces")
        # get values from UI elements
        rtf = self.profile_manager.prf_cfg['rtf']
        img_dir = self.profile_manager.prf_cfg['img_dir']
        profile = self.profile_manager.cur_prf
        mode = self.genmde_lst.value
        self.logger.info("rtf: {}".format(rtf))
        self.logger.info("img_dir: {}".format(img_dir))
        self.logger.info("profile: {}".format(profile))
        self.logger.info("mode: {}".format(mode))
        # parse rtf
        self.gen_prg.update_label("Parsing RTF")
        rtf_data = RTF_Parser().parse_rtf(rtf)
        self.gen_prg.update_label("Load profile config and create image set...")
        # prf_imgs = set(prf_cfg["imgs"].values())
        self.gen_prg.update_label("Restore already replaced faces if applicable...")

        # map rtf_data to ethnicities
        self.gen_prg.update_label("Map player to ethnicity...")
        mapping_data = Mapper(img_dir, self.profile_manager).generate_mapping(rtf_data, mode)

        self.profile_manager.write_xml(mapping_data)
        # save profile metadata (used pics and config.xml)
        self.gen_prg.update_label("Generate config.xml...")
        self.gen_prg.update_label("Save metadata for profile...")

        Config_Manager.save_config(".config/"+profile+".json", self.profile_manager.prf_cfg)
        self.gen_prg.value += 10
        self.gen_prg.update_label("Finished! :)")
        self._show_info("Finished! :)")
        self.gen_prg.reset()

    def change_image(self, id):
        self.logger.info("try to change image preview")
        uid = id.value
        try:
            img_name = self.prf_cfg["imgs"][uid]
            img_eth = self.prf_cfg["ethnics"][uid]
            img_path = self.prf_cfg["img_dir"] + "/" + img_eth + "/" + img_name
            self.rep_img.image = toga.Image(img_path)
            self.logger.info("change image preview to: {}".format(img_path))
        except Exception:
            self.logger.info("changing image preview failed!")
            return

    def send_report(self, e):
        uid = self.rep_inp.value
        img_name = self.prf_cfg["imgs"][uid]
        img_eth = self.prf_cfg["ethnics"][uid]
        img_path = img_eth + "/" + img_name
        img_file = self.rep_img.image.path
        self.logger.info("send report: {}".format(img_file))

        hook = Webhook("https://discord.com/api/webhooks/770397581149863946/Wls0g6LEyTXEpOqzfLn2YuDRKANFSAFpwKe62VL9IxpwsQDWFjYHVfy19hrYiv5p0X2a")

        embed = Embed(
            description='A user reported the following face',
            color=0x5CDBF0,
            timestamp='now'  # sets the timestamp to current time
            )

        file = File(img_file)
        embed.add_field(name='File', value=img_path)

        hook.send(embed=embed, file=file)
        self._show_info("Thanks for Reporting!")


def main():
    # create logger with 'spam_application'
    logger = logging.getLogger('NewGAN Logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('newgan.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    try:
        return NewGANManager(logger)
    except Exception:
        logger.error("Fatal error in main loop", exc_info=True)
