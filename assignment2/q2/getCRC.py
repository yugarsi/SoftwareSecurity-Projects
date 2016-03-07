import os
import time
import subprocess

target = 2695300100
while 1:
    with open("example", "a") as myfile:
            myfile.write("0")

    myfile.close()
    command = "cksum example"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = process.communicate()
    cksum = int((output[0]).split()[0])
    if target == cksum:
        break
