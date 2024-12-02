from datetime import datetime

def updateLog(type, message):
    year = datetime.today().strftime('%Y')
    file_name = '../log/' + str(year) + '.txt'
    file = open(file_name, 'a+')
    
    full_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    if (type == 'name'):
        file.write(str(full_date) + ' - ' + str(message) + ' logged in \n')
        
    file.close()