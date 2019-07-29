#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#forked from https://github.com/doudoudzj/tkinter-gui-ftp-server

pname="ftpServerTk"

import os
import sys
from tkinter import (Button, Entry, Frame, Label, StringVar, Tk, filedialog, messagebox)

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer

import _thread


class FTP(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(pname)
        self.set_window_center(self, 350, 180)
        self.resizable(False, False)
        self.update()

        self.server = None
        self.server_thread = None
        self.running = StringVar(value="normal")
        self.var_username = StringVar(value="username")
        self.var_passwd = StringVar(value="password")
        self.var_address = StringVar(value="127.0.0.1")
        self.var_port = StringVar(value="3333")
        self.var_path = StringVar(value="./sharedfiles") 

        self.entry_username = None
        self.entry_passwd = None
        self.entry_address = None
        self.entry_port = None
        self.entry_path = None

        self.load_view()

    def run_ftp(self):
        if os.path.isdir(self.var_path.get()) is not True:
            messagebox.showerror(title="error", message="The path is wrong", parent=self)
            return

        _thread.start_new_thread(self.ftpserver, ())
        self.fixed_entry("readonly")

    def stop_ftp(self):
        self.fixed_entry()
        if self.server:
            try:
                self.server.close()
            except Exception:
                print(Exception)

    def ftpserver(self):

        authorizer = DummyAuthorizer()

        authorizer.add_user(
            self.var_username.get(),
            self.var_passwd.get(),
            self.var_path.get(),
            perm="elradfmwMT")

        authorizer.add_anonymous(self.var_path.get(), msg_login="Welcome")

        handler = FTPHandler
        handler.authorizer = authorizer

        self.server = ThreadedFTPServer(
            (self.var_address.get(), self.var_port.get()), handler)

        self.server.serve_forever()

    def load_view(self):

        Label(self, text="user:").grid(column=0, row=0, sticky="nswe")
        self.entry_username = Entry(self, textvariable=self.var_username, bd=2)
        self.entry_username.grid(column=1, row=0, columnspan=2, sticky="nswe")

        Label(self, text="password:").grid(column=0, row=1, sticky="nswe")
        self.entry_passwd = Entry(self, textvariable=self.var_passwd, bd=2)
        self.entry_passwd.grid(column=1, row=1, columnspan=2, sticky="nswe")

        Label(self, text="address:").grid(column=0, row=2, sticky="nswe")
        self.entry_address = Entry(self, textvariable=self.var_address, bd=2)
        self.entry_address.grid(column=1, row=2, columnspan=2, sticky="nswe")

        Label(self, text="port:").grid(column=0, row=3, sticky="nswe")
        self.entry_port = Entry(self, textvariable=self.var_port, bd=2)
        self.entry_port.grid(column=1, row=3, columnspan=2, sticky="nswe")

        Label(self, text="shared files:").grid(column=0, row=4, sticky="nswe")
        self.entry_path = Entry(self, textvariable=self.var_path, bd=2)
        self.entry_path.grid(column=1, row=4)

        self.btn_select_path = Button(self, text="select", command=self.selectPath)
        self.btn_select_path.grid(column=2, row=4)

        btn_box = Frame(self, relief="ridge", borderwidth=0, bd=2)
        btn_box.grid(column=0, row=5, columnspan=3, sticky="nswe")

        self.btn_start = Button(btn_box, text="run", command=self.run_ftp)
        self.btn_start.pack(side="left")

        self.btn_stop = Button(
            btn_box, text="stop", command=self.stop_ftp, state="disable")
        self.btn_stop.pack(side="left")

    def selectPath(self):
        path = filedialog.askdirectory()
        if os.path.isdir(path):
            self.var_path.set(path)

    def fixed_entry(self, state="normal"):
        s = "readonly" if (state == "readonly") else "normal"
        a = "disable" if (state == "readonly") else "normal"
        self.entry_username["state"] = s
        self.entry_passwd["state"] = s
        self.entry_address["state"] = s
        self.entry_port["state"] = s
        self.entry_path["state"] = s
        self.btn_select_path["state"] = a
        self.btn_start["text"] = "Running" if (state == "readonly") else "start"
        self.btn_start["state"] = a
        self.btn_stop["state"] = "normal" if (
            state == "readonly") else "disable"

    def set_window_center(self, window, width, height):
        w_s = window.winfo_screenwidth()
        h_s = window.winfo_screenheight()
        x_co = (w_s - width) / 2
        y_co = (h_s - height) / 2 - 50
        window.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
        window.minsize(width, height)


if __name__ == "__main__":
    ftp = FTP()
    ftp.mainloop()
