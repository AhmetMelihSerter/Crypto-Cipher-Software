# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 20:31:11 2018

@author: Ahmet Melih Serter
"""

from config import *

class GUI2(SuperNesne):
    def __init__(self,crypto_type,key,db_name):
        self.database_name=db_name # Giriş yapılan veritabanı adı.
        self.crypto_type=crypto_type
        self.key=key # Giriş yapılan veritabanı'nın key'i alınır.
        window=super().__init__("Welcome","1026x560")
        Button(window,text="Listing",width=20,command=lambda: self.listing_file(window)) \
                .grid(row=0,column=0,columnspan=10,padx=(6,3),pady=5) # Listeleme Butonu
        self.add_buton=Button(window,text="Add",width=20,command=lambda: self.add_file(window))
        self.add_buton.grid(row=0,column=10,columnspan=10,padx=3,pady=5) # Ekleme Butonu
        self.update_buton=Button(window,text="Edit",width=20,command=lambda: self.update_file(window))
        self.update_buton.grid(row=0,column=20,columnspan=10,padx=3,pady=5) # Düzenleme Butonu
        self.delete_buton=Button(window,text="Delete",width=20,command=lambda:self.delete_file(window))
        self.delete_buton.grid(row=0,column=30,columnspan=10,padx=3,pady=5) # Silme Butonu
         # Çıkış Butonu
        Button(window,text="Exit",width=20,command=window.destroy).grid(row=0,column=40,columnspan=10,padx=3,pady=5) 
        self.state_disabled(self.add_buton) # Başlangıçta veri seçilmediğinden buton disable edildi.
        self.state_disabled(self.update_buton) # Başlangıçta  veri seçilmediğinden buton disable edildi.
        self.state_disabled(self.delete_buton) # Başlangıçta veri seçilmediğinden buton disable edildi.
        window.mainloop() # Pencere sabitlendi.
    def add_file(self,window):
        self.window_freeze(window) # Pencereyi Dondur.
        window2=super().__init__("Add New File","700x580") # Pencere oluşturulur.
        """
            Protocol: Çarpı butonuna basılınca çalıştırılacak fonksiyonu belirliyoruz.
        """
        window2.protocol('WM_DELETE_WINDOW',lambda:self.window_freeze(window,window2))
        Label(window2,text="New File Name:",anchor="center").grid(row=0,column=0,columnspan=4,pady=(12,6),padx=(12,50))
        self.new_file=Entry(window2,width=30,validate="key") # Eklenecek dosyanın adı
        self.new_file["validatecommand"]=(self.new_file.register(self.maxlenght),'%P',15,True) # "15" Dosya adı limiti
        self.new_file.grid(row=0,column=4,columnspan=4,pady=(12,6))
        Label(window2,text="New Title:",anchor="center").grid(row=1,column=0,columnspan=4,pady=6,padx=(12,50))
        self.new_title=Entry(window2,width=75,validate="key") # Eklenecek Başlık
        self.new_title["validatecommand"]=(self.new_title.register(self.maxlenght),'%P',50,True) # "50" Başlık limit
        self.new_title.grid(row=1,column=4,columnspan=26,pady=6)
        Label(window2,text="New Text:",anchor="center").grid(row=2,column=0,columnspan=4,pady=6,padx=(12,50))
        self.new_text=Text(window2,width=57,height=27) # Eklenecek Metin
        self.new_text.grid(row=2,column=4,columnspan=26,rowspan=30,pady=6)
        Button(window2,width=20,text="Add New File",command=lambda:self.add_file_processing(window,window2))\
                .grid(row=32,column=4,columnspan=13,padx=12) # Ekleme butonu
        Button(window2,width=20,text="Cancel",command=lambda:self.window_freeze(window,window2))\
                .grid(row=32,column=17,columnspan=13,padx=12) # İptal butonu
        window2.mainloop() # Pencere sabitlendi.
    def add_file_processing(self,window,window2):
        """
            Alanlar boş sa ekrana doldurulması gerektiği yazdırılır.
            Veriler ilk önce şifrelenir. Sonra veritabanı bağlantısı yapılır.
            Veritabanına şifreli halde yazılır.
        """
        if len(self.new_file.get())<1 or len(self.new_title.get())<1 or len(self.new_text.get(1.0,"end"))<1:
            showwarning("Warning","File name and title cannot be empty!!!",parent=window2)
        else:
            if self.crypto_type=="AES-256":
                crypto=AESCipher(self.key) # Aes nesnesi oluşturuldu.
            elif self.crypto_type=="Blowfish":
                crypto=BlowfishCipher(self.key) # Blowfish nesnesi oluşturuldu.
            file=crypto.encrypt(self.new_file.get()) # Yeni file'yi şifrele
            title=crypto.encrypt(self.new_title.get()) # Yeni title'yi şifrele
            text=crypto.encrypt(self.new_text.get(1.0,"end")) # Yeni text'ti şifrele
            con=sql.connect(self.database_name) # Veritabanı bağlantısı oluşturulur.
            db=con.cursor() # İşlem yapabilimek için imleç oluşturuldu.
            sorgu="insert into data (file,title,crypto) values ('{}','{}','{}')" \
                    .format(file,title,text) # Sorgumuz: Yeni veriler ekleniyor.
            db.execute(sorgu) # Sorguyu ekle.
            con.commit() # Sorguyu çalıştır. 
            con.close() # Bağlantıyı kapat.
            self.window_freeze(window,window2) # Pencereyi çöz,pencere2'yi kapat.
            self.listing_file(window) # Listeleme fonksiyonun baştan çalıştırır.
    def update_file(self,window):
        """
            Düzenle butonuna basılınca Update_Buton,Cancel_Buton,Entry,Text aktif edildi.
        """
        self.state_active(self.buton_update)
        self.state_active(self.cancel_buton)
        self.state_active(self.title_data)
        self.state_active(self.text_data,True) # İlk veri false giderse text olduğunu anlıyor!!!
    def update_file_processing(self,window):
        listbox_id=self.file_id[self.convert_id]
        if self.crypto_type=="AES-256":
            crypto=AESCipher(self.key) # Aes nesnesi oluşturuldu.
        elif self.crypto_type=="Blowfish":
            crypto=BlowfishCipher(self.key) # Blowfish nesnesi oluşturuldu.
        title=crypto.encrypt(self.title_data.get()) # Yeni title'yi şifrele
        text=crypto.encrypt(self.text_data.get(1.0,"end")) # Yeni text'ti şifrele
        con=sql.connect(self.database_name) # Veritabanı bağlantısı oluşturulur.
        db=con.cursor() # İşlem yapabilimek için imleç oluşturuldu.
        sorgu="update data set title='{}', crypto='{}' where id={}" \
                .format(title,text,listbox_id) # Sorgumuz: Yeni veriler ekleniyor.
        db.execute(sorgu) # Sorguyu ekle.
        con.commit() # Sorguyu çalıştır. 
        con.close() # Bağlantıyı kapat.
        self.listing_file(window)
    def delete_file(self,window):
        isYes = askyesno("Delete", "Are You Sure?")
        if isYes==True:
            self.listbox_file.delete(self.convert_id) # Listbox'dan seçili veriyi siler.
            con=sql.connect(self.database_name) # Veritabanı bağlantısı oluşturulur.
            db=con.cursor() # İşlem yapabilimek için imleç oluşturuldu.
            sorgu="delete from data where id='{}'".format(self.file_id[self.convert_id]) # Sorgumuz:id listesinden veriyi sil.
            db.execute(sorgu) # Sorguyu ekle.
            con.commit() # Sorguyu çalıştır. 
            con.close() # Bağlantıyı kapat.
            self.listing_file(window) # Listeleme fonksiyonun baştan çalıştırır.
        else:
            showinfo("Delete","Data Is Not Deleted!!!")
    def listing_file(self,window):
        """
            Listeleme butonuna basıldığında listbox'da veri seçilmiş olmaz bu yüzden butonları aktif veya disabled yap.
            .grid(): Tabloya yerleştirme yapıyor.
            anchor: Label içindeki veriyi ortalamaya yarıyor.
        """
        self.state_active(self.add_buton) # Listele butonuna basıldığında ekleme butonunu aktif et.
        self.state_disabled(self.update_buton) # Listele butonuna basıldığında düzenleme butonunu disable et.
        self.state_disabled(self.delete_buton) # Listele butonuna basıldığında silme butonunu disable et.
        yscroll = Scrollbar(window, orient="vertical") # Scrollbar oluşturuluyor.
        yscroll.grid(row=1, column=20, rowspan=30, sticky="nsw") # Scrolbarı tabloya yerleştiriyoruz.
        self.listbox_file=Listbox(window,width=47,height=27,yscrollcommand=yscroll.set)
        self.listbox_config(self.listbox_file) # Listbox ayarları yapılıyor.
        self.listbox_file.grid(row=1,column=0,columnspan=20,rowspan=25,sticky="nsew",padx=(6,0))
        """
            Tkinter'de halledildi. Fakat global olması için config.py ye eklendi.
            self.listbox_file['activestyle']="none"
        """
        yscroll["command"] = self.listbox_file.yview # Scrollbar bağlanıyor.
        self.take_data() # Verilerin veritabanından çekilip çözüldüğü fonksiyon.
        self.title_set=StringVar() # Title_set verinin içini değiştirmek için oluşturuldu.
        Label(window,text="Title",anchor="center").grid(row=1,column=21,columnspan=3)
        self.title_data=Entry(window,width=75,validate="key",textvariable=self.title_set) # Başlıkların tutulacağı Entry.
        self.title_data["validatecommand"]=(self.title_data.register(self.maxlenght),'%P',50,True) # 50 değeri limiti.
        self.title_data.grid(row=1,column=24,columnspan=26) # validate="key" limit koymak için yazıldı.
        Label(window,text="Text",anchor="center").grid(row=2,column=21,columnspan=3)
        self.text_data=Text(window,width=57,height=26,selectbackground="#ed7442") # Verilerin tutulacağı text.
        self.text_data.grid(row=2,column=24,columnspan=26,rowspan=23)
        self.buton_update=Button(window,text="Save",command=lambda:self.update_file_processing(window)) 
        self.buton_update.grid(row=25,column=24,columnspan=13) # Güncelleme butonu düzenlenmiş veri güncellenir.
        self.cancel_buton=Button(window,text="Cancel",command=lambda:self.listing_file(window))
        self.cancel_buton.grid(row=25,column=37,columnspan=13) # Yapılan işlemler iptal edilir.
        self.listbox_file.bind("<<ListboxSelect>>",lambda event:self.listing_data(window))
        self.state_disabled(self.buton_update) # Buton başlangıçta disable edildi çünkü veri seçilmedi.
        self.state_disabled(self.cancel_buton) # Buton başlangıçta disable edildi çünkü veri seçilmedi.
        self.state_disabled(False,self.title_data) # Entry fonksiyonun tanıması için ilk verisi None olarak gönderildi.
        self.state_disabled(self.text_data,True) # Text readonly fonksiyonuna background ile gönderildi.
    def take_data(self):
        self.file_id=[] # Id'leri listede tutuyoruz.
        self.dec_file=[] # Çözülmüş dosyaları atacağımız liste oluşturuldu.
        self.dec_title=[] # Çözülmüş başlıkları atacağımız liste oluşturuldu.
        self.dec_crypto=[] # Çözülmüş verileri atacağımız liste oluşturuldu.
        con=sql.connect(self.database_name) # Veritabanı bağlantısı.
        db=con.cursor() # İşlem yapabilimek için imleç oluşturuldu.
        db.execute("select id,file,title,crypto from data")#fetchone sadece 1 veri çeker.
        encrypt_data=db.fetchall() # Bütün veriler alındı.
        if self.crypto_type=="AES-256":
            crypto=AESCipher(self.key) # Aes nesnesi oluşturuldu.
        elif self.crypto_type=="Blowfish":
            crypto=BlowfishCipher(self.key) # Blowfish nesnesi oluşturuldu.
        con.close() # Bağlantı kapatıldı.
        #print(encrypt_data)
        for i in range(1,len(encrypt_data)):
            self.file_id.append(encrypt_data[i][0]) # Idleri listeye atıyoruz.
            temp=crypto.decrypt(encrypt_data[i][1]) # Şifre çözme işlemi gerçekleştirildi.
            self.dec_file.append(temp) # Dosya listeye atıldı.
            self.dec_title.append(crypto.decrypt(encrypt_data[i][2])) # Başlık listeye atıldı.
            self.dec_crypto.append(crypto.decrypt(encrypt_data[i][3])) # Veri listeye atıldı.
            self.listbox_file.insert("end",temp) # Dosya Listbox'a eklendi.
    def listing_data(self,window):
        if len(self.listbox_file.get("anchor"))>0:
            self.state_active(self.update_buton) # Update butonu aktif olur.
            self.state_active(self.delete_buton) # Delete butonu aktif olur.
            self.state_disabled(self.buton_update) # Listboxdan yeni veri seçildiğinde butonun disable olması gerekiyor.
            self.state_disabled(self.cancel_buton) # Listboxdan yeni veri seçildiğinde butonun disable olması gerekiyor.
            self.state_disabled(False,self.title_data) # Entry fonksiyonun tanıması için ilk verisi None olarak gönderildi.
            try:
                """
                    Bazen curselection yani listbox seçili olmayı bırakabiliyor bu yüzden try except bloğu var!!!
                """
                self.convert_id=self.listbox_file.curselection()[0] # Listbox'daki seçili veriyi alır.
            except:
                """
                    Seçim bazen kaybolabiliyor. Oluşan hatayı çözmek için title Entry'sini içinde son veri alınıp tekrar
                    seçim yapılır.
                """
                i=0
                for deger in self.dec_file: # en son seçili veriyi listbox üzerinde baştan seçer.
                    if deger==self.title_data.get():
                        self.listbox_file.select_set(i)
                    i+=1
            finally:
                self.state_active(self.text_data,True) # Text'in içine veri yazılmadan önce aktif edilmeli. 
                self.title_set.set(self.dec_title[self.convert_id]) # title_set'in içine dec_title'deki listboxdaki seçili veri eklenir.
                self.text_data.delete('1.0', "end") # text_data'nın içi boşaltılır.
                self.text_data.insert("end",self.dec_crypto[self.convert_id]) # text_data'ya veri ekleriz.
                self.state_disabled(self.text_data,True) # Text readonly fonksiyonuna background ile gönderildi.