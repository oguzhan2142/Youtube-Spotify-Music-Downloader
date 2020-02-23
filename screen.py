from tkinter import *


class Screen:

    def __init__(self):
        self.frame = Tk()
        self.frame.title('Youtube mp3 Downloader')
        self.L1 = Label(self.frame, text="URL")
        self.L1.grid(row=0, column=0, sticky=W + E, ipadx=10, padx=10, pady=10)
        self.E1 = Entry(self.frame, bd=3, width=40)
        self.E1.grid(row=0, column=1, sticky=W + E, ipadx=10, padx=10, pady=10)

        self.B = Button(self.frame, text="Download", width=20, justify=CENTER)
        self.B.grid(row=1, column=0, columnspan=2, pady=10)

        self.status = StringVar(value='Status')

        # self.L2 = Label(self.frame, text="URL", textvariable=self.status)
        # self.E2 = Entry(self.frame, bd=3, width=40, state=DISABLED, textvariable=self.status)
        self.E2 = Text(self.frame, state=DISABLED)
        self.E2.grid(row=2, column=0, columnspan=2, sticky=W + E, ipadx=10, padx=10, pady=10)

    def screen_show(self):
        self.frame.mainloop()

    def append_text(self, string):
        self.E2.configure(state=NORMAL)
        self.E2.insert(END, string)
        self.E2.configure(state=DISABLED)
