import os, sys

def get_error_msg(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    path = os.path.split(exc_tb.tb_frame.f_code.co_filename)[0].split('/')
    line_number = exc_tb.tb_lineno
    msg = "path {}, line {}: ".format(path[-2]+"/"+path[-1]+"/"+fname,line_number)+str(e)
    return msg