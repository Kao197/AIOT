#########################匯入模組#########################
import network
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
wi = mcu.wifi()  # 宣告 WIFI 物件
wi.setup(ap_active=False, sta_active=True)  # 設定 WIFI 模組為 STA 模式
# 搜尋WIFI
wi.scan()
# 選擇要連接的WIFI
if wi.connect("Singular_AI", "Singular#1234"):
    print(f"ip={wi.ip}")
#########################主程式#########################
