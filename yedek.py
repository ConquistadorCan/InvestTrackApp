from tkinter import *
from tkinter.ttk import Treeview
from tkinter import simpledialog
import sqlite3



def bilgileriGetir():
    conn = sqlite3.connect('veritabanı.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS veritabanı (platform TEXT, isim TEXT, adet REAL, değer REAL, toplam REAL)')
    conn.commit()

    cursor.execute('SELECT * FROM veritabanı')
    rows = cursor.fetchall()
    for row in rows:
        liste.insert('', END, values=(row[0], row[1], row[2], row[3], row[4]))
    conn.close()

def ekle():
    platform = simpledialog.askstring('Platform', 'Platform adını girin:', parent=kök)
    isim = simpledialog.askstring('İsim', 'İsim girin:', parent=kök)
    adet = simpledialog.askfloat('Adet', 'Adeti girin:', parent=kök)
    değer = simpledialog.askfloat('Değer', 'Değeri girin:', parent=kök)
    toplam = adet * değer
    liste.insert('', END, values=(platform, isim, adet, değer, toplam))

def sil():
    seçili_item = liste.focus()
    if seçili_item:
        liste.delete(seçili_item)

def kaydet():
    conn = sqlite3.connect('veritabanı.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS veritabanı (platform TEXT, isim TEXT, adet REAL, değer REAL, toplam REAL)')
    cursor.execute('DELETE FROM veritabanı')
    conn.commit()

    # Create a set to keep track of items that have been inserted
    inserted_items = set()

    # Fetch existing items from the database and add them to the set
    cursor.execute('SELECT platform, isim, adet, değer, toplam FROM veritabanı')
    existing_items = cursor.fetchall()
    for existing_item in existing_items:
        inserted_items.add(existing_item)

    for item in liste.get_children():
        platform, isim, adet, değer, toplam = liste.item(item)['values']

        # Check if the item already exists in the set (previously inserted)
        if (platform, isim, adet, değer, toplam) not in inserted_items:
            # Item doesn't exist in the set, so insert it
            cursor.execute('INSERT INTO veritabanı (platform, isim, adet, değer, toplam) VALUES (?, ?, ?, ?, ?)',
                           (platform, isim, adet, değer, toplam))
            # Add the inserted item to the set
            inserted_items.add((platform, isim, adet, değer, toplam))

    conn.commit()
    conn.close()



kök = Tk()
kök.title('Varlık Saklama')

canvas = Canvas(kök, height=1000, width=1000, background='gray12')
canvas.pack()



frame_liste = Frame(kök, bg='gainsboro')
frame_liste.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.88)
frame_liste.columnconfigure(0, weight=1)
frame_liste.rowconfigure(0, weight=1)

liste = Treeview(frame_liste, column=('platform', 'isim', 'adet', 'değer', 'toplam'), show='headings')
liste.column('# 1',anchor=CENTER)
liste.heading('# 1', text= 'Platform')
liste.column('# 2',anchor=CENTER)
liste.heading('# 2', text= 'İsim')
liste.column('# 3', anchor= CENTER)
liste.heading('# 3', text= 'Adet')
liste.column('# 4', anchor= CENTER)
liste.heading('# 4', text='Değer')
liste.column('# 5', anchor= CENTER)
liste.heading('# 5', text='Toplam')
liste.grid(sticky='NSEW')


bilgileriGetir()


frame_ekleme_butonu = Frame(kök, bg='gainsboro')
frame_ekleme_butonu.place(relx=0.02, rely=0.05, relwidth=0.07, relheight=0.03)
frame_ekleme_butonu.columnconfigure(0, weight=1)
frame_ekleme_butonu.rowconfigure(0, weight=1)

ekleme_butonu = Button(frame_ekleme_butonu, text='EKLE', command=ekle)
ekleme_butonu.grid(sticky='NSEW')



frame_silme_butonu = Frame(kök, bg='gainsboro')
frame_silme_butonu.place(relx=0.11, rely=0.05, relwidth=0.07, relheight=0.03)
frame_silme_butonu.columnconfigure(0, weight=1)
frame_silme_butonu.rowconfigure(0, weight=1)

silme_butonu = Button(frame_silme_butonu, text='SİL', command=sil)
silme_butonu.grid(sticky='NSEW')



frame_kaydet_butonu = Frame(kök, bg='gainsboro')
frame_kaydet_butonu.place(relx=0.2, rely=0.05, relwidth=0.07, relheight=0.03)
frame_kaydet_butonu.columnconfigure(0, weight=1)
frame_kaydet_butonu.rowconfigure(0, weight=1)

kaydet_butonu = Button(frame_kaydet_butonu, text='KAYDET', command=kaydet)
kaydet_butonu.grid(sticky='NSEW')

kök.mainloop()