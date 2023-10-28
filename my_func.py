"""=================
    功能:檔案保護
    作者:吳彥楓
    日期:2023/10/26
   ================="""


""" 匯入系統模組 """
import os,sys,time
from os import path

""" 匯入遊戲模組 """
import pygame

""" 匯入GUI模組 """
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

""" 匯入指紋辨識模組 """
from fingerprint import FingerPrint
global myFP
global fingermsg
global fingertxt
myFP = FingerPrint()

""" 匯入OTP模組 """
import base64
import pyotp

""" 匯入檔案崁入影片模組 """
import bytes_manipulation as bm
import video
import message
import utils
import cv2
# raw video (no codec)
VIDEO_CODEC = 'RGBA'

""" 匯入Fernet加解密模組 """
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography import *
import cryptography
global token

""" 匯入USB模組 """
import usb.core
import usb.util



""" PyInstaller 打包 GUI 執行檔需要之程式碼 """
def resource_path(relative_path):
    """ 取得資源的絕對路徑，使用於 PyInstaller """
    try:
        # PyInstaller 建立一個暫存資料夾和儲存路徑在_MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


""" 播放 MP3 檔案 """
def play_mp3(x):
    pygame.init()
    pygame.mixer.init()
    file=resource_path(x)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()


""" 顯示軟體LOGO視窗 """
def splash_logo():
    global splash_root
    
    # 建立LOGO視窗
    splash_root = Tk()

    # 移除標題列
    splash_root.overrideredirect(True)

    # 設定軟體LOGO視窗大小
    splash_width = 526
    splash_height = 268

    # 設定指紋辨識視窗位於螢幕中心
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x = screen_width / 2 - splash_width / 2
    y = screen_height / 2 - splash_height / 2
    splash_root.geometry(f"{splash_width}x{splash_height}+{int(x)}+{int(y)}")

    # 去除背景顏色
    splash_root.attributes('-transparentcolor', '#ff80c0')

    # 顯示圖片-splash_logo.png
    logo = PhotoImage(file=(resource_path('./image/splash_logo.png')))
    Label(splash_root, image=logo).pack()
    
    # 播放音樂-logo.mp3
    play_mp3("./sound/logo.mp3")

    # 持續7秒後結束軟體LOGO視窗
    splash_root.after(7000,splash_root.destroy)

    # 視窗繼續執行，同時進入等待與處理視窗事件
    splash_root.mainloop()


""" 設定滑鼠可移動視窗 """
def move_main_window(event):
    main_root.geometry(f'+{event.x_root}+{event.y_root}')
def move_fingerprint_window(event):
    fingerprint_root.geometry(f'+{event.x_root}+{event.y_root}')
def move_otp_window(event):
    otp_root.geometry(f'+{event.x_root}+{event.y_root}')
    
    
""" 執行指紋的驗證 """
def fingerprint_verify():
  myFP.open()
  if myFP.verify():
      print("指紋辨識成功")
      messagebox.showinfo('資訊', '系統指紋比對成功。')
      myFP.close()
      fingerprint_root.destroy()
  else:
      print("指紋辨識失敗")
      messagebox.showerror('錯誤', '系統指紋比對失敗，請重新啟動程式。')
      os._exit(0)
        
        
""" 顯示指紋辨識視窗 """
def fingerprint_detect():
    global fingerprint_root

    # 建立指紋辨識視窗
    fingerprint_root = Tk()

    # 移除標題列
    fingerprint_root.overrideredirect(True)

    # 設定指紋辨識視窗大小
    login_width = 334
    login_height = 581

    # 設定指紋辨識視窗不能調整大小
    fingerprint_root.resizable(0, 0)

    # 設定指紋辨識視窗位於螢幕中心
    screen_width = fingerprint_root.winfo_screenwidth()
    screen_height = fingerprint_root.winfo_screenheight()
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    fingerprint_root.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    # 設定滑鼠能夠拖移圖片視窗
    fingerprint_root.bind("<B1-Motion>", move_fingerprint_window)

    # 顯示圖片-mobile.png
    logo = PhotoImage(file=resource_path('./image/mobile.png'))
    Label(fingerprint_root,image=logo).pack()
    
    # 去除背景顏色
    fingerprint_root.attributes('-transparentcolor','#C0C0C0') 

    # 顯示圖片-info.png
    info = PhotoImage(file=resource_path('./image/info.png'))
    lab1=Label(fingerprint_root,image=info,width=250,height=300)
    lab1.place(x=40,y=75)
  
    # 顯示圖片-fingerprint3.png
    finger = PhotoImage(file=resource_path('./image/fingerprint3.png'))
    lab1=Label(fingerprint_root,image=finger,width=120,height=150,bg='#1a1e36')
    lab1.place(x=100,y=150)

    # 顯示文字-請將手指指紋置於感測器上
    fingermsg = Label(fingerprint_root,text="請將手指指紋置於感測器上",bg='#1a1e36',fg='white')
    fingermsg.place(x=100,y=290)
    fingertxt = Label(fingerprint_root,text="",bg='#1a1e36',fg='white',font=("Arial", 15))
    fingertxt.place(x=100,y=335)

    # 顯示按鈕-比對指紋
    btn1=Button(fingerprint_root,text="比對指紋",compound=LEFT,font=("Arial", 15),cursor="mouse",command=fingerprint_verify)
    btn1.place(x=50,y=420)

    # 顯示按鈕-離開系統
    btn2=Button(fingerprint_root,text="離開系統",compound=LEFT,font=("Arial", 15),cursor="mouse",command=fingerprint_close)
    btn2.place(x=180,y=420)

    # 視窗繼續執行，同時進入等待與處理視窗事件
    fingerprint_root.mainloop()


""" 關閉指紋辨識視窗並結束程式 """
def fingerprint_close():
    fingerprint_root.destroy()
    os._exit(0)

 
""" 顯示OTP密碼驗證視窗 """
def otp_detect():
    global otp_root

    # 建立OTP密碼驗證視窗
    otp_root = Tk()
    
    # 移除標題列
    otp_root.overrideredirect(True)

    # 設定OTP密碼驗證視窗大小
    login_width = 334
    login_height = 581
    
    # 設定登入視窗不能調整大小
    otp_root.resizable(0, 0)
    
    # 設定登入視窗位於螢幕中心
    screen_width = otp_root.winfo_screenwidth()
    screen_height = otp_root.winfo_screenheight()
    x = (screen_width / 2) - (login_width / 2)
    y = (screen_height / 2) - (login_height / 2)
    otp_root.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

    # 設定滑鼠能夠拖移圖片視窗
    otp_root.bind("<B1-Motion>", move_otp_window)

    # 顯示圖片-mobile.png
    logo = PhotoImage(file=resource_path('./image/mobile.png'))
    Label(otp_root,image=logo).pack()

    # 去除背景顏色
    otp_root.attributes('-transparentcolor','#C0C0C0') 

    # 顯示圖片-info.png
    info = PhotoImage(file=resource_path('./image/info.png'))
    lab1=Label(otp_root,image=info,width=250,height=300)
    lab1.place(x=40,y=75)
    
    global pwd

    # 顯示密碼輸入框
    pwd=Entry(otp_root,font=20,width=20,fg='red', justify=CENTER)
    pwd.place(x=75,y=256)

    # 顯示文字-輸入OTP即時密碼
    otp=Label(otp_root,text='輸入OTP即時密碼',compound=LEFT,font=("Arial", 15),height=2,bg='#1a1e36',fg='white')
    otp.place(x=85,y=190)

    # 顯示按鈕-比對密碼
    btn1=Button(otp_root,text="比對密碼",compound=LEFT,font=("Arial", 15),cursor="mouse",command=otp_verify)
    btn1.place(x=50,y=420)

    # 顯示按鈕-離開系統
    btn2=Button(otp_root,text="離開系統",compound=LEFT,font=("Arial", 15),cursor="mouse",command=otp_root_close)
    btn2.place(x=180,y=420)
    
    # 產生TOTP碼    
    global string
    string = 'python'
    global secretKey
    secretKey = base64.b32encode(string.encode(encoding='utf-8'))

    # 視窗繼續執行，同時進入等待與處理視窗事件
    otp_root.mainloop()


""" 關閉OTP驗證視窗並結束程式 """
def otp_root_close():
    otp_root.destroy()
    os._exit(0)

 
""" 執行OTP的驗證 """
def otp_verify():
    global totp  

    # 取得之前產生的TOTP碼
    totp=pyotp.TOTP(secretKey)

    # 取得之前輸入的OTP驗證碼
    global code   
    code = pwd.get()
    print(code)

    while True:
        # 如果OTP驗證碼正確
        if totp.verify(code) == 1 :
            messagebox.showinfo('資訊', '密碼驗證正確，點擊進入主選單。')
            otp_root.destroy()
            break
        else:
            messagebox.showerror('錯誤', '密碼輸入錯誤，請重新啟動程式。')
            os._exit(0)
            
     
""" 顯示主視窗 """
def main_show():
    global main_root

    # 建立主視窗
    main_root = Tk()

    # 移除標題列
    main_root.overrideredirect(True)
    main_root.title("檔案騎士")
    main_root.focus_force()

    # 設定主視窗大小
    main_width = 1137
    main_height = 822

    # 設定主視窗不能調整大小
    main_root.resizable(0, 0)

    # 設定主視窗位於螢幕中心
    screen_width = main_root.winfo_screenwidth()
    screen_height = main_root.winfo_screenheight()
    x = (screen_width / 2) - (main_width / 2)
    y = (screen_height / 2) - (main_height / 2)
    main_root.geometry(f'{main_width}x{main_height}+{int(x)}+{int(y)}')

    # 顯示圖片-laptop.png
    logo = PhotoImage(file=resource_path('./image/laptop.png'))
    Label(main_root,image=logo).pack()
    
    # 去除背景顏色
    main_root.attributes('-transparentcolor','#ff0000') 

    global var
    var = StringVar()
    global rb1,rb2,rb3,rb4,next_btn,exit_btn

    # 顯示選項-目標檔案加密
    rb1 = Radiobutton(main_root,text = "目標檔案加密",variable = var,value = '1',font = "微軟正黑體 40 bold",fg='gold',bg='#0080ff',activebackground='#0080ff',activeforeground='#0080ff')
    rb1.configure(height = 1, width = 10)
    rb1.place(x=370,y=70)
        
    # 顯示選項-目標檔案解密
    rb2 = Radiobutton(main_root,text = "目標檔案解密",variable = var,value = '2',font = "微軟正黑體 40 bold",fg='gold',bg='#0080ff',activebackground='#0080ff',activeforeground='#0080ff')
    rb2.configure(height = 1, width = 10)
    rb2.place(x=370,y=150)
    
    # 顯示選項-檔案藏入影片
    rb3 = Radiobutton(main_root,text = "檔案藏入影片",variable = var,value = '3',font = "微軟正黑體 40 bold",fg='gold',bg='#0080ff',activebackground='#0080ff',activeforeground='#0080ff')
    rb3.configure(height = 1, width = 10)
    rb3.place(x=370,y=230)

    # 顯示選項-影片還原檔案
    rb4 = Radiobutton(main_root,text = "影片還原檔案",variable = var,value = '4',font = "微軟正黑體 40 bold",fg='gold',bg='#0080ff',activebackground='#0080ff',activeforeground='#0080ff')
    rb4.configure(height = 1, width = 10)
    rb4.place(x=370,y=310)

    # 顯示按鈕-下一步
    next_btn = Button(main_root, text='下一步', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=selectitem)
    next_btn.place(x=410, y=440)

    # 顯示按鈕-離開系統
    exit_btn = Button(main_root, text='離開系統', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=(main_root.destroy))
    exit_btn.place(x=610, y=440)

    # 隱藏標題列(視窗能拖曳移動)
    title_bar1 = Label(main_root, text='', bg='#1a1a1a')
    title_bar1.place(x=125, y=15, width=480, height=15)
    title_bar1.bind('<B1-Motion>', move_main_window)
    title_bar2 = Label(main_root, text='', bg='#1a1a1a')
    title_bar2.place(x=525, y=15, width=480, height=15)
    title_bar2.bind('<B1-Motion>', move_main_window)

    # 視窗繼續執行，同時進入等待與處理視窗事件
    main_root.mainloop()


"""清除 輸入框-請輸入自行定義的檔案密碼 內容"""
def e3_click(event):
    e3.delete(0, END)


"""清除 輸入框-請輸入自行定義的檔案密碼 內容"""
def e6_click(event):
    e6.delete(0, END)


"""清除 輸入框-請按左邊按鈕儲存產生的載體影片 內容"""
def e9_click(event):
    e9.delete(0, END)


"""清除 輸入框-請按左邊按鈕選擇載體影片 內容"""
def e10_click(event):
    e10.delete(0, END)    


""" 主畫面選擇進入子項目畫面 """
def selectitem():
    global e1,e2,e3,select,select_btn,save,save_btn,pwd,pwd_btn,enc_btn,back_btn
    global e4,e5,e6,dec_btn
    global e7,e8,e9,select1,select2,select1_btn,select2_btn,avi,avi_btn,ebd_btn
    global e10,select3,select3_btn,ext_btn,text 

    # 如果沒選擇就不動作
    if var.get()=='':return

    # 如果選擇1，則執行
    if var.get()=='1':

        # 隱藏選項-目標檔案加密
        rb1.place_forget()

        # 隱藏選項-目標檔案解密
        rb2.place_forget()

        # 隱藏選項-檔案藏入影片
        rb3.place_forget()

        # 隱藏選項-影片還原檔案
        rb4.place_forget()

        # 隱藏按鈕-下一步
        next_btn.place_forget()

        # 隱藏按鈕-離開系統
        exit_btn.place_forget()

        # 顯示輸入框-請按左邊按鈕選擇要加密的檔案        
        e1 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e1.insert(0, "請按左邊按鈕選擇要加密的檔案")
        e1.place(x=255, y=100, width=670, height=64)

        # 顯示圖片按鈕-open.png
        select = PhotoImage(file=(resource_path('./image/open.png')))
        select_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=select, command=select_encrypt_file)
        select_btn.place(x=180, y=100)

        # 顯示輸入框-請按左邊按鈕儲存加密後的檔案
        e2 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e2.insert(0, "請按左邊按鈕儲存加密後的檔案")
        e2.place(x=255, y=200, width=670, height=64)

        # 顯示圖片按鈕-save.png
        save = PhotoImage(file=(resource_path('./image/save.png')))
        save_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=save, command=save_encrypt_file)
        save_btn.place(x=180, y=200)

        # 顯示輸入框-請輸入自行定義的檔案密碼
        e3 = Entry(main_root, font='微軟正黑體 27 bold', bg='white', fg='blue',justify='center')
        e3.insert(0, "請輸入自行定義的檔案密碼")
        e3.place(x=255, y=300, width=670, height=64)
        e3.bind("<1>", e3_click)

        # 顯示圖片按鈕-pwd.png
        pwd = PhotoImage(file=(resource_path('./image/pwd.png')))
        pwd_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=pwd)
        pwd_btn.place(x=180, y=300)

        # 顯示按鈕-檔案加密
        enc_btn = Button(main_root, text='檔案加密', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=run_encrypt)
        enc_btn.place(x=410, y=440)

        # 顯示按鈕-上一步
        back_btn = Button(main_root, text='上一步', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=one_switch_main)
        back_btn.place(x=610, y=440)

    # 如果選擇2，則執行
    if var.get()=='2':
        
        # 隱藏選項-目標檔案加密
        rb1.place_forget()

        # 隱藏選項-目標檔案解密
        rb2.place_forget()

        # 隱藏選項-檔案藏入影片
        rb3.place_forget()

        # 隱藏選項-影片還原檔案
        rb4.place_forget()

        # 隱藏按鈕-下一步
        next_btn.place_forget()

        # 隱藏按鈕-離開系統
        exit_btn.place_forget()

        # 顯示輸入框-請按左邊按鈕選擇要解密的檔案
        e4 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e4.insert(0, "請按左邊按鈕選擇要解密的檔案")
        e4.place(x=255, y=100, width=670, height=64)

        # 顯示圖片按鈕-open.png
        select = PhotoImage(file=(resource_path('./image/open.png')))
        select_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=select, command=select_decrypt_file)
        select_btn.place(x=180, y=100)

        # 顯示輸入框-請按左邊按鈕儲存解密後的檔案
        e5 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e5.insert(0, "請按左邊按鈕儲存解密後的檔案")
        e5.place(x=255, y=200, width=670, height=64)

        # 顯示圖片按鈕-save.png
        save = PhotoImage(file=(resource_path('./image/save.png')))
        save_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=save, command=save_decrypt_file)
        save_btn.place(x=180, y=200)

        # 顯示輸入框-請輸入自行定義的檔案密碼
        e6 = Entry(main_root, font='微軟正黑體 27 bold', bg='white', fg='blue',justify='center')
        e6.insert(0, "請輸入自行定義的檔案密碼")
        e6.place(x=255, y=300, width=670, height=64)
        e6.bind("<1>", e6_click)

        # 顯示圖片按鈕-pwd.png
        pwd = PhotoImage(file=(resource_path('./image/pwd.png')))
        pwd_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=pwd)
        pwd_btn.place(x=180, y=300)

        # 顯示按鈕-檔案解密
        dec_btn = Button(main_root, text='檔案解密', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=run_decrypt)
        dec_btn.place(x=410, y=440)

        # 顯示按鈕-上一步
        back_btn = Button(main_root, text='上一步', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=two_switch_main)
        back_btn.place(x=610, y=440)

    # 如果選擇3，則執行
    if var.get()=='3':
        
        # 隱藏選項-目標檔案加密
        rb1.place_forget()

        # 隱藏選項-目標檔案解密
        rb2.place_forget()

        # 隱藏選項-檔案藏入影片
        rb3.place_forget()

        # 隱藏選項-影片還原檔案
        rb4.place_forget()

        # 隱藏按鈕-下一步
        next_btn.place_forget()

        # 隱藏按鈕-離開系統
        exit_btn.place_forget()
        
        # 顯示輸入框-請按左邊按鈕選擇要隱藏的檔案
        e7 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e7.insert(0, "請按左邊按鈕選擇要隱藏的檔案")
        e7.place(x=255, y=100, width=670, height=64)

        # 顯示圖片按鈕-open.png
        select1 = PhotoImage(file=(resource_path('./image/open.png')))
        select1_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=select1, command=select_embed_file)
        select1_btn.place(x=180, y=100)

        # 顯示輸入框-請按左邊按鈕選擇當載體的影片
        e8 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e8.insert(0, "請按左邊按鈕選擇當載體的影片")
        e8.place(x=255, y=200, width=670, height=64)

        # 顯示圖片按鈕-mp4.png
        select2 = PhotoImage(file=(resource_path('./image/mp4.png')))
        select2_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=select2, command=select_mp4_file)
        select2_btn.place(x=180, y=200)

        # 顯示輸入框-請按左邊按鈕儲存產生的載體影片
        e9 = Entry(main_root, font='微軟正黑體 27 bold', bg='white', fg='blue',justify='center')
        e9.insert(0, "請按左邊按鈕儲存產生的載體影片")
        e9.place(x=255, y=300, width=670, height=64)
        e9.bind("<1>", e9_click)

        # 顯示圖片按鈕-avi.png
        avi = PhotoImage(file=(resource_path('./image/avi.png')))
        avi_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=avi, command=save_avi_file)
        avi_btn.place(x=180, y=300)

        # 顯示按鈕-檔案隱藏
        ebd_btn = Button(main_root, text='檔案隱藏', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=run_embed)
        ebd_btn.place(x=410, y=440)

        # 顯示按鈕-上一步
        back_btn = Button(main_root, text='上一步', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=three_switch_main)
        back_btn.place(x=610, y=440)

    # 如果選擇4，則執行
    if var.get()=='4':
        
        # 隱藏選項-目標檔案加密
        rb1.place_forget()

        # 隱藏選項-目標檔案解密
        rb2.place_forget()

        # 隱藏選項-檔案藏入影片
        rb3.place_forget()

        # 隱藏選項-影片還原檔案
        rb4.place_forget()

        # 隱藏按鈕-下一步
        next_btn.place_forget()

        # 隱藏按鈕-離開系統
        exit_btn.place_forget()
        
        # 顯示輸入框-請按左邊按鈕選擇載體影片
        e10 = Entry(main_root, font='微軟正黑體 27', bg='white', fg='black',justify='center')
        e10.insert(0, "請按左邊按鈕選擇載體影片")
        e10.place(x=255, y=100, width=670, height=64)
        e10.bind("<1>", e10_click)

        # 顯示圖片按鈕-avi.png
        select3 = PhotoImage(file=(resource_path('./image/avi.png')))
        select3_btn = Button(main_root, compound=LEFT, width=64, height=64, cursor='mouse', image=select3, command=select_avi_file)
        select3_btn.place(x=180, y=100)

        # 顯示文字-[ 注意 ] 要從影片還原檔案，須有隱藏檔案到影片時產生的keys，然後與影片放在同一路徑下。還原的檔案會產出在與影片同一路徑下。
        text = Text(main_root,height=6,width=31,font='微軟正黑體 20',fg='white',bg='#0080ff')
        text.insert(END,"[ 注意 ] \n要從影片還原檔案，須有隱藏檔案到影片時產生的keys，然後與影片放在同一路徑下。\n\n還原的檔案會產出在與影片同一路徑下。")
        text.configure(state='disabled')
        text.place(x=320,y=210)

        # 顯示按鈕-還原檔案
        ext_btn = Button(main_root, text='還原檔案', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=run_extract)
        ext_btn.place(x=410, y=440)

        # 顯示按鈕-上一步
        back_btn = Button(main_root, text='上一步', compound=LEFT, width=7,font = "微軟正黑體 20 ", cursor='mouse', command=four_switch_main)
        back_btn.place(x=610, y=440)


""" 切換選項1-目標檔案加密畫面-->主畫面 """
def one_switch_main():

    # 顯示選項-目標檔案加密
    rb1.place(x=370,y=70)

    # 顯示選項-目標檔案解密
    rb2.place(x=370,y=150)

    # 顯示選項-檔案藏入影片
    rb3.place(x=370,y=230)

    # 顯示選項-影片還原檔案
    rb4.place(x=370,y=310)
    
    # 顯示按鈕-下一步
    next_btn = Button(main_root, text='下一步', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=selectitem)
    next_btn.place(x=410, y=440)

    # 顯示按鈕-離開系統
    exit_btn = Button(main_root, text='離開系統', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=(main_root.destroy))
    exit_btn.place(x=610, y=440)

    # 隱藏輸入框-請按左邊按鈕選擇要加密的檔案 
    e1.place_forget()

    # 隱藏輸入框-請按左邊按鈕儲存加密後的檔案
    e2.place_forget()

    # 隱藏輸入框-請輸入自行定義的檔案密碼
    e3.place_forget()

    # 隱藏圖片按鈕-open.png
    select_btn.place_forget()

    # 隱藏圖片按鈕-save.png
    save_btn.place_forget()

    # 隱藏圖片按鈕-pwd.png
    pwd_btn.place_forget()     

    # 隱藏按鈕-檔案加密
    enc_btn.place_forget()

    # 隱藏按鈕-上一步
    back_btn.place_forget()
    
    
""" 切換選項2-目標檔案解密畫面-->主畫面 """
def two_switch_main():
    
    # 顯示選項-目標檔案加密
    rb1.place(x=370,y=70)

    # 顯示選項-目標檔案解密
    rb2.place(x=370,y=150)

    # 顯示選項-檔案藏入影片
    rb3.place(x=370,y=230)

    # 顯示選項-影片還原檔案
    rb4.place(x=370,y=310)
    
    # 顯示按鈕-下一步
    next_btn = Button(main_root, text='下一步', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=selectitem)
    next_btn.place(x=410, y=440)

    # 顯示按鈕-離開系統
    exit_btn = Button(main_root, text='離開系統', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=(main_root.destroy))
    exit_btn.place(x=610, y=440)

    # 隱藏輸入框-請按左邊按鈕選擇要解密的檔案    
    e4.place_forget()

    # 隱藏輸入框-請按左邊按鈕儲存解密後的檔案
    e5.place_forget()

    # 隱藏輸入框-請輸入自行定義的檔案密碼
    e6.place_forget()

    # 隱藏圖片按鈕-open.png
    select_btn.place_forget()

    # 隱藏圖片按鈕-save.png
    save_btn.place_forget()

    # 隱藏圖片按鈕-pwd.png
    pwd_btn.place_forget()     

    # 隱藏按鈕-檔案解密
    dec_btn.place_forget()

    # 隱藏按鈕-上一步
    back_btn.place_forget()     

   
""" 切換選項3-檔案崁入影片-->主畫面 """
def three_switch_main():

    # 顯示選項-目標檔案加密
    rb1.place(x=370,y=70)

    # 顯示選項-目標檔案解密
    rb2.place(x=370,y=150)

    # 顯示選項-檔案藏入影片
    rb3.place(x=370,y=230)

    # 顯示選項-影片還原檔案
    rb4.place(x=370,y=310)
    
    # 顯示按鈕-下一步
    next_btn = Button(main_root, text='下一步', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=selectitem)
    next_btn.place(x=410, y=440)

    # 顯示按鈕-離開系統
    exit_btn = Button(main_root, text='離開系統', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=(main_root.destroy))
    exit_btn.place(x=610, y=440)

    # 隱藏輸入框-請按左邊按鈕選擇要隱藏的檔案
    e7.place_forget()

    # 隱藏輸入框-請按左邊按鈕選擇當載體的影片
    e8.place_forget()

    # 隱藏輸入框-請按左邊按鈕儲存產生的載體影片
    e9.place_forget()

    # 隱藏圖片按鈕-open.png
    select1_btn.place_forget()

    # 隱藏圖片按鈕-mp4.png
    select2_btn.place_forget()

    # 隱藏圖片按鈕-avi.png
    avi_btn.place_forget()

    # 隱藏按鈕-檔案隱藏
    ebd_btn.place_forget()     

    # 隱藏按鈕-上一步
    back_btn.place_forget()     


""" 切換選項4-影片解出檔案-->主畫面 """
def four_switch_main():
    
    # 顯示選項-目標檔案加密
    rb1.place(x=370,y=70)

    # 顯示選項-目標檔案解密
    rb2.place(x=370,y=150)

    # 顯示選項-檔案藏入影片
    rb3.place(x=370,y=230)

    # 顯示選項-影片還原檔案
    rb4.place(x=370,y=310)
    
    # 顯示按鈕-下一步
    next_btn = Button(main_root, text='下一步', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=selectitem)
    next_btn.place(x=410, y=440)

    # 顯示按鈕-離開系統
    exit_btn = Button(main_root, text='離開系統', compound=LEFT, width=7,font = "微軟正黑體 20", cursor='mouse', command=(main_root.destroy))
    exit_btn.place(x=610, y=440)

    # 隱藏輸入框-請按左邊按鈕選擇載體影片
    e10.place_forget()

    # 隱藏圖片按鈕-avi.png
    select3_btn.place_forget()

    # 隱藏按鈕-還原檔案
    ext_btn.place_forget()     

    # 隱藏按鈕-上一步
    back_btn.place_forget()    

    # 隱藏文字-[ 注意 ] 要從影片還原檔案，須有隱藏檔案到影片時產生的keys，然後與影片放在同一路徑下。還原的檔案會產出在與影片同一路徑下。
    text.place_forget()  
  

""" 選擇要加密的檔案 """
def select_encrypt_file():

    # 清除 輸入框-請按左邊按鈕選擇要加密的檔案 內容
    e1.delete(0,END)

    # 開啟選擇檔案視窗
    global str5
    str5=filedialog.askopenfilename(title="選擇來源檔案",filetypes=[("所有檔案", ".*")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e1.insert(0,str5)
    print(str5)


""" 儲存加密後的檔案 """
def save_encrypt_file():

    # 清除 輸入框-請按左邊按鈕儲存加密後的檔案 內容
    e2.delete(0,END)

    # 開啟儲存檔案視窗
    global str7
    str7=filedialog.asksaveasfilename(title="儲存目的檔案",filetypes=[("所有檔案", ".*")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e2.insert(0,str7) 
    print(str7)


""" 執行加密動作 """
def run_encrypt():

    dev3 = usb.core.find(idVendor=0x090c, idProduct=0x1000)
    
    try:
        if e1.get() == '' or e1.get() == '請按左邊按鈕選擇要加密的檔案':
            messagebox.showinfo('注意', '必須指定選擇檔案!')
            return
        elif e2.get() == '' or e2.get() == '請按左邊按鈕儲存加密後的檔案':
            messagebox.showinfo('注意', '必須指定儲存檔案!')
            return
        elif e3.get() == '' or e3.get() =='請輸入自行定義的檔案密碼':
            messagebox.showinfo('注意', '必須指定檔案密碼!')
            return
        elif dev3 is None:
            messagebox.showerror('注意', '請插上指定USB!')
            return
        else:
            play_mp3("./sound/檔案加密中.mp3")

            time.sleep(2)

            # 取得手動輸入密碼值
            user_keyin = e3.get()

            # 密碼進行加密運算組態
            password = user_keyin.encode()
            salt = b'salt_'
            kdf = PBKDF2HMAC(algorithm=(hashes.SHA256()),
              length=32,
              salt=salt,
              iterations=100000,
              backend=(default_backend()))
            key = base64.urlsafe_b64encode(kdf.derive(password))

            # 開啟檔案
            file = open(str5, 'rb')

            # 讀取檔案資料
            data = file.read()

            # 關閉檔案
            file.close()
            
            token = Fernet(key)

            start = time.time()

            # 加密檔案資料
            encrypted = token.encrypt(data)

            # 儲存檔案
            file = open(str7, 'wb')

            # 寫入檔案資料
            file.write(encrypted)

            # 關閉檔案
            file.close()
            
            end = time.time()

            print('檔案加密花費' + str(round(end - start, 6)) + '秒')

            play_mp3("./sound/成功將檔案加密.mp3")

            time.sleep(2)          

            messagebox.showinfo('檔案加密','總共花費' + str(round(end - start, 6)) + '秒')
            
    except:
        messagebox.showinfo('注意', '必須指定選擇檔案、儲存檔案和密碼!')


""" 選擇要解密的檔案 """
def select_decrypt_file():

    # 清除 輸入框-請按左邊按鈕選擇要解密的檔案 內容
    e4.delete(0,END)

    # 開啟選擇檔案視窗
    global str6
    str6=filedialog.askopenfilename(title="選擇來源檔案",filetypes=[("所有檔案", ".*")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e4.insert(0,str6)
    print(str6)


""" 儲存解密後的檔案 """
def save_decrypt_file():

    # 清除 輸入框-請按左邊按鈕儲存解密後的檔案 內容
    e5.delete(0,END)

    # 開啟儲存檔案視窗
    global str8
    str8=filedialog.asksaveasfilename(title="儲存目的檔案",filetypes=[("所有檔案", ".*")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e5.insert(0,str8) 
    print(str8)


""" 執行解密動作 """
def run_decrypt():

    dev4 = usb.core.find(idVendor=0x090c, idProduct=0x1000)
    
    try:
        if e4.get() == '' or e4.get() == '請按左邊按鈕選擇要解密的檔案':
            messagebox.showinfo('注意', '必須指定選擇檔案!')
            return
        elif e5.get() == '' or e5.get() == '請按左邊按鈕儲存解密後的檔案':
            messagebox.showinfo('注意', '必須指定儲存檔案!')
            return
        elif e6.get() == '' or e6.get() =='請輸入自行定義的檔案密碼':
            messagebox.showinfo('注意', '必須指定檔案密碼!')
            return
        elif dev4 is None:
            messagebox.showerror('注意', '請插上指定USB!')
            return
        else:
            play_mp3("./sound/檔案解密中.mp3")

            time.sleep(2)

            # 取得手動輸入密碼值
            user_keyin = e6.get()

            # 密碼進行加密運算組態
            password = user_keyin.encode()
            salt = b'salt_'
            kdf = PBKDF2HMAC(algorithm=(hashes.SHA256()),
                  length=32,
                  salt=salt,
                  iterations=100000,
                  backend=(default_backend()))
            key = base64.urlsafe_b64encode(kdf.derive(password))

            # 開啟檔案
            file = open(str6, 'rb')

            # 讀取檔案資料            
            data = file.read()

            # 關閉檔案
            file.close()
            
            token = Fernet(key)

            start = time.time()

            # 解密檔案資料
            decrypted = token.decrypt(data)

            # 儲存檔案
            file = open(str8, 'wb')

            # 寫入檔案資料
            file.write(decrypted)

            # 關閉檔案
            file.close()
            
            end = time.time()

            print('檔案解密花費' + str(round(end - start, 6)) + '秒')

            play_mp3("./sound/成功將檔案解密.mp3")

            time.sleep(2)

            messagebox.showinfo('檔案解密','總共花費' + str(round(end - start, 6)) + '秒')

    except(cryptography.fernet.InvalidToken,TypeError):
        time.sleep(2)
        play_mp3("./sound/請輸入正確密碼.mp3")
        messagebox.showerror('密碼錯誤', '請輸入正確密碼!')


""" 選擇崁入檔案 """
def select_embed_file():

    # 清除 輸入框-請按左邊按鈕選擇要隱藏的檔案 內容
    e7.delete(0,END)

    # 開啟選擇檔案視窗
    global str1
    file1=filedialog.askopenfilename(title="選擇隱藏檔案",filetypes=[("所有檔案", ".*")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e7.insert(0,file1)

    # 置換文字
    str1 = file1.replace('/', '\\\\')
    print(str1)


""" 選擇被崁入檔案的MP4影片 """
def select_mp4_file():

    # 清除 輸入框-請按左邊按鈕選擇當載體的影片 內容
    e8.delete(0,END)

    # 開啟選擇檔案視窗
    global str2
    file2=filedialog.askopenfilename(title="選擇載體影片",filetypes=[("影片檔案(MP4)", ".mp4")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e8.insert(0,file2)

    # 置換文字
    str2 = file2.replace('/', '\\\\')
    print(str2)


""" 儲存AVI影片檔案 """
def save_avi_file():

    # 清除 輸入框-請按左邊按鈕儲存產生的載體影片 內容
    e9.delete(0,END)

    # 開啟儲存檔案視窗
    global str3
    file3=filedialog.asksaveasfilename(title="輸出載體影片",filetypes=[("影片檔案(AVI)", ".avi")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e9.insert(0,file3)

    # 置換文字
    str3 = file3.replace('/', '\\\\')
    print(str3)


""" 選擇被崁入檔案的AVI影片 """
def select_avi_file():

    # 清除 輸入框-請按左邊按鈕選擇載體影片 內容
    e10.delete(0,END)

    # 開啟選擇檔案視窗
    global str4
    file4=filedialog.askopenfilename(title="選擇載體影片",filetypes=[("影片檔案(AVI)", ".avi")],defaultextension=".*")

    # 將檔案路徑顯示在輸入框
    e10.insert(0,file4)

    # 置換文字
    str4 = file4.replace('/', '\\\\')
    print(str4)


""" 執行檔案隱藏於影片 """
def run_embed():

      dev1 = usb.core.find(idVendor=0x090c, idProduct=0x1000)
    
      try:
          if e7.get() == '' or e7.get() == '請按左邊按鈕選擇要隱藏的檔案':
              messagebox.showinfo('注意', '必須指定選擇檔案!')
              return
          elif e8.get() == '' or e8.get() == '請按左邊按鈕選擇當載體的影片':
              messagebox.showinfo('注意', '必須指定載體影片!')
              return
          elif e9.get() == '' or e9.get() =='請按左邊按鈕儲存產生的載體影片':
              messagebox.showinfo('注意', '必須指定輸出影片!')
              return
          elif dev1 is None:
              messagebox.showerror('注意', '請插上指定USB!')
              return
          else:
              hide(str2, str3, str1, will_shuffle=True, dict_index=None)
              return
      except:
          messagebox.showinfo('注意', '必須指定隱藏檔案、載體影片和產出影片!')    
   

""" 執行從影片解出檔案 """    
def run_extract():

    dev2 = usb.core.find(idVendor=0x090c, idProduct=0x1000)

    try:
        if e10.get() == '' or e10.get() == '請按左邊按鈕選擇載體影片':
            messagebox.showinfo('注意', '必須指定載體影片!')
        elif dev2 is None:
            messagebox.showerror('注意', '請插上指定USB!')
            return
        else:
            index = str4.rfind('\\')
            print(index)
            print(str4[0:index+1])
            # 要檢查的檔案
            filepath = str4[0:index+1]+'keys'
            # 檢查檔案是否存在
            if os.path.isfile(filepath) == False:
                messagebox.showinfo('注意', 'keys檔案不存在!')
            else:
                retrieve(str4, str4[0:index+1]+'keys')
   
    except Exception:
     return


""" 檔案隱藏於影片 """
def hide(video_file_input, video_file_output, message_file, will_shuffle=False, dict_index=None):
    # open video file
    video_file = cv2.VideoCapture(video_file_input)
    # retrieve some information about the video file
    fps = video.frames_per_second(video_file)
    width = video.video_width(video_file)
    height = video.video_height(video_file)

    # create object writer
    writer = cv2.VideoWriter(video_file_output, cv2.VideoWriter_fourcc(*VIDEO_CODEC), fps, (width, height), True)
     
    # open the file to hide and get the bytes
    message_bytes = message.read_file(message_file)

    # length of the bytes to hide
    message_bytes_length = len(message_bytes)

    # equals to dict_index, if the user did not input no dict_index then it is None and one will be generated
    index_dict = dict_index

    # check if it is necessary to generate dictionary of indexes
    if will_shuffle and index_dict is None:
        # generate the dictionary of indexes
        index_dict = utils.generate_dictionary(10)

    # counter of the frames
    frame_count = 0

    # number of bytes that a frame can hide
    frames_bytes_length = video.bytes_to_hide_frame_count(video_file)

    # number of bytes that can be hidden in the video
    video_bytes_to_hide = video.bytes_to_hide_count(video_file)

    # check if the message can be hidden
    if message_bytes_length > video_bytes_to_hide:
        messagebox.showinfo('檔案資訊','載體視訊小於檔案，\n空間不足，無法隱藏消息。')
        print('空間不足，無法隱藏訊息')
        
    time.sleep(2)

    play_mp3("./sound/檔案隱藏中.mp3")
    
    print('產生影片中...')
    hstart = time.time()
    
    # loop thought the video frame by frame
    while video_file.isOpened():
        ret, frame = video_file.read()

        # check if we have a frame
        if not ret:
            break

        # calculate the limit
        start = frames_bytes_length * frame_count
        stop = frames_bytes_length * frame_count + frames_bytes_length

        # check if there are more bytes to hide
        if start <= message_bytes_length:
            # get a sublist to byte the frames
            bytes_to_hide_sub_list = message_bytes[start:stop]
            # hide the message in the frame
            modified_frame = bm.hide_in_frame(frame, bytes_to_hide_sub_list, index_dict)
            # save the frame to the output file
            writer.write(modified_frame)
        else:
            # if not continue to save the default frames
            writer.write(frame)

        frame_count += 1
    
    # generate the file to retrieve the message
    utils.generate_key_file(message_file, len(message_bytes), index_dict)

    video_file.release()
    writer.release()

    # copy the audio stream from the original file to the carrier file
    video.copy_audio(video_file_input, video_file_output)


    hend = time.time()
    print('檔案成功地被建立')
       
    play_mp3("./sound/成功將檔案隱藏.mp3")
    time.sleep(2)
    messagebox.showinfo('檔案崁入影片','總共花費' + str(round(hend - hstart, 2)) + '秒')
   

""" 從影片解出檔案 """
def retrieve(video_file_location, key_file):
    
    
    # open video file
    try:
        video_file = cv2.VideoCapture(video_file_location)
    except ImportError:
        print('開啟檔案錯誤')
        
    time.sleep(2)
    play_mp3("./sound/檔案還原中.mp3")
    
      
    
    # retrieve from the file the data
    keys_data = utils.read_key_file(key_file)

    # number of bytes
    bytes_length = keys_data['length']

    # dictionary containing the indexes
    dictionary = None

    # check if method is shuffle
    if keys_data['method'] == 'shuffle':
        dictionary = keys_data['indexes_dictionary']

    # get the name of result file
    result_file = keys_data['file_name']

    # calculate the output file location
    file_directory = path.dirname(video_file_location)
    if file_directory != '':
        final_name = file_directory + '/' + result_file
    else:
        final_name = result_file

    
    # array with the bytes extracted
    extracted_bytes_array = []

    # number of bytes that a frame can hide
    frames_bytes_length = video.bytes_to_hide_frame_count(video_file)

    # bytes left to retrieve
    bytes_left = bytes_length


    hstart = time.time()
    # retrieve the data
    # loop thought the video frame by frame
    while video_file.isOpened():
        if bytes_left <= 0:
            break

        ret, frame = video_file.read()

        # If we have more bytes to retrieve and not more frames, then something is wrong
        if not ret:
            print('無效的影片檔案和/或KEY檔案')
            messagebox.showinfo('檔案資訊','無效的影片檔案和/或KEY檔案')
            
        if bytes_left >= frames_bytes_length:
            bytes_to_get = frames_bytes_length
            bytes_left -= bytes_to_get
        else:
            bytes_to_get = bytes_left
            bytes_left = 0

        # extract the bytes in the frame
        extracted_bytes = bm.retrieve_in_frame(frame, bytes_to_get, dictionary)

        # add the extracted bytes to the final result
        extracted_bytes_array.extend(extracted_bytes)

    video_file.release()

    # create the hidden file
    result = message.write_file(final_name, extracted_bytes_array)
   
    
    if result:
        hend = time.time()
        print('訊息成功被解出')
        
        play_mp3("./sound/成功將檔案還原.mp3")
        time.sleep(2)
       
        messagebox.showinfo('影片解出檔案','總共花費' + str(round(hend - hstart, 6)) + '秒')
        
    else:
        print('最終檔案建立錯誤')
