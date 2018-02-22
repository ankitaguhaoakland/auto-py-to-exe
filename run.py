import eel
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import os
import subprocess
import sys
import shutil

eel.init('web')

@eel.expose
def askFile():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    filename = askopenfilename(parent=root)
    return filename

@eel.expose
def checkIfFileExists(file):
    return os.path.isfile(file)

@eel.expose
def convert(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(process.stderr.readline, ''):
        if line == b'':
            break
        eel.addOutput(line.decode('utf-8'))
    eel.outputComplete()
    moveProject()
    clean()

def moveProject():
    if not os.path.exists('output/'):
        os.makedirs('output/')
    folder = 'dist/' + os.listdir('dist/')[0]
    shutil.move(folder, 'output/')

def clean():
    shutil.rmtree('dist/')
    shutil.rmtree('build/')
    files = os.listdir('.')
    for file in files:
        if file.endswith('.spec'):
            os.remove(file)

eel.start('main.html', size=(650, 550))
