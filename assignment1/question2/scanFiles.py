
from os.path import expanduser
import re
import os


def getAllUsers():
    users = os.popen("cut -d: -f1 /etc/passwd").read()
    users = users.strip().split("\n")
    res = [user for user in users if user[0]!= "#"]
    return res

def getHostnames(fileName):
    allhosts = []
    try:
        file = open(fileName,"r")
        if "config" in fileName:
            hosts = os.popen("cat "+fileName+" |grep 'Host \|HostName'").read()
            hosts = [host.strip().split()[1:] for host in hosts.strip().split("\n") if (host and host.strip()[0]!="#")]
            for h in hosts:
                for h1 in h:
                    if any(c.isalpha() for c in h1):
                        allhosts.append(h1.strip())
            #print allhosts

        elif "authorized_keys" in fileName:
            hosts = os.popen("cat "+fileName).read()
            allhosts = [host.split()[2].rpartition("@")[-1] for host in hosts.strip().split("\n")if (host and host.strip()[0]!="#" and "@" in host)]

            hosts2 = os.popen("cat "+fileName +"|grep permitopen=").read()
            res2 = [host.rpartition('"')[0].replace('"','').split(",") for host in filter(None,hosts2.strip().split("permitopen=")) if (host and host.strip()[0]!="#")]
            for h in res2:
                for h1 in h:
                    allhosts.append(h1.partition(":")[0].strip())

            hosts3 = os.popen("cat "+fileName +"|grep from=").read()
            res3 = [host.rpartition('"')[0].replace('"','').split(",") for host in filter(None,hosts3.strip().split("from=")) if (host and host.strip()[0]!="#")]
            for h in res3:
                for h1 in h:
                    allhosts.append(h1.strip().partition(":")[0].strip())
            #print allhosts

        elif "/etc/hosts" in fileName:
            hosts = os.popen("cat "+fileName).read()
            hosts = [ host.split()[1:] for host in hosts.strip().split("\n") if (host and host.strip()[0]!="#")]
            for h in hosts:
                for h1 in h:
                    allhosts.append(h1.strip())
            #print allhosts

        else:
            hosts = os.popen("cat "+fileName).read()
            hosts = [ host.split()[0].split(",") for host in hosts.strip().split("\n") if (host and host.strip()[0]!="#")]
            for h in hosts:
                for host in h:
                    if any(c.isalpha() for c in host):
                        allhosts.append(host.strip())
            #print allhosts

        return allhosts

    except:

        return []



def runNetstat():
    allhosts = []
    hosts = os.popen("netstat -a |awk '{print $5}'").read()
    hosts = hosts.strip().split("\n")
    for host in hosts:
        h = host.split(":")[0]
        if(any(c.isalpha() for c in h) and "." in h):
            allhosts.append(host)
    return allhosts

def checkValidHostname(hostname):
    if len(hostname) > 255 or hostname.strip() == "" :
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def main():
    sysFiles = ["/etc/hosts","/etc/ssh/ssh_config", "/etc/ssh/ssh_known_hosts"]
    userFiles = ["/.ssh/config","/.ssh/authorized_keys","/.ssh/authorized_keys2","/.ssh/known_hosts"]


    for file in sysFiles:
        hosts = getHostnames(file)
        for host in list(set(hosts)):
            if checkValidHostname(host):
                print(host.strip())


    allusers = getAllUsers()
    #allusers.append("yugarsi")
    for user in allusers:
        path = "/home/"+user
        for file in userFiles:
            hosts = getHostnames(path+file)
            for host in list(set(hosts)):
                if checkValidHostname(host):
                    print(host.strip())






if __name__=="__main__":

    #path = "/Users/yugarsi/.ssh/authorized_keys"
    #print checkValidHostname("10.199.4.1")
    main()