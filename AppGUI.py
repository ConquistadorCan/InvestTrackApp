from tkinter import *
from tkinter.ttk import Treeview
from tkinter import simpledialog
from DataBaseHandler import *
from tkcalendar import Calendar
import os

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('InvestTrackApp')

        canvas = Canvas(self.root, height=1000, width=1000, background='gray12')
        canvas.pack()

        self.createWidgets()

    def createWidgets(self):
        self.createTable()
        self.createAddButton()
        self.createDeleteButton()
        self.createEditButton()
        self.createChooseSaveMenu()
        self.createSaveButton()
        
    def createTable(self):
        tableFrame = Frame(self.root, bg='gainsboro')
        tableFrame.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.88)
        tableFrame.columnconfigure(0, weight=1)
        tableFrame.rowconfigure(0, weight=1)

        self.table = Treeview(tableFrame, column=('platform', 'isim', 'adet', 'değer', 'toplam'), show='headings')
        self.table.column('# 1', anchor=CENTER)
        self.table.heading('# 1', text='Platform')
        self.table.column('# 2', anchor=CENTER)
        self.table.heading('# 2', text='İsim')
        self.table.column('# 3', anchor=CENTER)
        self.table.heading('# 3', text='Adet')
        self.table.column('# 4', anchor=CENTER)
        self.table.heading('# 4', text='Değer')
        self.table.column('# 5', anchor=CENTER)
        self.table.heading('# 5', text='Toplam')
        self.table.grid(sticky='NSEW')

    def createAddButton(self):
        addButtonFrame = Frame(self.root, bg='gainsboro')
        addButtonFrame.place(relx=0.02, rely=0.05, relwidth=0.07, relheight=0.03)
        addButtonFrame.columnconfigure(0, weight=1)
        addButtonFrame.rowconfigure(0, weight=1)

        addButton = Button(addButtonFrame, text='EKLE', command=self.add)
        addButton.grid(sticky='NSEW')

    def createDeleteButton(self):
        deleteButtonFrame = Frame(self.root, bg='gainsboro')
        deleteButtonFrame.place(relx=0.11, rely=0.05, relwidth=0.07, relheight=0.03)
        deleteButtonFrame.columnconfigure(0, weight=1)
        deleteButtonFrame.rowconfigure(0, weight=1)

        deleteButton = Button(deleteButtonFrame, text='SİL', command=self.delete)
        deleteButton.grid(sticky='NSEW')
    
    def createEditButton(self):
        editButtonFrame = Frame(self.root, bg='gainsboro')
        editButtonFrame.place(relx=0.2, rely=0.05, relwidth=0.07, relheight=0.03)
        editButtonFrame.columnconfigure(0, weight=1)
        editButtonFrame.rowconfigure(0,weight=1)

        editButton = Button(editButtonFrame, text='DÜZENLE', command=self.edit)
        editButton.grid(sticky='NSEW')

    def createSaveButton(self):
        saveButtonFrame = Frame(self.root, bg='gainsboro')
        saveButtonFrame.place(relx=0.91, rely=0.05, relwidth=0.07, relheight=0.03)
        saveButtonFrame.columnconfigure(0, weight=1)
        saveButtonFrame.rowconfigure(0, weight=1)

        saveButton = Button(saveButtonFrame, text='KAYDET', command=self.save)
        saveButton.grid(sticky='NSEW')

    def createChooseSaveMenu(self):
        self.clearTable()
        def selectDatabase(*args):
            self.clearTable()
            selected_date = valueInside.get()
            if selected_date == 'Tarih Yok':
                return
            selected_date = 'date' + selected_date.replace('-', '_')
            self.getData(selected_date)

        chooseSaveMenuFrame = Frame(self.root, bg='gainsboro')
        chooseSaveMenuFrame.place(relx=0.75, rely=0.05, relwidth=0.14, relheight=0.03)
        chooseSaveMenuFrame.columnconfigure(0, weight=1)
        chooseSaveMenuFrame.rowconfigure(0, weight=1)

        databaseFiles = self.getDatabaseFiles()
        showDatabaseFiles = [file.split('e')[-1].replace('_', '-').split('.')[0] for file in databaseFiles]

        valueInside = StringVar(self.root)

        if showDatabaseFiles:
            valueInside.set(showDatabaseFiles[-1])
            self.getData(databaseFiles[-1])
        else:
            valueInside.set('Tarih Seçin')
            showDatabaseFiles = ['Tarih Yok']

        valueInside.trace('w', selectDatabase)
        saveMenu = OptionMenu(chooseSaveMenuFrame, valueInside, *showDatabaseFiles)
        saveMenu.grid(sticky='NSEW')

    def getData(self, databaseName):
        database = DatabaseHandler(databaseName)
        rows = database.fetchAllItems()
        for row in rows:
            self.table.insert('', END, values=row)
        database.closeConnection()
        self.totalRow()

    def add(self):
        platform = simpledialog.askstring('Platform', 'Platform adını girin:', parent=self.root)
        name = simpledialog.askstring('İsim', 'İsim girin:', parent=self.root)
        quantity = simpledialog.askfloat('Adet', 'Adeti girin:', parent=self.root)
        value = simpledialog.askfloat('Değer', 'Değeri girin:', parent=self.root)
        total = round(quantity * value, 2)
        self.table.insert('', END, values=(platform, name, quantity, value, total))
        self.totalRow()
        
    def delete(self):
        selectedItem = self.table.focus()
        if selectedItem:
            self.table.delete(selectedItem)
        self.totalRow()

    def edit(self):
        selectedItem = self.table.focus()
        if selectedItem:
            platform, name, quantity, value, total = self.table.item(selectedItem)['values']
            platform = simpledialog.askstring('Platform', 'Platform adını girin:', parent=self.root, initialvalue=platform)
            name = simpledialog.askstring('İsim', 'İsim girin:', parent=self.root, initialvalue=name)
            quantity = simpledialog.askfloat('Adet', 'Adeti girin:', parent=self.root, initialvalue=quantity)
            value = simpledialog.askfloat('Değer', 'Değeri girin:', parent=self.root, initialvalue=value)
            total = round(quantity * value, 2)
            self.table.item(selectedItem, values=[platform, name, quantity, value, total])
        self.totalRow()

    def save(self):
        date = self.chooseDateWithDatePicker()
        database = DatabaseHandler(date)
        # First, clear all existing items in the database
        database.deleteData()
        database.commit()

        inserted_items = set() # Create a set to keep track of items that have been inserted

        existing_items = database.fetchAllItems()
        for existing_item in existing_items:
            inserted_items.add(existing_item)

        for item in self.table.get_children():
            platform, name, quantity, value, total = self.table.item(item)['values']
            if (platform, name, quantity, value, total) not in inserted_items:
                database.insertItem(platform, name, quantity, value, total)
                inserted_items.add((platform, name, quantity, value, total))
        
        self.createChooseSaveMenu()
        database.closeConnection()

    def chooseDateWithDatePicker(self):
        datePicker = Toplevel(self.root)
        cal = Calendar(datePicker, selectmode='day', date_pattern='y-mm-dd')
        cal.pack(pady=20)

        selected_date = None

        def onDateSelected():
            nonlocal selected_date
            selected_date = cal.get_date()
            selected_date = selected_date.replace('-', '_')
            selected_date = 'date{}'.format(selected_date)
            datePicker.destroy()

        ok_button = Button(datePicker, text="Tamam", command=onDateSelected)
        ok_button.pack()

        datePicker.wait_window(datePicker)

        return selected_date

    def totalRow(self):
        self.deleteTotalRow()

        items = self.table.get_children()

        if not items:
            return

        allAssets = 0
        for item in items:
            platform, name, quantity, value, total = self.table.item(item)['values']
            allAssets += float(total)
        self.table.insert('', END, values=(' ', ' ', ' ', ' ', allAssets))

    def deleteTotalRow(self):
        items = self.table.get_children()
        for item in items:
            if self.table.item(item)['values'][0] == ' ':
                self.table.delete(item)


    def getDatabaseFiles(self):
        databaseFiles = []
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.db'):
                    fileName = os.path.join(root, file)
                    fileName = fileName.split("\\")[-1].split(".db")[0]
                    databaseFiles.append(fileName)
        return databaseFiles
    
    def clearTable(self):
        for item in self.table.get_children():
            self.table.delete(item)