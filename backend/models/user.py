import utils.log_handler

def set_user(self):
    global user
    print(self)
    user = self['first_name']
    
def get_user():
    global user
    return user