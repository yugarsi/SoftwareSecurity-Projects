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
            hosts = os.popen("cat "+fileName+" |grep HostName").read()
            allhosts = [host.replace("HostName","").strip() for host in hosts.strip().split("\n")]


        elif "authorized_keys" in fileName:
            hosts = os.popen("cat "+fileName).read()
            allhosts = [host.split()[2].rpartition("@")[2] for host in hosts.strip().split("\n")]

        elif "/etc/hosts" in fileName:
            hosts = os.popen("cat "+fileName).read()
            hosts = [ host.split()[1:] for host in hosts.strip().split("\n") if (host and host[0]!="#")]
            for h in hosts:
                for h1 in h:
                    allhosts.append(h1)



        # else:
        #     lines = file.readlines()
        #     for line in lines:
        #         line = line.strip()
        #         if line[0] != "#":
        #             host = line.split()
        #             if fileName == "/etc/hosts":
        #                 allhosts = allhosts+host[1:]
        #
        #             else:
        #                 allhosts.append(host[0].split(",")[0])


        # else:
        #     lines = file.readlines()
        #     for line in lines:
        #         host = line.strip().split()
        #         #host = line.split()
        #         for i in host:
        #             if '#' in i:
        #                 break
        #             else:
        #                 allhosts = allhosts+host[1:]

        print allhosts
        return allhosts

    except:
        return []
        #print "File not found"






def main():
    allhosts = []
    sysFiles = ["/etc/hosts"]#,"/etc/ssh/ssh_config", "/etc/ssh/ssh_known_hosts"]
    userFiles = ["/.ssh/config","/.ssh/authorized_keys","/.ssh/known_hosts"]


    for file in sysFiles:
        hosts = getHostnames(file)
        for host in hosts:
            print(host)

    # allusers = getAllUsers()
    # #allusers.append("yugarsi")
    # #print allusers
    # for user in allusers:
    #     path = "/home/"+user
    #     for file in userFiles:
    #         #print path+file
    #         hosts = getHostnames(path+file)
    #         for host in hosts:
    #             print(host)






if __name__=="__main__":
    main()