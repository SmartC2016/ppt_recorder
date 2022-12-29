"""
Dies ist ein kleines Programm, welches Screenshots macht und die in einem gegebenen Folder abspeichert
Inspiriert durch: https://youtu.be/iM3kjbbKHQU
customtkinter: https://github.com/TomSchimansky/CustomTkinter
pynput: https://pynput.readthedocs.io/en/latest/keyboard.html#
pynput help: https://nitratine.net/blog/post/how-to-make-hotkeys-in-python/
Inspieriert durch das "complex" example
29.12.2022 - Christian Hetmann
"""

import customtkinter
import tkinter
import platform  # to identify the OS running on
import sys  # to terminate the script
import datetime
from pathlib import Path
from pynput import keyboard
from PIL import Image, ImageGrab
from index_html import index_html

DESC_TEXT = "Put your description here ..."

# Identify the Operating system
USED_OS = platform.system()

# the key combinations to check
if USED_OS == "Darwin":
    COMBINATIONS = [{keyboard.Key.cmd, keyboard.Key.ctrl, keyboard.KeyCode(char="1")}]
    COMBO_TEXT = " For Screenshot press 'CMD + Ctrl + 1' "
elif USED_OS == "Windows":
    # The Windows Key is also named cmd in pynput
    COMBINATIONS = [{keyboard.Key.cmd, keyboard.Key.ctrl, keyboard.KeyCode(char="1")}]
    COMBO_TEXT = " For Screenshot press 'Windows + Ctrl + 1' "
else:
    print("This script only runs on MacOS or Windows. Sorry, not compatible.")
    print(f"And this is: {platform.system()} - Release {platform.release()}")
    sys.exit()

current = set()


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            app.make_screenshot()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
    # try:
    #     if any([key in COMBO for COMBO in COMBINATIONS]):
    #         if key in current:
    #             current.remove(key)
    # except KeyError:
    #     pass


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # set some status
        self.IS_FOLDER_SELECTED = False
        self.IS_TITLE_GIVEN = False
        self.USE_DATE_PREFIX = True
        self.list_of_pics = list()
        self.selected_folder = None  # later a path object
        self.original_title = ""
        self.title_folder = None  # later a path object
        self.img_folder = None  # later a path object
        self.today = datetime.datetime.now().date()
        self.description = None
        self.chkbox_var = customtkinter.StringVar(
            master=self, value="on"
        )  # default = On
        self.saveHTML_var = customtkinter.BooleanVar(
            master=self,
            value=True,
        )  # default = True
        self.radio_var = customtkinter.IntVar(
            master=self,
            value=1,
        )
        self.counter = 0
        self.counter_var = customtkinter.IntVar(
            master=self,
            value=0,
        )

        # configure window
        self.title("Presentation Recorder")
        self.geometry(f"{500}x{810}")

        self.title_label = customtkinter.CTkLabel(
            master=self,
            text="Presentation Recorder",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.pack(pady=10, padx=10)

        # Title-Text in Title-Frame
        self.title_text = """This app can take screenshots on demand and saves the screenshots including a title and a description to a given folder.\n\n"""
        self.title_text += """1. Select Title (of the meeting e.g.)\n2. Select Folder\n3. Start making Screenshots"""
        self.title_text_label = customtkinter.CTkLabel(
            master=self,
            wraplength=450,
            justify=customtkinter.CENTER,
            text=self.title_text,
            font=customtkinter.CTkFont(size=12, weight="normal"),
        )
        self.title_text_label.pack(pady=10, padx=10)

        self.btn_enter_title = customtkinter.CTkButton(
            master=self,
            text="Enter the title",
            width=400,
            command=self.open_title_input_dialog_event,
        )
        self.btn_enter_title.pack(pady=(20, 10), padx=10)

        self.entry_title = customtkinter.CTkEntry(
            master=self,
            placeholder_text="None",
            width=400,
        )
        self.entry_title.configure(state="disabled")
        self.entry_title.pack(pady=10, padx=10)

        self.chkbox_save_as_html = customtkinter.CTkCheckBox(
            master=self,
            text="Save Pictures including HTML-File to watch the files in a browser",
            variable=self.saveHTML_var,
        )
        self.chkbox_save_as_html.pack(pady=20, padx=10)

        self.chkbox_date_prefix = customtkinter.CTkCheckBox(
            master=self,
            text="Use Date as Prefix for the folder name",
            onvalue="on",
            offvalue="off",
            variable=self.chkbox_var,
        )
        self.chkbox_date_prefix.pack(pady=(10, 15), padx=10)

        self.btn_select_folder = customtkinter.CTkButton(
            master=self,
            text="Select folder to store pictures",
            width=400,
            command=self.select_folder,
        )
        self.btn_select_folder.pack(pady=10, padx=10)

        self.entry_selected_folder = customtkinter.CTkEntry(
            master=self,
            placeholder_text="None",
            width=400,
        )
        self.entry_selected_folder.configure(state="disabled")
        self.entry_selected_folder.pack(pady=10, padx=10)

        self.description_label = customtkinter.CTkLabel(
            master=self,
            text="Put Your description below (optional)",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.description_label.pack(pady=10, padx=10)

        self.description_textbox = customtkinter.CTkTextbox(
            master=self,
            width=400,
            height=75,
        )
        self.description_textbox.pack(pady=10, padx=10)
        self.description_textbox.insert("0.0", DESC_TEXT)

        self.radio_frame = customtkinter.CTkFrame(master=self, width=400)
        self.radio_frame.pack(padx=10, pady=10)

        self.radio1 = customtkinter.CTkRadioButton(
            master=self.radio_frame,
            text="Save as JPG",
            variable=self.radio_var,
            value=1,
        )
        self.radio2 = customtkinter.CTkRadioButton(
            master=self.radio_frame,
            text="Save as PNG",
            variable=self.radio_var,
            value=2,
        )
        self.radio1.grid(row=0, column=0, pady=10, padx=10, sticky="n")
        self.radio2.grid(row=0, column=1, pady=10, padx=10, sticky="n")

        self.hotkey_label = customtkinter.CTkLabel(
            master=self,
            text=COMBO_TEXT,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color=("#2CC985", "#2FA572"),
            corner_radius=8,
        )
        self.hotkey_label.pack(pady=(25, 10), padx=10)

        self.screenshot_counter_frame = customtkinter.CTkFrame(master=self, width=400)
        self.screenshot_counter_frame.pack(pady=10, padx=10)

        self.btn_reset = customtkinter.CTkButton(
            master=self.screenshot_counter_frame,
            text="Reset all Values!",
            fg_color="#E30000",
            hover_color="#B80000",
            command=self.reset_variables,
        )

        self.sc_label1 = customtkinter.CTkLabel(
            master=self.screenshot_counter_frame,
            text="Screenshots done:",
        )

        self.sc_label2 = customtkinter.CTkLabel(
            master=self.screenshot_counter_frame,
            textvariable=self.counter_var,
        )
        self.sc_label1.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.sc_label2.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        self.btn_reset.grid(row=0, column=2, pady=10, padx=10, sticky="e")

    def reset_variables(self):
        """Put all variables to the state of the beginning"""
        self.freeze_settings(state="normal")

        self.IS_FOLDER_SELECTED = False
        self.IS_TITLE_GIVEN = False
        self.USE_DATE_PREFIX = True
        self.list_of_pics = list()
        self.selected_folder = None  # later a path object
        self.title_folder = None  # later a path object
        self.img_folder = None  # later a path object
        self.today = datetime.datetime.now().date()
        self.original_title = ""
        self.description = None
        self.counter_var.set(0)
        self.counter = 0
        self.chkbox_var.set("on")
        self.saveHTML_var.set(True)
        self.radio_var.set(1)

        self.entry_title.configure(state="normal")
        self.entry_title.delete(0, "end")  # delete old title
        self.entry_title.configure(state="disabled")

        self.entry_selected_folder.configure(state="normal")
        self.entry_selected_folder.delete(0, customtkinter.END)
        self.entry_selected_folder.configure(state="disabled")

        self.description_textbox.delete("1.0", customtkinter.END)
        self.description_textbox.insert("0.0", DESC_TEXT)
        self.btn_enter_title.focus_set()

    def freeze_settings(self, state):
        """This function freezes all entries, when the first screenshot is made.
        So that the folders and so on can not be changed anymore
        Args:
            state (String): either 'disabled' or 'normal'
        """
        self.btn_select_folder.configure(state=state)
        self.btn_enter_title.configure(state=state)
        self.description_textbox.configure(state=state)
        self.radio1.configure(state=state)
        self.radio2.configure(state=state)
        self.chkbox_save_as_html.configure(state=state)
        self.chkbox_date_prefix.configure(state=state)

    def put_folder_name_to_entry(self):
        """Putting the path into the entry field"""
        self.entry_selected_folder.configure(state="normal")
        self.entry_selected_folder.insert(0, self.title_folder)
        self.entry_selected_folder.configure(state="disabled")

    def create_folders(self):
        """This function creates the needed folders"""
        # if the folder already exists !
        if self.title_folder.exists():
            self.show_error_title_exists()
        else:
            self.title_folder.mkdir()
            # Adding and creating a subfolder for the images
            # This should only be done, when saving as HTML
            if self.saveHTML_var.get():
                self.img_folder.mkdir()

    def select_folder(self):
        """This function selects the folder where the files are stored"""
        if self.IS_TITLE_GIVEN:
            folder_selected = customtkinter.filedialog.askdirectory()
            if folder_selected:  # the user has selected a folder and not pressed Cancel
                self.IS_FOLDER_SELECTED = True
                self.selected_folder = Path(folder_selected)
                if self.chkbox_date_prefix.get() == "on":
                    # Adding the title to the selected parent folder
                    folder_to_save = f"{self.today:%y%m%d}_{self.entry_title.get()}"
                    self.title_folder = self.selected_folder.joinpath(folder_to_save)
                else:
                    self.title_folder = self.selected_folder.joinpath(
                        self.entry_title.get()
                    )
                if self.saveHTML_var.get():
                    self.img_folder = self.title_folder.joinpath("img")
                self.put_folder_name_to_entry()
        else:
            self.show_error_title_missing()

    def open_title_input_dialog_event(self):
        """Opens a dialog to enter the TITLE and puts the title to the entry element"""
        dialog = customtkinter.CTkInputDialog(
            text="Enter the title. Will be used as folder and filename for the pictures.",
            title="Enter Title",
        )
        title = dialog.get_input()
        # Change the title if needed so that a file and directory can be created
        # remove "special" characters
        # Thank you Stack Overflow
        # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
        self.original_title = title
        title = "".join(x for x in title if (x.isalnum() or x in "_-"))
        if title:
            self.entry_title.configure(state="normal")
            self.entry_title.delete(0, "end")  # delete old title
            self.entry_title.insert(0, title)
            self.entry_title.configure(state="disabled")
            self.IS_TITLE_GIVEN = True
            self.btn_select_folder.focus_set()
        else:
            # a previously entered title has been overwritten
            # by confirming the dialog window empty
            self.entry_title.configure(state="normal")
            self.entry_title.delete(0, "end")
            self.entry_title.configure(state="disabled")
            self.IS_TITLE_GIVEN = False

    def make_screenshot(self):
        """Making the screenshot and saving it"""
        if self.IS_FOLDER_SELECTED:
            # the folders are created only once at the very beginning
            if self.counter == 0:
                self.create_folders()
                self.freeze_settings(state="disabled")
            now = datetime.datetime.now()
            now_str = f"{now:%y%m%d_%H%M%S}"
            size = (1920, 1080)
            im = ImageGrab.grab(bbox=None)
            im = im.resize(size, resample=Image.Resampling.LANCZOS)
            # Check how it should get saved
            if self.radio_var.get() == 1:  # save as jpg
                im = im.convert("RGB")
                filename = f"{now_str}_{self.entry_title.get()}.jpg"
            else:  # save as png
                filename = f"{now_str}_{self.entry_title.get()}.png"
            if self.saveHTML_var.get():  # save html is true
                im.save(self.img_folder.joinpath(filename))
                self.list_of_pics.append(filename)
                self.save_as_html()
            else:
                im.save(self.title_folder.joinpath(filename))
                self.list_of_pics.append(filename)
            im.close()
            self.counter += 1
            self.counter_var.set(self.counter)
        else:
            self.show_error_no_folder_selected()

    def save_as_html(self):
        # If HTML already exists, this needs to be deleted
        # as there is one more picture and this has to be given to the JS-List
        html_file = self.title_folder.joinpath("index.html")
        if html_file.exists():
            html_file.unlink()

        html = index_html
        # Replace does not work inplace, it has to be a new variable
        title_window = self.original_title
        new_title_browser = f"{title_window}"
        new_title = f"{title_window} - {self.today}"
        html = html.replace("--TITLE-BROWSER--", new_title_browser)
        html = html.replace("--TITLE--", new_title)
        html = html.replace("--LIST_OF_PICS--", str(self.list_of_pics))
        desc_text = self.description_textbox.get("0.0", "end")
        # In the text box there are /n added, I need to get rid for comparison
        if desc_text[:28] != DESC_TEXT[:28]:
            html = html.replace("--DESCRIPTION--", desc_text)
        else:
            html = html.replace("--DESCRIPTION--", "")
        with open(html_file, "w") as opened_file:
            opened_file.write(html)

    def show_error_title_missing(self):
        tkinter.messagebox.showerror(
            "You have to give a title first!",
            "You have to give a title first!",
        )

    def show_error_no_folder_selected(self):
        tkinter.messagebox.showerror(
            "You have to select a folder first!",
            "You have to select a folder first!",
        )

    def show_error_title_exists(self):
        tkinter.messagebox.showerror(
            "Title is already existing!",
            "That title is already existing, cannot create folder! Choose different title!",
        )


if __name__ == "__main__":
    # pynput - listening to keyboard presses in order to make the screenshots
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
    )
    listener.start()
    app = App()
    app.mainloop()
