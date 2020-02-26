from tkinter import *
from tkinter import filedialog
from tkinter.font import Font


class Screen:

    def __init__(self):
        self.frame = Tk()
        self.frame.configure(bg='gray')
        self.frame.resizable(width=False, height=False)
        self.directory = None
        self.frame.title('Youtube & Spotify mp3 Downloader')

        widgets_font = Font(family="Tahoma", weight='bold', size=15)
        self.L1 = Label(self.frame, bg='gray', font=widgets_font, text="URL:")
        self.L1.grid(row=0, column=0, sticky=W + E, padx=20, pady=10)

        self.url_field = Entry(self.frame, bd=3, width=40)
        self.url_field.grid(row=0, column=1, sticky=W + E, padx=18, pady=10)

        self.label_frame = LabelFrame(self.frame, bg='gray', bd=0)
        self.label_frame.grid(row=1, column=0, padx=20, pady=10, sticky=W + E)

        # Resizing image to fit on button
        self.delete_icon = PhotoImage(file=r"icon/clear_console.png").subsample(1, 2)
        self.clear_console_btn = Button(self.label_frame, image=self.delete_icon, height=20)
        self.clear_console_btn.grid(row=0, column=0, padx=5, ipadx=5)

        self.folder_btn = Button(self.label_frame, font=widgets_font, text="Select Folder", justify=CENTER)
        self.folder_btn.grid(row=0, column=1, padx=5)

        # download btn old color        #54FA9B
        self.download_btn = Button(self.frame, text="Download", font=widgets_font,
                                   width=20, bg='green', justify=CENTER)
        self.download_btn.grid(row=1, column=1, pady=10, padx=20, sticky=W + E)

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

    def select_folder(self):
        self.directory = filedialog.askdirectory(initialdir="./")

    def clear_console(self):
        self.console.configure(state=NORMAL)
        self.console.delete('1.0', END)
        self.console.configure(state=DISABLED)
