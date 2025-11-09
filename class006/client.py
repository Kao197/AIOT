# PC執行
#########################匯入模組#########################
import socket

#########################函式與類別定義#########################
client_socket = socket.socket()  # 建立socket
client_socket.connect(("127.0.0.1", 55555))  # 連接伺服器IP與port
#########################宣告與設定#########################
while True:
    msg = input("Imput Message: ")  # 從使用者取得輸入訊息
    client_socket.send(msg.encode("utf8"))  # 發送訊息給伺服器, 並編碼為utf8位元組
    reply = client_socket.recv(1024).decode("utf8")
    # 接收來自伺服器的回應, 最大1024位元組, 並解碼為utf8字串
    if reply == "quit":  # 顯示來自伺服器的回應
        print("Disconnected")
        client_socket.close()  # 關閉socket連接
        break
    print(reply)

#########################主程式#########################
