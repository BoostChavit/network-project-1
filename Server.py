from socket import *
import os
import json

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
                res = json.dumps({"code":200, "msg":'ok', "data":str(file_list)})
                print(res)
                connection_socket.send(res.encode())
            elif command == 'upload':
                file_name = connection_socket.recv(1024).decode()
                print('File name to be save :', file_name)
                file_path = os.path.join(getDirectory(), file_name)

                with open(file_path, 'wb') as file:
                    data = connection_socket.recv(1024)
                    file.write(data)
                
                res = json.dumps({"code":200, "msg":'ok', "data":f'File "{file_name}" received and saved successfully.'})
                print(res)
                connection_socket.send(res.encode())
            elif command == 'download':
                file_list = os.listdir(getDirectory())
                res = json.dumps({"code":200, "msg":'ok', "data":str(file_list)})
                print(res)
                connection_socket.send(res.encode())
                
                filed = connection_socket.recv(1024).decode()
                res = json.dumps({"code":200, "msg":'ok'})
                connection_socket.send(res.encode())
                
                try:
                    with open(os.path.join(getDirectory(), filed), "rb") as file:
                        data = file.read(1024)
                        while data:
                            connection_socket.send(data)
                            data = file.read(1024)
                        file.close()


                except FileNotFoundError:
                    str = 'File not found!'
                    res = json.dumps({"code":200, "msg":str})
                    connection_socket.send(res.encode())
                except Exception as e:
                    str = 'Error while uploading file!'
                    res = json.dumps({"code":200, "msg":str})
                    connection_socket.send(res.encode())
                
                connection_socket.send(res.encode())
            elif command == 'end':
                break

        connection_socket.close()
    except Exception as e:
        print(f'Error in connection: {e}')
