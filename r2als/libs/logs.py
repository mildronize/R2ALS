# This is class log handler

from colorama import init
from colorama import Fore, Back, Style

import time
from datetime import datetime, date

class LogHandler:

    file = None
    colorRowInfo = 0

    def __init__(self):
        filename = 'LOG_' + str(date.today()) + '.txt'
        self.file = open('../logs/'+filename, 'a')
        # file.write('write test\n')
        init()

    def terminalFormat(self, mode, text):
        dt = datetime.now()
        return str(dt.strftime("%H:%M:%S")) + " " + mode.upper() + ": " + text

    def fileFormat(self, mode, text):
        return str(datetime.now()) + ',' + mode[0].upper() + ',"' + text + '"\n'

    def error(self, text):
        # print to terminal
        # coloring text
        print(Fore.WHITE + Back.RED,end ="")
        print(self.terminalFormat('error',text))
        # reset color
        print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
        # write to file
        self.file.write(self.fileFormat('error',text))

    def info(self, text):
        # print to terminal
        # coloring text
        if self.colorRowInfo % 2 == 0: print(Fore.CYAN,end ="")
        else: print(Fore.WHITE,end ="")
        print(self.terminalFormat('info',text))
        # reset color
        print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
        # write to file
        self.file.write(self.fileFormat('info',text))
        self.colorRowInfo = self.colorRowInfo + 1

    def success(self, text):
        # print to terminal
        # coloring text
        print(Fore.GREEN,end ="")
        print(self.terminalFormat('success',text))
        # reset color
        print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
        # write to file
        self.file.write(self.fileFormat('success',text))

    def debug(self, text):
        # print to terminal
        # coloring text
        print(Fore.MAGENTA,end ="")
        print(self.terminalFormat('debug',text))
        # reset color
        print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
        # write to file
        self.file.write(self.fileFormat('debug',text))

    def head(self, text):
        # print to terminal
        # coloring text
        print(Fore.YELLOW,end ="")
        print(self.terminalFormat('head',text))
        # reset color
        print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
        # write to file
        self.file.write(self.fileFormat('head',text))

    def close(self):
        self.file.close()

    def startScript(self, name):
        self.head("Starting script : " + name)
        print("-"*10)

    def startApp(self, name):
        print("="*40)
        self.head("Starting app : " + name)
        print("="*40)
