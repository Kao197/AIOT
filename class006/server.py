# pc執行
#########################匯入模組#########################
import socket

#########################函式與類別定義#########################
HOST = "localhost"  # IP
PORT = 55555  # port, 可自行更改但需要與客戶端相同
server_socket = socket.socket()  # 建立socket
server_socket.bind((HOST, PORT))  # 綁定IP與port
server_socket.listen(5)  # 最大連接數量, 超過則拒絕連接
print(f"server:{HOST}, port:{PORT} start")  # 顯示伺服器IP和port
client, addr = server_socket.accept()  # 接受客戶端連接, 返回客戶端socket和地址
print(f"client address: {addr[0]} port: {addr[1]} connected")  # 顯示客戶端IP和port
#########################宣告與設定#########################

#########################主程式#########################
while True:
    msg = client.recv(1024).decode("utf8")
    # 接收來自客戶端的訊息, 最大1024位元組, 並解碼為utf8字串
    print(f"client message: {msg}")  # 顯示來自客戶端的訊息
    reply = ""  # 建立伺服器回應字串

    if msg == "hi":
        reply = "hello"  # 將字串轉換為位元組, 因為socket傳輸的是位元組
        client.send(reply.encode("utf8"))  # 發送回應給客戶端
    elif msg == "bye":
        client.send(b"quit")  # 這個=client.send(reply.encode("utf8"))
        break
    else:
        client.send(b"what?")  # 這個=client.send(reply.encode("utf8"))
client.close()  # 關閉客戶端連接
server_socket.close()  # 關閉伺服器socket
