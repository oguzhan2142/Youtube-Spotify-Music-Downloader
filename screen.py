from tkinter import *
from tkinter import filedialog
from tkinter.font import Font


class Screen:

    def __init__(self):
        self.frame = Tk()
        self.directory = None

        self.frame.title('Youtube mp3 Downloader')

        self.L1 = Label(self.frame, text="URL")
        self.L1.grid(row=0, column=0, sticky=W + E, ipadx=10, padx=4, pady=10)

        self.url_field = Entry(self.frame, bd=3, width=40)
        self.url_field.grid(row=0, column=1, sticky=W, ipadx=10, padx=10, pady=10)

        self.B_folder = Button(self.frame, text="Select Folder", width=10, justify=CENTER)
        self.B_folder.grid(row=1, column=0, padx=20, pady=10, sticky=W + E)

        self.B = Button(self.frame, text="Download", width=20, bg='#54FA9B', justify=CENTER)
        self.B.grid(row=1, column=1, pady=10, padx=20, sticky=W + E)

        myFont = Font(family="Times New Roman", size=15)
        self.E2 = Text(self.frame, state=DISABLED, pady=3, padx=10, font=myFont, background="black", foreground="green")
        self.E2.grid(row=2, column=0, columnspan=2, sticky=W + E, ipadx=10, padx=10, pady=10)

    def screen_show(self):
        self.frame.mainloop()

    def append_text(self, string):
        self.E2.configure(state=NORMAL)
        self.E2.insert(END, string)
        self.E2.configure(state=DISABLED)

    def select_folder(self):
        self.directory = filedialog.askdirectory(initialdir="./")
