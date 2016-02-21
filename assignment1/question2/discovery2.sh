#!/bin/bash

# echo "Get all hostnames in /etc/hosts"
sed '/^#/ d' /etc/hosts | grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|[0-9]\:\:[0-9]' | awk -F' ' '{print $2}' > hostlist.txt 2>/dev/null

for user in `cat /etc/passwd | awk -F':' '{print $1}'`; do
	
	# echo "Get hostname in all users specific ssh config"
	if [ -f /home/$user/.ssh/config ]; then
		sed '/^#/ d' /home/$user/.ssh/config | grep 'Host \|HostName' | awk -F' ' '{print $2}' >> hostlist.txt 2>/dev/null
	fi

	# echo "Get hostname in system level ssh config"
	if [ -f /etc/ssh/ssh_config ]; then
		sed '/^#/ d' /etc/ssh/ssh_config | grep -i 'Host \|HostName' | awk -F' ' '{print $2}' >> hostlist.txt 2>/dev/null
	fi

	# echo "Get hostname for all hosts that is authorized for ssh client login"
	# echo "via protocol version 1 - identity.pub files of other hosts"
	if [ -f /home/$user/.ssh/authorized_keys ]; then
		sed '/^#/ d' /home/$user/.ssh/authorized_keys | awk -F' ' '{print $3}' | awk -F'@' '{print $2}' >> hostlist.txt 2>/dev/null	
	fi
	# echo "via protocol version 2 - id_rsa.pub files of other hosts"
	if [ -f /home/$user/.ssh/authorized_keys2 ]; then
		sed '/^#/ d' /home/$user/.ssh/authorized_keys2 | awk -F' ' '{print $3}' | awk -F'@' '{print $2}' >> hostlist.txt 2>/dev/null
	fi

	# echo "Get hostname in known host file"
	#if [ -f /home/$user/.ssh/known_hosts ]; then
		sed '/^#/ d' /Users/yugarsi/.ssh/known_hosts | grep ',' | awk -F',' '{print $1}'>> hostlist.txt 2>/dev/null
	#fi

        # echo "Get hostname in known host file"
	if [ -f /etc/ssh/ssh_known_hosts ]; then
		sed '/^#/ d' /etc/ssh/ssh_known_hosts | grep ',' | awk -F',' '{print $1}'>> hostlist.txt 2>/dev/null
	fi
done

# Do something extra
# echo "Getting all hostnames that have open connection with this host at present"
# netstat | awk -F' ' '{print $5}' | grep ':' | awk -F':' '{print $1}' | sort | uniq | grep -v -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' >> hostlist.txt
sed 's/^[ \t]*//g' hostlist.txt | grep -E "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$" | awk '!a[$0]++' 2>/dev/null
rm hostlist.txt
