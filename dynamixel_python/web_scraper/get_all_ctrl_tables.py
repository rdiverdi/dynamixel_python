from .get_ctrl_table import *
from .get_model_list import *

import pkg_resources

url='https://emanual.robotis.com/docs/en/dxl/'
#folder = '../control_tables'
folder = pkg_resources.resource_filename('dynamixel_python', 'control_tables')

def get_all_ctrl_tables():
    for series, model in get_model_list(url):
        try:
            build_model_json(series, model, folder)
            print('built json for ' + model)
        except Exception as e:
            print('failed to build json for ' + model)
            if 'HTTP' not in repr(e):
                raise e
