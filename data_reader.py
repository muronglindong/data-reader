#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter as tk
import code
from data_window import *

def main():
    data_window_display = data_window(height=800)
    tk.mainloop()
    return data_window_display.data_dict

if __name__ == '__main__':
    data = main()
    # code.interact(banner = "", local = locals())