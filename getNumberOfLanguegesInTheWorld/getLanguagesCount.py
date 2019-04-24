fname = 'languages.txt'
cnt = 0
with open(fname, 'r') as f:
    while True:
        l = f.readline()
        if not l: break;
        if l.find('(')==-1 : continue
        while l[l.find('(')+1]<'0' or l[l.find('(')+1]>'9':
            l = l[l.find(')')+1:]
        st = l[l.find('(')+1 : l.find(')')]
        if st[0]>='0' and st[0] <= '9': cnt+= int(st)
print(cnt) # which is 7474
