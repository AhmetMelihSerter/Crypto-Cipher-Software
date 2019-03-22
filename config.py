# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 17:51:11 2019

@author: Ahmet Melih Serter
"""

import os
import random
import string
import sqlite3 as sql
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from mini_radiance import ThemedStyle 
from aes import *
from blowfish import *

class SuperNesne:
    def __init__(self,title,size):
        window = Tk() # Pencere oluşturulur.
        window.title(title) #Başlık Adı Giriş
        theme = ThemedStyle(window) # Temayı oluşturuyoruz.
        theme.set_theme("radiance") # Temanın adı.
        window.geometry(size) # Pencere Boyutu Girilir.
        window.resizable(False,False) # Pencere boyutunu ayarlama iptal edilir.
        self.center(window)
        return window 
    def listbox_config(self,listbox):
        """
            Normalde tcl ile çözüldü fakat global olması için böyle bıraktım!!!
            Listbox içindeki ayarlar burada yapılır.
        """
        listbox['selectbackground']="#ed7442"
        listbox['activestyle']="none"
    def combobox_config(self,combobox):
        """
            Normalde tcl ile çözüldü fakat global olması için böyle bıraktım!!!
            Combobox içindeki ayarlar burada yapılır.
        """
        combobox.option_add("*TCombobox*Listbox*selectBackground", "#ed7442")
    def window_freeze(self,window,window2=False):
        """
            Window penceresi dondurulur. Window2 None ise window'un donması iptal edilir.
        """
        if window2==False:
            window.wm_attributes("-disabled", True) # Pencereyi dondurur.
        else:
            window.wm_attributes("-disabled", False) # Pencere donması İptal edilir.
            window2.destroy() # Pencere2 sonlandırılır.
    def center(self,win):
        """
            Pencereyi Ekrana Ortalıyor.
            winfo_screenwidth():Bilgisayarın en çözünürlüğü
            winfo_screenheight():Bilgisayarın boy çözünürlüğü
            Bilgisayarın çözünürlüğünden pencerenin boyutunu çıkartıyor.
            Formülü    x: (pc_x//2)-(win_x//2)     y:(pc_y//2)-(win_y//2)
        """
        win.update_idletasks() #Pencerenin bekleyen işlerini pencereye uyguluyor.
        width = win.winfo_width() #Pencerenin en'ini alıyor.
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height() #Pencerenin boy'unu alıyor.
        titlebar_height = win.winfo_rooty() - win.winfo_y() # Başlık yüksekliğini alıyor.
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y)) # Pencere konumunu ayarlar.
        win.deiconify() # Pencere boyutu ile oynandığı için pencere silinip tekrardan oluşturuyor.
        """
            print("Width:",width,"\nheight:",height,"\nwin.winfo_x():",win.winfo_x(),"\nwin.winfo_y():",win.winfo_y())
            print("win_width:",win_width,"\nwin_height:",win_height,"\nfrm_width:",frm_width)
            print("win.winfo_rootx():",win.winfo_rootx(),"\nwin.winfo_rooty():",win.winfo_rooty())
            print("titlebar_height:",titlebar_height,"\nwin.winfo_screenwidth():",win.winfo_screenwidth())
            print("win.winfo_screenheight():",win.winfo_screenheight())
        """
    def maxlenght(self,text,limit,password_and_login=False):
        """
            Entry için bir tuşa basıldığında bu fonksiyon çalışır. Validatecommand ile tetiklenir.
            Fonksiyonun geri dönüşü True olursa işlem yapılır. False olursa işlem yapma.
            password:Entry şifre ise True değilse False olarak belirlenir. False olarak gelen entryler isalpha() olarak
            belirlenir.
        """
        if len(text)>int(limit) or (password_and_login==False and not text.isalpha()):
            return False
        return True
    def state_active(self,btn,btn1=False):
        """
            Buton ve Entry'leri aktif eden fonksiyondur.
        """
        btn["state"]="normal" # Buton veya Entry aktif edildi.
        if btn1: # text_data gelirse buraya girer ve background değişir.
            btn["bg"]="white"
    def state_disabled(self,btn=False,btn1=False):
        """
            if block'una entryler
            elif block'una text
            else block'una butonlar girer
        """
        if btn==False and btn1: # title_data'in çalışması için ilk verinin boş,ikinci verinin dolu gelmesi lazım.
            btn1["state"]="readonly"
        elif btn and btn1: # text_data gelirse buraya girer disable olur.Background değişir..
            btn["bg"]="#F6F4F2" # Tkinter üzerinde halledildi  
            btn["state"]="disabled"
        else: # title_data ve text_data dışındaki butonlar buraya girer.
            btn["state"]="disabled"
