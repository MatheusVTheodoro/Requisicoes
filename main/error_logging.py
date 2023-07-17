import sys
import datetime

def excepthook(type, value, traceback):
    with open('erros.txt', 'a') as file:
        timestamp = datetime.datetime.now().strftime('''%d-%m-%Y %H:%M:%S''')
        file.write(f"\n###### - {timestamp} - ######\n Erro ocorrido:\n ")
        sys.stderr = file
        sys.__excepthook__(type, value, traceback)
        sys.stderr = sys.__stderr__