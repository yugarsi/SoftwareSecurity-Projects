import itertools
s='abcd'
def getSubstring(s):
    j=len(s)
    subs = []
    for k in range(1,j+1):
        for i in range (j-(k-1)):
            subs.append("".join(s[i:i+k]))
    return subs


n = input()
for line in range(n):
    s = raw_input()

    sum=0
    count=1
    for i in range(1,len(s)):
        if s[i-1] != s[i]:
            count=count+1
        else:
            sum += count*(count+1)/2
            count=1

    sum = sum+count*(count+1)/2
    print sum