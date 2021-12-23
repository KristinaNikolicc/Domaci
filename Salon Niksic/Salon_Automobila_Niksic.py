from tkinter import *
from tkinter import messagebox
from db import Database

db = Database('store_nk.db')


def populate_list(): #za uzimanje podataka
    parts_list.delete(0, END) #da se ne bi vise puta ucitalo ono sto smo pozvali
    for row in db.fetch():
        parts_list.insert(END, row) #dodavanje novih na kraj liste


def add_item():
    if part_text.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Greška', 'Molimo Vas popunite sva polja.')
        return
    db.insert(part_text.get(), customer_text.get(), #dodavanje u bazu podataka
              retailer_text.get(), price_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (part_text.get(), customer_text.get(), #dodavanje u listu
                            retailer_text.get(), price_text.get()))
    clear_text()
    populate_list()


def select_item(event): # da bismo uklonili nesto, moramo da znamo sta selektujemo
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)
            #ovo iznad samo da uzmemo podatke modela koji smo selektovali
        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
            #ovo iznad kad selektujemo nesto da nam se pokaze u input polja da bismo mogli i da izmijenimo
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], part_text.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    populate_list()


def clear_text(): #brise ono smo smo unijeli u input kad god kliknemo na neko dugme
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)


# Create window object
app = Tk()

# Marka
part_text = StringVar()
part_label = Label(app, text='Marka', font=('bold', 14), pady=10, padx=5)
part_label.grid(row=0, column=0, sticky=W) # svaki label i input predstavljaju matrice KxI
part_entry = Entry(app, textvariable=part_text) #input
part_entry.grid(row=0, column=1)
# Model
customer_text = StringVar()
customer_label = Label(app, text='Model', font=('bold', 14))
customer_label.grid(row=0, column=2, sticky=W)
customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)
# Godiste
retailer_text = StringVar()
retailer_label = Label(app, text='Godište', font=('bold', 14), padx=5)
retailer_label.grid(row=1, column=0, sticky=W)
retailer_entry = Entry(app, textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)
# Cijena
price_text = StringVar()
price_label = Label(app, text='Cijena', font=('bold', 14))
price_label.grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)
# Parts List (Listbox)
parts_list = Listbox(app, height=8, width=50, border=0)
parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set) #postavimo scroll pored liste dolje
scrollbar.configure(command=parts_list.yview) #skrola po y osi
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item) #ovo treba za select_item(event)

# Buttons
add_btn = Button(app, text='Dodaj', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Ukloni', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Izmijeni', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Ocisti polja', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)

app.title('Salon Automobila Nikšić')
app.geometry('500x350')
app.configure(bg='#455e87')

# Populate data
populate_list()

# Start program
app.mainloop()

