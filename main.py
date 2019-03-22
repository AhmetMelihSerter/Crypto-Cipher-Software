# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 21:33:40 2018

@author: Ahmet Melih Serter
"""

from config import *
from main2 import *

class GUI(SuperNesne):
    
    def __init__(self):
        """
            Tkinter main.py nesnesinden kalıtılır. Temel tkinter özellikleri super() nesnesinde oluşturulur.
            Programın olduğu dizindeki veritabanları taranır. Listbox'a eklenir.
            Create Database butonu ile yeni hesap oluşturulur. 
            Eğer aynı veritabanından yoksa yeni veritabanı oluşturulur.
            Kullanıcı kendi veritabanını seçip şifresini girerek login butonu ile programa giriş yapar.
        """
        self.limit=3
        window=super().__init__("Login","320x300") # (title,window_size)
        yscroll = Scrollbar(window, orient="vertical") # Scrollbar oluşturuluyor.
        yscroll.grid(row=0, column=7,columnspan=1, rowspan=5, sticky=N+S+W,pady=(20,10))
        data=self.find_db() # Databaseleri arıyoruz.
        self.listbox_data=StringVar(value=data) # Listbox'un içine databaseler yerleştiriliyor.
        self.listbox_db=Listbox(window,listvariable=self.listbox_data,yscrollcommand=yscroll.set)
        self.listbox_config(self.listbox_db) # Listbox ayarları yapılıyor.
        self.listbox_db.grid(row=0,column=2,columnspan=5,rowspan=5,padx=(20,0),pady=(20,10))
        yscroll["command"] = self.listbox_db.yview # Scrollbar bağlanıyor.
        Label(window,text="Password",anchor="center").grid(row=6,column=1,columnspan=4,padx=(20,0),pady=(10,10))
        self.password_entry=Entry(window,show="*",validate="key") # Şifre Alanı, key: limitlemek için gerekiyor.
        """
            ValidateCommand:İşlemi onaylamadan işlem yapmamızı engelliyor yani işlem yapmadan önce gidilen
            fonksiyondan True değeri almamızı istiyor.
        """
        # Şifreye limit koy. "16"
        self.password_entry["validatecommand"]=(self.password_entry.register(self.maxlenght),'%P',16,True) 
        self.password_entry.grid(row=6,column=5,columnspan=4,pady=(10,10))
        Button(window,text="Create Database",command=lambda:self.new_db(window)).grid(row=7,column=1,columnspan=4,
              padx=(20,0))
        self.login_buton=Button(window,text="Login",command=lambda:self.login_process(window))
        self.login_buton.grid(row=7,column=5,columnspan=4)
        self.state_disabled(self.login_buton) # Giriş Butonu Disable edildi çünkü veritabanı seçilmedi.
        self.listbox_db.bind("<<ListboxSelect>>",\
                             lambda event:self.login_enable(window)) # Liste verisi seçilirse fonksiyona git.
        window.mainloop() # Pencere sabitlendi.
    def login_process(self,window):
        """
            Şifre 5 haneden küçükse uyarı veriyor.
        """
        key=self.password_entry.get() # şifre alanındaki veri key değişkeni'nin içine alınıyor.
		# 3 kere şifre deneme hakkı tanınıyor eğer 3 den fazla denenirse program kapatılıyor.
        self.limit-=1
        if self.limit<0:
            window.destroy()
        elif len(key)<5:
            showwarning("Warning",\
                        "Password must be at least 5 characters long!!!\nYou Have Trial Remaining {}".format(self.limit))
        else:
            """
                self.listbox_db.curselection()[0]=id alınır.
                self.listbox_db.get()=listboxdaki veri id ile alınır.
            """
            database_name=self.listbox_db.get(self.listbox_db.curselection()[0])+".db" # Seçili db alınır.
            control=self.find_db(database_name) # Veritabanı kontrolü yapılıyor. return true or false
            if control:              
                con=sql.connect(database_name) # Veritabanı bağlantısı
                db=con.cursor() # İşlem yapabilimek için imleç oluşturuldu.
                db.execute("select file,title from data") # Sorgumuz: Veriler veritabanından çekilir.
                datum=db.fetchone() # fetchone sadece 1 veri çeker.
                db.execute("select crypto_method from crypto") # Sorgumuz: Veriler veritabanından çekilir.
                crypto_type=db.fetchone() # fetchone sadece 1 veri çeker.
                con.close() # Bağlantıyı kapat.              
                if crypto_type[0]=="AES-256": # Kripto tipini belirliyoruz.
                    crypto=AESCipher(key) # Aes nesnesi oluştur.
                elif crypto_type[0]=="Blowfish":
                    crypto=BlowfishCipher(key) # Blowfish nesnesi oluştur.
                try:
                    """
                        Bazen şifre çözerken hata oluşabiliyor. Bu yüzden try,except kullanılmalı.
                    """   
                    descrpyt_datum=[crypto.decrypt(i) for i in datum if len(crypto.decrypt(i))==16]
                except Exception as hata:
                    print(hata)
#                    showerror("Error","An unknown error occurred\nPlease Try Again Later!!!")
                finally:
                    if len(descrpyt_datum)==0: # Liste içinde veri yoksa giriş yaparken bir problem oluştu.
                        showwarning("Warning",\
                                    "Password is incorrect please try again!!!\nYou Have Trial Remaining {}".format(self.limit))
                    else:                   
                        window.destroy()# Pencere sonlandırılır.
                        GUI2(crypto_type[0],key,database_name) # Giriş yapıldı.
            else:
                showerror("Error","File is not found!!!\nPlease Try Again Later")
                
    def find_db(self,db_control=False):
        """
            Hatalı kod taradığı dizinde klasör varsa çöküyor!!! Çünkü klasörün uzantısı yok!!!
            dl_split=[i.split(".") for i in directory_list]
            Son Not Problem Daha Kısa Kodla Çözüldü!!!
            os.path.splitext()=dosyanın dosya adi ile uzantısını ayırır.
        """
        """
            Dizin Okuma ve Filtreleme
            db_control:İçinde veritabanı gelirse dizinde böyle bir veritabanı var mı kontrolünü yapacaktır.
            db_control:False değeri gelirse veritabanlarını arayacaktır.
            db_split[i][0]:Dizindeki dosyaların adıdır.
            db_split[i][1]:Dizindeki dosyaların uzantısıdır.
        """
        directory_list=os.listdir() # Dizini oku.
        dl_split=[os.path.splitext(directory_list[i]) for i in range(len(directory_list))] # Uzantıları ayırır.
        # Filtrele ve dizine at.
        if db_control:
            for i in range(len(dl_split)):
                if dl_split[i][1]==".db" and dl_split[i][0]==db_control:
                    return False
            return True
        else:
            true_db=[dl_split[i][0] for i in range(len(dl_split)) if dl_split[i][1]==".db" or dl_split[i][1]==".sqlite"]
            return true_db  
        
    def login_enable(self,window):
        """
            Listede veri seçilirse giriş butonunu aktif et.
            Listeden veri seçilirken hata oluşabiliyor. Yani veriyi seçerken seçim kaybolabiliyor. 
            bind:Enter tuşu ile butonu aktif et
        """
        self.state_active(self.login_buton)
        window.bind("<Return>",lambda event:self.login_process(window))
        try:
            self.listbox_selected=self.listbox_db.index(self.listbox_db.curselection()[0])
        except:
            self.state_disabled(self.login_buton)
            window.unbind("<Return>") # Liste verisi seçimi bulunamazsa Enter tuşu iptal edilir
    def new_db(self,window):
        self.window_freeze(window) # Pencere dondurulur.
        window2=super().__init__("Create New Database","320x300") # (title,window_size)
        """
            Protocol: Çarpı butonuna basılınca çalıştırılacak fonksiyonu belirliyoruz.
        """
        window2.protocol('WM_DELETE_WINDOW',lambda:self.window_freeze(window,window2)) #Delete butonunu yönlendirir.
        Label(window2,text="Database Name").grid(row=0,column=1,columnspan=2,padx=(20,0),pady=(20,0))
        self.db_name=Entry(window2,validate="key") # Veritabanı adı textbox
        self.db_name["validatecommand"]=(self.db_name.register(self.maxlenght),"%P",16)
        self.db_name.grid(row=0,column=3,columnspan=2,pady=(20,0),padx=(20,0))
        Label(window2,text="Password").grid(row=1,column=1,columnspan=2,padx=(20,0),pady=(20,0))
        self.new_password=Entry(window2,show="*",validate="key") # Veritabanı şifre textbox
        """
            ValidateCommand:İşlemi onaylamadan işlem yapmamızı engelliyor yani işlem yapmadan önce gidilen
            fonksiyondan True değeri almamızı istiyor.
        """
        self.new_password["validatecommand"]=(self.new_password.register(self.maxlenght),"%P",16,True)#şifreye limit koy."16"
        self.new_password.grid(row=1,column=3,columnspan=2,padx=(20,0),pady=(20,0))
        Label(window2,text="Encrypt Type").grid(row=2,column=1,columnspan=2,padx=(20,0),pady=(20,0))
        self.combobox_encryption=Combobox(window2,values=("AES-256","Blowfish")) # Şifreleme Türü
        self.combobox_encryption.current(0) # Birinci Veriyi Seçer
        self.combobox_config(self.combobox_encryption) # Combobox ayarları yapılıyor.
        self.combobox_encryption.grid(row=2,column=3,columnspan=2,padx=(20,0),pady=(20,0))
        Button(window2,text="Create",command=lambda: self.new_db_process(window,window2)).grid(row=3,column=2,\
              columnspan=2,padx=(20,0)) # Ekleme butonu 
        Button(window2,text="Cancel",command=lambda: self.window_freeze(window,window2)).grid(row=3,\
              column=4,columnspan=2,padx=(10,0)) # İptal butonu
        window2.bind("<Return>",\
                             lambda event:self.new_db_process(window,window2)) # Liste verisi seçilirse fonksiyona git.
        window2.mainloop() # Pencere sabitlendi.
    
    def control_db(self,database_name):
        """
            Veritabanı kontrolu yapılıyor. Veritabanı varsa yeni veritabanı oluşturulmaz.
        """
        return self.find_db(database_name)
    
    def new_db_process(self,window,window2):
        """
            Veritabanı kontrolü ve şifre uzunluğu kontrol ediliyor.
        """
        database_name=self.db_name.get()+".db" # Veritabanı adının sonuna ".db" ekle.
        #print(self.combobox_encryption.get())
        if self.control_db(self.db_name.get())==False:
            """
                os.path.exists(dosya)==Dosyanın olup olmadığını kontrol eder true ya da false döndürür.
            """
            showwarning("Warning","Database already exists!!!",parent=window2)
        elif len(self.new_password.get())<5:
            showwarning("Warning","Password must be at least 5 characters long!!!",parent=window2)
            """
            Burası Düzenlenecek!!!
            harf taraması yapılacak!!!
            """
        elif len(self.db_name.get())==0:
            showwarning("Warning","Database name cannot be empty!!!",parent=window2)
        else:
            """
                random_data=rastgele karakter oluştur     
            """
            random_data=lambda x:(''.join(random.choice(string.ascii_letters+string.digits) for i in range(x)))
            if self.combobox_encryption.get()=="AES-256":
                crypto=AESCipher(self.new_password.get()) # Aes nesnesi oluştur.
            elif self.combobox_encryption.get()=="Blowfish":
                crypto=BlowfishCipher(self.new_password.get()) # Blowfish nesnesi oluştur.
            # 16 karakterli rastgele veri oluştur. Bytes olan veri utf-8 e dönüştürülür.(key,veri)
            file_val=crypto.encrypt(random_data(16))  # Dosya
            # 16 karakterli rastgele veri oluştur. Bytes olan veri utf-8 e dönüştürülür.(key,veri)
            title_val=crypto.encrypt(random_data(16)) # Başlık 
            # 64 karakterli rastgele veri oluştur. Bytes olan veri utf-8 e dönüştürülür.(key,veri)
            crypto_val=crypto.encrypt(random_data(64)) # Veri
#            print("<->",title_val,"<->")
#            print("<->",crypto_val,"<->")
            con=sql.connect(database_name) # Veritabanı bağlantısı dosya yoksa yenisi oluşturulur.
            db=con.cursor() # İşlem yapabilimek için imleç oluşturuldu.
            sorgu="create table data (id integer not null primary key autoincrement,file text not null," \
                "title text not null,crypto text not null);"
            sorgu2="create table crypto (id integer not null primary key autoincrement,crypto_method text not null);"
            db.execute(sorgu) # Sorguyu ekle.
            db.execute(sorgu2) # Sorguyu ekle.
            sorgu3="insert into data (file,title,crypto) values ('{}','{}','{}')" \
                .format(file_val,title_val,crypto_val)
            sorgu4="insert into crypto (crypto_method) values ('{}')".format(self.combobox_encryption.get())
            """
                print(sorgu)  Sorguları ekrana yazdırır.
                print(sorgu2) Sorguları ekrana yazdırır.
            """
            db.execute(sorgu3) # Sorguyu ekle.
            db.execute(sorgu4) # Sorguyu ekle.
            con.commit() # Sorguyu çalıştır. 
            con.close() # Bağlantıyı kapat.
            data=self.find_db() # Veritabanını bul.
            self.listbox_data.set(data) # Listbox'a yeni veritabanını ekle.
            db_search=self.listbox_db.get(0,"end").index(self.db_name.get()) # Yeni veritabanını ara.
            self.listbox_db.selection_clear(0,"end")# Seçili öğenin seçimini iptal eder.
            self.listbox_db.select_set(db_search) # Yeni veritabanını seç.
            self.login_enable(window) # Giriş Butonu aktif edildi.
            """
                a=key_encrypt.decrypt(title_val)
                b=key_encrypt.decrypt(crypto_val)
                print(a)
                print(b)
            """
            self.window_freeze(window,window2) # Pencereyi çöz,pencere2'yi kapat.
 
GUI()

        
        
        
        
        
        
        
        
