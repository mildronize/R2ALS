'''
config.py
Description#   Configuration of the system
Developer#     Thada Wangthammang
'''
import os

# global variable
db_name = 'r2alsdb'
db_name_test = 'r2alsdb_test'
host = 'localhost'
is_reset = True
root_path = os.path.dirname(os.path.dirname(__file__))+'/'
data_path = root_path + 'data/'
