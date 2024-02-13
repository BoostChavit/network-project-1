from socket import *
import os

def getDirectory():
    cur = os.getcwd()
    path = os.path.join(cur, 'files')
    return path

if(os.path.isdir('files')):
    print('Directory created!')
else:
    try:
        path = getDirectory()
        os.mkdir(path)
        print('Create directory successfully!')
    except:
        print('Fail to create directory!')

serverPort = '127.0.0.1'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverPort, 12000))
serverSocket.listen(1)

print('The server is ready')

while True:
    try:
        connection_socket, addr = serverSocket.accept()

        while True:
            command = connection_socket.recv(1024).decode()
            print(command)

            if command == 'ls':
                file_list = os.listdir(getDirectory())
                connection_socket.send(str(file_list).encode())
            elif command == 'upload':
                file_name = connection_socket.recv(1024).decode()
                print(file_name)
                file_path = os.path.join(getDirectory(), file_name)
                print(file_path)

                with open(file_path, 'wb') as file:
                    data = connection_socket.recv(1024)
                    file.write(data)
                
                res = f'File "{file_name}" received and saved successfully.'
                print(res)
                connection_socket.send(res.encode())
            elif command == 'download':
                file_list = os.listdir(getDirectory())
                connection_socket.send(str(file_list).encode())
                try:
                    filed = connection_socket.recv(1024).decode()
                    with open(os.path.join(getDirectory(), filed), "rb") as file:
                        data = file.read(1024)
                        connection_socket.send('200'.encode())
                        while data:
                            connection_socket.send(data)
                            data = file.read(1024)
                        file.close()
                    res = connection_socket.recv(1024).decode()
                    print(res)

                except FileNotFoundError:
                    str = 'File not found!'
                    connection_socket.send('404'.encode())
                    connection_socket.send(str.encode())
                except Exception as e:
                    str = 'Error while uploading file!'
                    connection_socket.send('404'.encode())
                    connection_socket.send(str.encode())
            elif command == 'end':
                break

        connection_socket.close()
    except Exception as e:
        print(f'Error in connection: {e}')
