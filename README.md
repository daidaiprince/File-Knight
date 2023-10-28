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
PyUSB模組


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

# 使用者自訂伺服器端金鑰為python    
  global string
  string = 'python'

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
# 使用者自訂用戶端金鑰為python
  string= 'python'
  secretKey = base64. b32encode ( string. encode ( encoding= "utf-8" ))
# 產生二維條碼圖檔
  url = pyotp.totp.TOTP(secretKey).provisioning_uri   ( "python@python.test.org" ,issuer_name= 'python' )
  img = qrcode.make ( url )
  print( url )
  with open ( 'qrcode.png' , 'wb' ) as f:
      img.save ( f )
```

***

 FingerPrint模組
 
這是筆記型本電腦上指紋辨識器的驅動程式（LG Gram 2018）。該腳本也可以在其他筆記型電腦，甚至帶有指紋辨識器的個人電腦上運行。
使用 Windows Biometric Framework API 與指紋辨識器進行互動。從技術上講，可以使用 API 存取任何 WBF 設備，包括臉部識別和虹膜識別。

模組來源：https://github.com/luspock/FingerPrint

安裝指令：使用FingerPrint 類別

使用範例：
```
# 匯入指紋辨識模組
  from fingerprint import FingerPrint
  global myFP

# 建立myFP物件類別
  myFP = FingerPrint()
  
# 打開設備
  myFP.open()
   # 進行指紋比對
if myFP.verify():
        messagebox.showinfo('資訊', '指紋比對成功!')
    else:
        messagebox.showerror('資訊', '指紋比對失敗!')
# 關閉設備
  myFP.close()
```
***
Fernet模組

Fernet 透過以下方式克服了開發人員在設計系統時可能犯的錯誤：
*	提供用於產生密鑰的安全機制（密鑰類似於密碼）。
*	選擇安全加密算法（AES 使用 CBS 模式和 PKCS7 填充）。
*	隨機分配一個安全的“salt”值使加密更加安全。
*	時間戳加密的訊息。
*	對消息進行簽名（使用 HMAC 和 SHA256）以檢測任何更改它的嘗試。

模組來源：https://github.com/pyca/cryptography

安裝指令：```pip install cryptography```
```
使用範例：
# 匯入檔案加解密模組
  from cryptography.hazmat.backends import default_backend
  from cryptography.hazmat.primitives import hashes
  from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
  from cryptography.fernet import Fernet
  from cryptography.fernet import InvalidToken
  from cryptography import *
  import cryptography
  global token

  password = ‘www.utaipei.edu.tw’
  salt = b'salt_'
  kdf = PBKDF2HMAC(algorithm=(hashes.SHA256()),
       length=32, salt=salt, iterations=100000,
       backend=(default_backend()))
       key = base64.urlsafe_b64encode(kdf.derive(password))

# 將檔案test.txt以二進制方式讀取  
file = open(‘test.txt’, 'rb')
  data = file.read()
  file.close()
  token = Fernet(key)

# 將檔案test.txt加密
  encrypted = token.encrypt(data)
  
# 將加密資料寫入至檔案encrypt.txt中 
  file = open(‘encrypt.txt’, 'wb')
  file.write(encrypted)
  file.close()
  
# 將檔案encrypt.txt以二進制方式讀取
  file = open(‘encrypt.txt’, 'rb')
  data = file.read()
  file.close()
  token = Fernet(key)
  
# 將檔案encrypt.txt解密
  decrypted = token.decrypt(data)

# 將解密資料寫入至檔案decrypt.txt中
  file = open(‘decrypt.txt’, 'wb')
  file.write(decrypted)
  file.close()
```
***
Steganography模組

隱藏方法：

為該項目開發的一種方法稱為Shuffle方法，它包括以隨機順序對位元進行混淆，產生一個檔案（密鑰），這是檢索隱藏訊息必需的，沒有它就無法檢索。

隨機播放方法：

隨機播放方法包括在隱藏訊息之前以隨機順序隨機播放位元組的位元。順序保存在一個包含 8 個不相關元素的列表（稱為索引/鍵列表）中，每個元素的索引是指要更改的位置位元，值是目標索引。例如，在第一個元素（位置0）是2，第二個（位置1）是6等的列表中，意味著位置0的位元將轉到位置2，位置1的位元將轉到位置6...下面是一個索引列表的示例，以及使用該列表對位元組進行混淆時會發生什麼。

![隨機播放方法](https://github.com/daidaiprince/image-database/blob/main/steg1.png?raw=true )

![隨機播放方法](https://github.com/daidaiprince/image-database/blob/main/steg2.png?raw=true )


使用此方法檢索訊息時，必須提供列表以獲取正確的資料，否則無法獲取。該列表總組合共有8！個，等於40,320。但這種方法不是只使用1個列表，而是實際使用10個列表，將組合數提高到8!10等於1.1355473e+46。
它使用了10個列表，只是為了使暴力破解成為不可能的事。它使用位元組索引的最後一位元組來知道使用哪個列表來打亂該位元組，例如，位元組#6543將使用列表#3打亂，位元組#6544使用列表#4等等。
任何視訊檔案都可以作為輸入，但輸出必須是avi，這是一個支持原始視訊的容器。需要使用FFmpeg將音訊流從原始視訊檔案複製到載體檔案。


模組來源：https://github.com/rafaeloliveira00/Steganography

安裝指令：使用hide和retrieve 函數

```
使用範例：
# 匯入影片隱藏還原檔案模組
  import bytes_manipulation as bm
  import video
  import message
  import utils
  import sys
  import cv2

# 指定隱藏的檔案(str1)、載體MP4(str2)和載體AVI(str3)
str1='c:\1.doc '
str2='c:\2.mp4 '
str3='c:\3.avi '       

#將檔案隱藏於MP4影片中
hide(str2, str3, str1, will_shuffle=True, dict_index=None)
#從AVI影片中還原檔案
 retrieve('c:\3.avi ', 'c:\Keys ')
```

## 系統封裝
本文開發之檔案保護系統，只能在開發環境內使用，為了讓沒有安裝Python電腦也能夠使用本系統，必須將Python程式封裝成獨立執行檔案，使用的是auto-py-to-exe，它是圖形化介面封裝工具，相關功能透過滑鼠點選完成，無須記憶指令。


模組名稱：auto-py-to-exe


模組來源：https://github.com/brentvollebregt/auto-py-to-exe

安裝指令：```pip install auto-py-to-exe```




使用前必須完成以下條件：

* 安裝Google Chrome瀏覽器，其為執行圖形介面底層框架。

* 下載UPX壓縮檔並將其解壓縮，其為EXE資源壓縮工具 。




本系統的封裝步驟說明：

1.腳本位置按瀏覽鈕選擇要封裝成EXE檔的py檔。

2.點選單檔案。

3.點選基於視窗(隱藏控制台)。
 
4.按瀏覽鈕選擇執行檔呈現的圖示。
 
5.將程式使用到的資源檔(圖像、聲音)一併以新增檔案附加。
 
6.按瀏覽檔案夾鈕選擇UPX程式所在位置。
 
7.按將.PY轉換為.EXE鈕，等候產生EXE檔案。

8.按打開輸出目錄鈕。
 
9.此處的EXE檔案可以拿到未安裝Python的電腦上使用。


## 系統功能


![身分認證階段操作](https://github.com/daidaiprince/image-database/blob/main/SystemFunc1.png?raw=true "身分認證階段操作")

![資料保護階段操作](https://github.com/daidaiprince/image-database/blob/main/SystemFunc2.png?raw=true "資料保護階段操作")



## 展示系統
檔案名稱為，移除指紋辨識和USB鎖功能，可掃描以下二維條碼檔案，以取得OTP驗證碼測試。

![OTP二維條碼](https://github.com/daidaiprince/image-database/blob/main/qrcode.png?raw=true "OTP二維條碼")


