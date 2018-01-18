import os

path = 'static'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)

latest = files[-1]

print latest
