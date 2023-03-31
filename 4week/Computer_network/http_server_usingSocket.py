import os
import socket

HOST = ''
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Start server')
    while True:
        try:
            conn, addr = s.accept() # cilent는 accept()를 통해서 대기하게 됩니다.
            with conn:
                print(f'Connected by {addr}')
                data = conn.recv(1500) # 요청을 받으면 data를 받게됩니다.
                ptr = data.find('\r\n'.encode('utf-8')) # '/r/n'으로 줄바꿈되는 첫번째 지점의 인덱스를 반환해주고
                header = data[:ptr] # 위에서 반환한 index로 header와 left로 나눕니다.
                left = data[ptr:]
                request = header.decode('utf-8') # header가 byte형이므로 decode를 하여 변환을 시켜주는 과정입니다.
                method, path, protocol = request.split(' ') # 공백을 기준으로 method, path, protocol 에 각각 저장합니다.
                print(f'Received: {method} {path} {protocol}')
                if not data: # data가 비어있으면 종료합니다.
                    break
                if path == '/': # 만약 path가 '/'이면 index.html을 호출합니다. default = index.html
                    path = '/index.html'

                path = f'.{path}'

                # 위에서 받은 path가 mystyle.css 일 때, path를 외부폴더의 경로로 설정해주어서
                # 올바른 위치로 찾아가게 하였습니다.
                # 아래의 js 파일의 path도 동일하게 작성하였습니다.
                if path == './mystyle.css':
                    path = './css/mystyle.css'

                if path == './myscript.js':
                    path = './js/myscript.js'

                # path를 발견하지 못했을떄 404 not found가 나타나는 notfound.html로 path를 설정해줍니다.
                if not os.path.exists(path):
                    path = './notfound.html'

                # 반복되는 조건문
                # 아래의 path 조건에 따라 조건문들을 작성해주어서 html,css,js,image 파일들을 여는 방식과 encoding 방식을 설정해주었습니다.
                # 그리고 다시 서버에 보낼 header의 상태와 Content-Type을 파일마다 다르게 설정해주어야 했기 때문에 조건문을 반복해서 사용했습니다.

                if path == './201602037.html':
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
                    with open(path, 'r', encoding='UTF-8') as f:
                        body = f.read()
                        body = body.encode('utf-8')

                if path == './index.html':
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
                    with open(path, 'r', encoding='UTF-8') as f:
                        body = f.read()
                        body = body.encode('utf-8')

                if path == './css/mystyle.css':
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Content-Type: text/css;charset=utf-8\r\n'
                    with open(path, 'r', encoding='UTF-8') as f:
                        body = f.read()
                        body = body.encode('utf-8')

                if path == './js/myscript.js':
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Content-Type: text/javascript;charset=utf-8\r\n'
                    with open(path, 'r', encoding='UTF-8') as f:
                        body = f.read()
                        body = body.encode('utf-8')

                # 위 3 파일과 다른 점이 있었던 image파일이였습니다.
                # 파일을 str 타입으로 여는것과 다르게 이미지파일은 byte로 이루어져 있기 때문에 encoding 과정과 byte 형식으로 파일을
                # 열어주어야 하기 때문에 'rb'로 파일을 열어주고 encoding을 삭제하였습니다. 마찬가지고 body 부분에서도 파일 f를 읽고
                # utf-8 형식으로 encode 하는 과정을 뺐습니다.
                if path == './myimage.jpg':
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Content-Type: image/jpeg;charset=utf-8\r\n'
                    with open(path, 'rb') as f:
                        body = f.read()

                if path == './notfound.html':
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
                    with open(path, 'r', encoding='UTF-8') as f:
                        body = f.read()
                        body = body.encode('utf-8')

                header = f'{header}Server: Our server\r\n'
                header = f'{header}Connection: close\r\n'
                header = f'{header}Content-Length: {len(body)}\r\n'
                header = f'{header}\r\n'
                header = header.encode('utf-8')
                response = header + body  # 위에서 작성된 header와 body를 더해주어서 변수에 저장하고 보내줍니다.
                conn.sendall(response)

        except KeyboardInterrupt:
            print('Shutdown server')
            break
