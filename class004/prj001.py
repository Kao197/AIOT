#########################匯入模組#########################
import network 
#########################函式與類別定義#########################

#########################宣告與設定#########################
wlan = network.WLAN(network.STA_IF) #建立WLAN物件，設定為站台模式
ap = network.WLAN(network.AP_IF) #建立WLAN物件，設定為基地台模式
ap.active(False) #關閉 AP 模式
wlan.active(True) #啟用 STA 模式
#搜尋 WIFI
wifi_list = wlan.scan()
print("Scan result:")
for i in range(len(wifi_list)):
    print(wifi_list[i])
#選擇要連接的 WIFI

wlSSID = "Singular_AI"
wlPWD = "Singular#1234"
wlan.connect(wlSSID, wlPWD) #連接 WIFI
while not (wlan.isconnected()):
    pass#卡在空的while裡用的
print("connect successfully", wlan.ifconfig())
while True:
    pass
#########################主程式#########################