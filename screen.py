from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
import platform
import subprocess


class Screen:

    def __init__(self):
        self.frame = Tk()
        self.frame.configure(bg='gray')
        self.frame.resizable(width=False, height=False)
        self.directory = None
        self.frame.title('Youtube & Spotify mp3 Downloader')

        widgets_font = Font(family="Tahoma", weight='bold', size=15)
        buttons_font = Font(family='Tahoma', size=13)
        # URL Area Part
        self.url_labelframe = LabelFrame(self.frame, bg='gray', bd=0)
        self.url_labelframe.grid(row=0, column=1)

        self.L1 = Label(self.url_labelframe, bg='gray', font=widgets_font, text="URL:")
        self.L1.grid(row=0, column=0, sticky=E, pady=10)

        self.url_field = Entry(self.url_labelframe, bd=3, width=40)
        self.url_field.grid(row=0, column=1, sticky=W, ipadx=40, pady=10)

        # Download Button Part
        self.download_btn = Button(self.frame, text="Download", font=widgets_font,
                                   width=45, bg='green', justify=CENTER, bd=0)
        self.download_btn.grid(row=1, column=1, pady=10, padx=23, sticky=E)

        # Buttons Part
        self.buttons_labelframe = LabelFrame(self.frame, bg='gray', bd=0)
        self.buttons_labelframe.grid(row=0, column=0, rowspan=2, padx=10, pady=4, )

        self.delete_icon = PhotoImage(file=r"icon/clear_console.png").subsample(1, 2)

        self.folder_btn = Button(self.buttons_labelframe, font=buttons_font, text="Select Folder", justify=CENTER, bd=0)
        self.folder_btn.grid(row=0, column=0, pady=2, sticky=W + E)

        self.open_folder_btn = Button(self.buttons_labelframe, font=buttons_font, text="Open Folder", justify=CENTER,
                                      bd=0)
        self.open_folder_btn.grid(row=1, column=0, pady=2, sticky=W + E)

        self.clear_console_btn = Button(self.buttons_labelframe, image=self.delete_icon, height=20, bd=0)
        self.clear_console_btn.grid(row=2, column=0, pady=2, sticky=W + E)

        # Console Part
        E2_font = Font(family="Times New Roman", size=15)
        self.console = Text(self.frame, state=DISABLED, pady=3, padx=10, font=E2_font, background="black",
                            foreground="green")
        self.console.grid(row=2, column=0, columnspan=2, sticky=W + E, ipadx=10, padx=10, pady=10)

    def screen_show(self):
        self.frame.mainloop()

    def append_text(self, string):
        self.console.configure(state=NORMAL)
        self.console.insert(END, string)
        self.console.configure(state=DISABLED)

    def open_folder(self):
        if self.directory:
            if platform.system() == "Windows":
                subprocess.check_call(["explorer", "/select", self.directory])
            else:
                subprocess.check_call(["open", "--", self.directory])

    def select_folder(self):
        self.directory = filedialog.askdirectory(initialdir="../")
        self.append_text(self.directory + '\n')

    def clear_console(self):
        self.console.configure(state=NORMAL)
        self.console.delete('1.0', END)
        self.console.configure(state=DISABLED)
