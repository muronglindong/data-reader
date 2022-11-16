#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
# import code
# import hashlib
# import queue
# import sys
# import threading
# import traceback
import tkinter as tk

import read_csv as rc

# from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
# from tkinter.scrolledtext import ScrolledText

from display_window import *
from console_widget import *
# from test import on_closing

class data_window:

    data_dict = {}
    display_windows = []

    def __init__(self, width = 800, height = 600):
        self.top = tk.Tk()
        self.top.title('数据阅读器')
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        init_position_x = int((screen_width - width) / 2)
        init_position_y = int((screen_height - height) / 2)
        position = str(width) + 'x' + str(height) + '+' + str(init_position_x) + '+' + str(init_position_y)
        self.top.geometry(position)
        
        self.count = 1
        new_display_window_button = tk.Button(self.top, text = '新建显示窗口', command = self.new_display_window_callback)
        new_display_window_button.place(x=10, y=90, width=135)
        # new_display_window_button.pack()

        self.open_dir = '/home/mu/bp/bp0_0/install/state/share/state/record'
        open_file_button = tk.Button(self.top, text = '导入数据', command = self.import_data_callback)
        # open_file_button.pack()
        open_file_button.place(x=10, y=10, width=135)

        open_file_button = tk.Button(self.top, text = '增加数据', command = self.add_data_callback)
        # open_file_button.pack()
        open_file_button.place(x=10, y=50, width=135)

        self.data_list = tk.Listbox(self.top)
        # self.data_list.yview_scroll(1, 'unit')
        self.data_list.place(x=400, y=10, width=380, height=580)
        # self.data_list.pack()
        self.data_list.bind('<<ListboxSelect>>', self.listbox_click)

        self.console_widget = ConsoleText(self, wrap=tk.WORD)
        self.console_widget.place(x=10, y=600, width=580, height=190)
        
    def listbox_click(self, event):
        try:
            data_key = self.data_list.get(self.data_list.curselection())
            for display_window in self.display_windows:
                display_window.get_data_key(data_key)
        except tk.TclError:
            pass
        except UnboundLocalError:
            pass
        # print(data_key)

        #传递键值
        
        

    def new_display_window_callback(self):
        new_display_window = display_window(self.count, self.top)
        new_display_window.get_data(self.data_dict)
        self.display_windows.append(new_display_window)
        # print(len(self.new_display_windows))
        self.count += 1

    def add_data_callback(self):
        file_names = self.open_files()
        if file_names:
            for file_name in file_names:
                new_header = rc.read_csv_header(file_name)
                try:
                    if new_header != self.header:
                        showinfo(title='错误', message='数据格式不兼容')
                        # self.data_list.delete(0, tk.END)
                        # header.clear()
                        return
                except AttributeError:
                    showinfo(title='错误', message='未导入数据')
                    return
                    

            #重新读取文件获得数据
            for file_name in file_names:
                new_data_dict = rc.read_csv_data(file_name)
                self.joint_data(self.data_dict, new_data_dict)



    def import_data_callback(self):
        file_names = self.open_files()

        if file_names:
            self.close_all_display_windows()

            #判断表头是否一致
            for i, file_name in enumerate(file_names):
                if i:
                    new_header = rc.read_csv_header(file_name)
                    if new_header != self.header:
                        showinfo(title='错误', message='数据格式不兼容')
                        # self.data_list.delete(0, tk.END)
                        # header.clear()
                        return                        
                        

                else:
                    self.header = rc.read_csv_header(file_name)
                    # print(ord(self.header[-1]))
            
            #重新读取文件获得数据
            for i, file_name in enumerate(file_names):
                if i:
                    new_data_dict = rc.read_csv_data(file_name)
                    self.joint_data(self.data_dict, new_data_dict)
                else:
                    self.data_dict = rc.read_csv_data(file_name)
            
            # data_list_index = len(header)
            self.data_list.delete(0, tk.END)
            for it in self.header:
                self.data_list.insert(tk.END, it)

            # print(self.data_dict['IDX'][-1], len(self.data_dict['IDX']))

            
                

    def open_files(self):
        filetypes = (
            ('csv文件', '*.csv'),
            # ('数据阅读器文件', '*.dar'),
            ('所有文件', '*.*')
        )

        filenames = fd.askopenfilenames(
            title='打开',
            initialdir=self.open_dir,
            filetypes=filetypes
        )

        if filenames:
            sorted(filenames)
            self.open_dir = os.path.dirname(filenames[0])

        
        # showinfo(
        #     title='Selected File',
        #     message=filenames
        # )

        return filenames


    def close_all_display_windows(self):
        for display_window in self.display_windows:
            if display_window.isopen:
                display_window.display_level.destroy()
        self.display_windows.clear()
        self.count = 1

    # def close(self):
    #     self.close_all_display_windows()
    #     self.top.destroy()
        
    def joint_data(self, data, new_data):
        for k in data.keys():
            data[k] += new_data[k]