# 檔案騎士

**工具用途 : 檔案資料保護**


![檔案騎士](https://github.com/daidaiprince/image-database/blob/main/FileKnight.png?raw=true "檔案騎士")

####




## 開發緣由
研究所期間，對於學校老師上課提到的資訊安全感到十分新奇，進而產生開發工具的想法，同時也是我撰寫論文所設計的檔案保護系統。




## 系統架構


![系統架構](https://github.com/daidaiprince/image-database/blob/main/SystemStructure.png?raw=true "系統架構")


## 系統流程
**登入系統認證流程**

![登入系統認證](https://github.com/daidaiprince/image-database/blob/main/FlowChart.png?raw=true "登入系統認證")

**執行檔案保護流程**

![執行檔案保護](https://github.com/daidaiprince/image-database/blob/main/FlowChart2.png?raw=true "執行檔案保護")


## 使用模組
++PyUSB模組++


PyUSB 主要在 Linux 和 Windows 上開發和測試，但可以在任何運行 Python >= 3.7、ctypes 和至少一個內置後端的平台上正常工作。
PyUSB 支持libusb 1.0、libusb 0.1 和 OpenUSB。其中，libusb 1.0 目前推薦適用於大多數案例。
在 Linux 和 BSD 上，這些通常可以在發行版的官方存儲庫中獲得。

模組來源：https://github.com/pyusb/pyusb

安裝指令：```pip install pyusb```

使用範例：
```
# 匯入USB識別模組
  import usb.core
  import usb.util
  import sys

# 找尋所有的USB裝置
  all_devs = usb.core.find(find_all=True)

  for d in all_devs:
   # 如果找到符合VID及PID的USB裝置，則列印該裝置明細
     if (d.idVendor == vid) & (d.idProduct == pid):
       print(d)
```
***
PyOTP模組

*	OTP涉及共享密鑰，儲存在手機和伺服器上

*	可以在沒有網際網路連接的手機上產生OTP

*	OTP 應始終用作身份認證的第二個因子（如果手機遺失，帳戶仍受密碼保護）

*	Google Authenticator和其他OTP客戶端應用程式允許儲存多個OTP機密並使用QR碼提供這些機密

模組來源：https://github.com/pyauth/pyotp

安裝指令：```pip install pyotp```

使用範例：
```
#==============
# 伺服器端
#==============
# 匯入OTP模組
  import base64
  import pyotp

# 使用者自訂伺服器端金鑰為M10716012    
  global string
  string = 'M10716012'

# 產生TOTP碼
  global secretKey
  secretKey = base64.b32encode(string.encode(encoding='utf-8'))
  global totp  
  totp=pyotp.TOTP(secretKey)

# 輸入即時TOTP碼
  global code   
  code = pwd.get()

# 如果與系統的即時TOTP碼相符
  if totp.verify(code) == 1 :
    messagebox.showinfo('資訊', '密碼驗證正確!')
  else:
    messagebox.showerror('資訊', '請重新輸入密碼!')
#==============
# 用戶端
#==============
# 匯入OTP模組和QRCODE模組
  import pyotp
  import qrcode
  import base64
# 使用者自訂用戶端金鑰為M10716012
  string= 'M10716012'
  secretKey = base64. b32encode ( string. encode ( encoding= "utf-8" ))
# 產生二維條碼圖檔
  url = pyotp.totp.TOTP(secretKey).provisioning_uri   ( "M10716012@utaipei.edu.tw" ,issuer_name= 'M10716012' )
  img = qrcode.make ( url )
  print( url )
  with open ( 'M10716012.png' , 'wb' ) as f:
      img.save ( f )
```
執行用戶端程式後，產生的二維條碼檔案如圖3-2所示。
圖3-2 OTP二維條碼
 

