from tkinter import *
from tkinter import messagebox

from db import Database

db = Database("store.db")


def populate_list():
    component_list.delete(0, END)
    for row in db.fetch():
        component_list.insert(END, row)


def add_item():
    if component_text.get() == "" or customer_text.get() == "" or retailer_text.get() == "" or price_text.get() == "":
        messagebox.showerror("Required Fields", "Please include all fields")
        return
    db.insert(component_text.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    component_list.delete(0, END)
    component_list.insert(END, (component_text.get(),
                                customer_text.get(), retailer_text.get(), price_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = component_list.curselection()[0]
        selected_item = component_list.get(index)

        component_entry.delete(0, END)
        component_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], component_text.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    populate_list()


def clear_text():
    component_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)


# Create window object
app = Tk()

# Component
component_text = StringVar()
component_label = Label(app, text="Component Name", font=("bold", 14), pady=20)
component_label.grid(row=0, column=0, sticky=W)
component_entry = Entry(app, textvariable=component_text)
component_entry.grid(row=0, column=1)

# Customer
customer_text = StringVar()
customer_label = Label(app, text="Customer", font=("bold", 14))
customer_label.grid(row=0, column=2, sticky=W)
customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)

# Retailer
retailer_text = StringVar()
retailer_label = Label(app, text="Retailer", font=("bold", 14))
retailer_label.grid(row=1, column=0, sticky=W)
retailer_entry = Entry(app, textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)

# Price
price_text = StringVar()
price_label = Label(app, text="Price", font=("bold", 14))
price_label.grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)

# Component list (Listbox)
component_list = Listbox(app, height=8, width=80, border=0, bg="#f0f0ed")
component_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# Scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, rowspan=6, column=3, sticky=NS)

# Set scrollbar to listbox
component_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=component_list.yview)

# Bind select
component_list.bind("<<ListboxSelect>>", select_item)

# Buttons
add_btn = Button(app, text="Add Component", width=15, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text="Remove Component",
                    width=15, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text="Update Component",
                    width=15, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text="Clear Input", width=15, command=clear_text)
clear_btn.grid(row=2, column=3)


app.title("Component Manager")
app.geometry("700x350")

# Populate data
populate_list()

# Start program
app.mainloop()
