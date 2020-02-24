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

        self.B_folder = Button(self.frame, font=widgets_font, text="Select Folder", width=10, justify=CENTER)
        self.B_folder.grid(row=1, column=0, padx=20, pady=10, sticky=W + E)

        self.B = Button(self.frame, text="Download", font=widgets_font, width=20, bg='#54FA9B', justify=CENTER)
        self.B.grid(row=1, column=1, pady=10, padx=20, sticky=W + E)

        E2_font = Font(family="Times New Roman", size=15)
        self.E2 = Text(self.frame, state=DISABLED, pady=3, padx=10, font=E2_font, background="black",
                       foreground="green")
        self.E2.grid(row=2, column=0, columnspan=2, sticky=W + E, ipadx=10, padx=10, pady=10)

    def screen_show(self):
        self.frame.mainloop()

    def append_text(self, string):
        self.E2.configure(state=NORMAL)
        self.E2.insert(END, string)
        self.E2.configure(state=DISABLED)

    def select_folder(self):
        self.directory = filedialog.askdirectory(initialdir="./")
