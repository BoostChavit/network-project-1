from socket import *
import os
import json

dir = os.getcwd()

servername = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((servername, serverPort))

print('Connected to server!')

while True:
    try:
        command = input("Enter command: ")
        clientSocket.send(command.encode())

        if command == 'ls':
            data = clientSocket.recv(1024).decode()
            data = json.loads(data)
            print('From server:', data['data'])
        elif command == 'upload':
            filename = input("Enter file name to be stored: ")
            clientSocket.send(filename.encode())
            filed = input("Enter file name in the your directory: ")
            try:
                with open(os.path.join(dir, filed), "rb") as file:
                    data = file.read(1024)
                    while data:
                        clientSocket.send(data)
                        print(data)
                        data = file.read(1024)
                    file.close()
            except FileNotFoundError:
                print('File not found')
            except Exception as e:
                print(f'Error during file upload: {e}')

            # Receive and print the server's response
            res = clientSocket.recv(1024).decode()
            print('From server:', res)
        
        elif command == 'download':
            res = clientSocket.recv(1024).decode()
            res = json.loads(res)
            print(res)

            ## enter filename that want to download
            file_name = input("Enter file name : ")
            clientSocket.send(file_name.encode())

            ##check status
            res = clientSocket.recv(1024).decode()
            res = json.loads(res)

            if(res['code'] == 404):
                print(res['msg'])
            else:
                with open(os.path.join(dir, file_name), 'wb') as file:
                    data = clientSocket.recv(1024)
                    file.write(data)
                
                res = clientSocket.recv(1024).decode()
                res = json.loads(res)
                print(res)
        elif command == 'end':
            clientSocket.close()
            break
    except Exception as e:
        print(f'Error in connection: {e}')
        break