"""
Name: Phuc Le
Assignment 1: Null MSA Code
"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread


def handle_incoming_email(connectionSocket: socket):
    # Read AT MOST 1024 bytes from the socket
    # decode(): converts bytes to text
    # encode(): convert text to bytes
    connectionSocket.sendall("220 nusa.foo.net\r\n".encode())

    text = connectionSocket.recv(1024).decode()
    if text == "EHLO [127.0.0.1]\r\n":
        connectionSocket.sendall("502 OK\r\n".encode())
    else:
        connectionSocket.sendall("550 Error in Email Handshake\r\n".encode())
        connectionSocket.close()
        return

    text = connectionSocket.recv(1024).decode()
    if text == "HELO [127.0.0.1]\r\n":
        connectionSocket.sendall("250 OK\r\n".encode())
    else:
        connectionSocket.sendall("550 Error in Email Handshake\r\n".encode())
        connectionSocket.close()
        return

    text = connectionSocket.recv(1024).decode()
    _, sender = text.split("FROM:")
    if text == f"MAIL FROM:{sender}":
        connectionSocket.sendall("250 OK\r\n".encode())
    else:
        connectionSocket.sendall("550 Error in Email Handshake\r\n".encode())
        connectionSocket.close()
        return

    text = connectionSocket.recv(1024).decode()
    recipients = 0
    while "RCPT TO:" in text:
        recipients += 1
        if recipients > 5:
            connectionSocket.sendall(f"550 More than 5 recipients\r\n".encode())
            connectionSocket.close()
            return
        _, recipient = text.split("TO:")
        if recipient.count('@') > 1:
            connectionSocket.sendall(f"550 Accepts Only 1 @ Per Email\r\n".encode())
            connectionSocket.close()
            return
        username, domain = recipient.split('@')
        tokens = domain.split('.')
        domain = tokens[0:-1]
        domain = ''.join(domain)
        tld = tokens[-1]
        username = username[1:]
        if len(username) == 0:
            connectionSocket.sendall(f"550 Username Can't Be Empty\r\n".encode())
            connectionSocket.close()
            return
        elif len(domain) == 0:
            connectionSocket.sendall(f"550 Domain Can't Be Empty\r\n".encode())
            connectionSocket.close()
            return
        elif domain.isalnum() is False:
            connectionSocket.sendall(f"550 Domain Must Be Alphanumeric\r\n".encode())
            connectionSocket.close()
            return
        tld = '.' + tld[:-3]
        if tld not in ['.com', '.org', '.net', '.edu', '.io', '.app']:
            connectionSocket.sendall(f"550 Unknown TLD\r\n".encode())
            connectionSocket.close()
            return
        elif text == f"RCPT TO:{recipient}":
            connectionSocket.sendall("250 OK\r\n".encode())
        else:
            connectionSocket.sendall("550 Error in Email Handshake\r\n".encode())
            connectionSocket.close()
            return
        text = connectionSocket.recv(1024).decode()

    if text == "DATA\r\n":
        connectionSocket.sendall("354 OK\r\n".encode())
    else:
        connectionSocket.sendall("550 Error in Email Handshake\r\n".encode())
        connectionSocket.close()
        return

    text = connectionSocket.recv(1024)

    # If no subject line, send error
    if 'Subject: '.encode() not in text:
        connectionSocket.sendall("451 No Subject Line\r\n".encode())
        connectionSocket.close()
        return

    boundary = ''.encode()
    if "boundary=".encode() in text:
        _, boundary = text.split("boundary=".encode(), 1)
        boundary, _ = boundary.split("\r\n".encode(), 1)
        boundary = boundary[1:-1]
    print("Incoming text is:")
    while True:
        text_buff = connectionSocket.recv(1024)
        if ".\r\n".encode() in text_buff:
            text += text_buff
            break
        else:
            text += text_buff
    if boundary in text:
        if text.count("filename=".encode()) > 5:
            connectionSocket.sendall("550 More than 5 Attachments\r\n".encode())
            connectionSocket.close()
            return
    if boundary:
        text = text.split(boundary)
        text[0] = text[0] + text[1]
        text.pop(1)
        for i in range(len(text) - 1):
            text[i] = text[i] + boundary
            print(text[i].decode())
        print(text[-1].decode())
    else:
        print(text.decode())

    # Ending handshake
    connectionSocket.sendall("250 OK\r\n".encode())
    text = connectionSocket.recv(1024).decode()
    if text == "QUIT\r\n":
        connectionSocket.sendall("221 OK\r\n".encode())
    else:
        connectionSocket.sendall("550 ERROR\r\n".encode())
    connectionSocket.close()
    return


def main():
    # Create a TCP socket that listens to port 9000 on the local host
    welcomeSocket = socket(AF_INET, SOCK_STREAM)
    welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    welcomeSocket.bind(("", 9000))
    welcomeSocket.listen(4)    # Max backlog 4 connections
    print('Server is listening on port 9000')

    connectionSocket, addr = welcomeSocket.accept()
    print("Accept a new connection", addr)
    t = Thread(target=handle_incoming_email, args=[connectionSocket])
    t.start()
    while True:
        connectionSocket, addr = welcomeSocket.accept()
        print("Accept a new connection", addr)
        t1 = Thread(target=handle_incoming_email, args=[connectionSocket])
        t1.start()
    welcomeSocket.close()
    print("End of server")


if __name__ == "__main__":
    main()
