import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import backend.utils.log_handler

def set_user(self):
    global user
    print(self)
    user = self['first_name']
    
def get_user():
    global user
    return user