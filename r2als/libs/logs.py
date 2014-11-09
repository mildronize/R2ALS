# This is class log handler
import os
import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler

class Log:

    def __init__(self, module_name):
        self.logger_tmp = None
        logger = logging.getLogger(module_name)
        logging.basicConfig(filename='/tmp/r2als.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
        # logging.basicConfig(level=logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s")  # same as default

         # setup `RainbowLoggingHandler`
        handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'gray', True))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger_tmp = logger
    def getLogger(self):
        return self.logger_tmp

        # logger.debug("debug msg")
        # logger.info("info msg")
        # logger.warn("warn msg")
        # logger.error("error msg")
        # logger.critical("critical msg")

# import os
# from colorama import init
# from colorama import Fore, Back, Style
# import time
# from datetime import datetime, date
# class LogHandler:
#
#     file = None
#     colorRowInfo = 0
#     logDirectory = '/tmp/r2als-logs/'
#
#     def __init__(self):
#         filename = 'R2ALS-LOG_' + str(date.today()) + '.txt'
#         if not os.path.exists(self.logDirectory):
#             os.makedirs(self.logDirectory)
#         self.file = open(self.logDirectory+filename, 'a')
#         # file.write('write test\n')
#         init()
#
#     def terminalFormat(self, mode, text):
#         dt = datetime.now()
#         return "["+str(dt.strftime("%H:%M:%S")) + "] " + mode.upper() + ": " + text
#
#     def fileFormat(self, mode, text):
#         return str(datetime.now()) + ',' + mode[0].upper() + ',"' + text + '"\n'
#
#     def error(self, text):
#         # print to terminal
#         # coloring text
#         print(Fore.WHITE + Back.RED,end ="")
#         print(self.terminalFormat('error',text))
#         # reset color
#         print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
#         # write to file
#         self.file.write(self.fileFormat('error',text))
#
#     def info(self, text):
#         # print to terminal
#         # coloring text
#         if self.colorRowInfo % 2 == 0: print(Fore.CYAN,end ="")
#         else: print(Fore.WHITE,end ="")
#         print(self.terminalFormat('info',text))
#         # reset color
#         print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
#         # write to file
#         self.file.write(self.fileFormat('info',text))
#         self.colorRowInfo = self.colorRowInfo + 1
#
#     def success(self, text):
#         # print to terminal
#         # coloring text
#         print(Fore.GREEN,end ="")
#         print(self.terminalFormat('success',text))
#         # reset color
#         print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
#         # write to file
#         self.file.write(self.fileFormat('success',text))
#
#     def debug(self, text):
#         # print to terminal
#         # coloring text
#         print(Fore.MAGENTA,end ="")
#         print(self.terminalFormat('debug',text))
#         # reset color
#         print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
#         # write to file
#         self.file.write(self.fileFormat('debug',text))
#
#     def head(self, text):
#         # print to terminal
#         # coloring text
#         print(Fore.YELLOW,end ="")
#         print(self.terminalFormat('head',text))
#         # reset color
#         print(Fore.RESET + Back.RESET + Style.RESET_ALL,end ="")
#         # write to file
#         self.file.write(self.fileFormat('head',text))
#
#     def close(self):
#         self.file.close()
#
#     def startScript(self, name):
#         self.head("Starting script : " + name)
#         print("-"*10)
#
#     def startApp(self, name):
#         print("="*40)
#         self.head("Starting app : " + name)
#         print("="*40)
