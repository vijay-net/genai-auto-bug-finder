
import subprocess

def add_item(item, items=[]):
    items.append(item)
    return items

try:
    val = eval(input('Enter value: '))
except:
    pass

subprocess.Popen('ls', shell=True)
