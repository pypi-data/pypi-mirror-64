import os
import sys


def add_relative_search_path(relative_path_list):
    caller_file_path = sys._getframe(1).f_code.co_filename
    path_base = os.path.dirname(os.path.realpath(caller_file_path))

    for item in relative_path_list:
        path_final = "%s/%s" % (path_base, item)
        sys.path.append(path_final)
