import os
def out():
    os.system('echo DISPLAY=:0')

def run(file):
    os.system('python3' + file)