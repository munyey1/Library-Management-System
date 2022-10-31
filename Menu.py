'''
Code written by F128784
Last updated: 16/12/2021

This program is responsible intertwining the functions of the system, and representing them
for the user, by creating a GUI. The GUI will have a main menu, where it should display what
functions are available for the user. There will also be pages for each of the functions,
search window, book checkout window, book recommend window, and a book return window, where
each page will show the appropriate widgets for the user.
'''

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import *
from booksearch import search
from bookcheckout import bookcheckout
from bookreturn import bookreturn
from bookrecommend import bookrecommend

def main_window(container):
    '''Main menu of the system which presents four options for the user, search, checkout
        return, recommend, and quit.

    :param container: the main tk window that holds the GUI
    '''
    for widget in container.winfo_children():
        widget.destroy()
    #Destroy what was previously in the window to load the main menu widgets.

    frame = ttk.Frame(container)

    tk.Label(frame, height=3, width=30, text="Library Management System", font = "consolas 16 underline").grid(column=0, row=0, columnspan = 2)

    tk.Button(
        frame,
        height=4, width=30,
        text="Search", relief=tk.RIDGE,
        command = lambda: search_window(container)).grid(column=0, row=2)
    #Search button, which when pressed enters the search_window fucntion, passing the tk window

    tk.Button(
        frame,
        height=4, width=30,
        text="Checkout", relief=tk.RIDGE,
        command = lambda: checkout_window(container)).grid(column=1, row=2)
    #Checkout button, enters the checkout_window when pressed.

    tk.Button(
        frame,
        height=4, width=30,
        text="Return", relief=tk.RIDGE,
        command = lambda: return_window(container)).grid(column=0, row=3)
    #Return button, enters return_window when pressed.

    tk.Button(
        frame,
        height=4, width=30,
        text="Recommend", relief=tk.RIDGE,
        command = lambda: recommend_window(container)).grid(column=1, row=3)
    #Recommend button, enters recommend_window when pressed.

    tk.Button(
        frame,
        height = 2, width = 20,
        text = "Quit", relief = tk.RIDGE,
        command = lambda: close_window(container)).grid(column = 0, row = 4, columnspan = 2)
    #Quit button, enters close_window when pressed.

    for widget in frame.winfo_children():
        widget.grid(padx = 5, pady = 15)

    frame.grid(row = 0, column = 0)

def search_window(container):
    '''The search window that displays the result of a search through the
        database. A back button, entry for the search term and a Treeview
        are used in this window.

    :param container: the main tk window that holds the GUI
    '''
    for widget in container.winfo_children():
        widget.destroy()

    frame = ttk.Frame(container)

    msgframe = ttk.Frame(container)

    columns = ('Book ID', 'Genre', 'Name', 'Author', 'Purchase Date','Member ID')
    tree = ttk.Treeview(frame, columns=columns, show='headings', height = 16, style = "Treeview.Heading")
    style = ttk.Style()
    style.configure("Treeview.Heading", font = "consolas 9", background = "white")
    tree.tag_configure('overdue', foreground="red")
    #Creation of the Treeview to display the records in the database.

    tree.column('Book ID',width = 60)
    tree.column('Genre',width = 100)
    tree.column('Name',width = 260)
    tree.column('Author',width = 200)
    tree.column('Purchase Date', width = 100)
    tree.column('Member ID', width = 80)

    tree.heading('Book ID', text='ID')
    tree.heading('Genre', text='Genre')
    tree.heading('Name', text='Name')
    tree.heading('Author', text='Author')
    tree.heading('Purchase Date', text = 'Purchase Date')
    tree.heading('Member ID', text = 'Member ID')

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.grid(row=0, column=3, rowspan = 3, sticky = tk.N)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=4, rowspan = 3, sticky= tk.NS)
    #The scrollbar for the Treeview

    tk.Button(
        frame,
        text = "Back",
        relief = tk.RIDGE, font = "consolas 15",
        command = lambda: main_window(container)).grid(row = 0, column = 0, sticky = tk.NW)
    #Back button, enters the main_windo when pressed.

    tk.Label(
        frame,
        height = 2,
        text = "Book Search",
        font = "consolas 15 underline").grid(row = 0, column = 1)

    tk.Label(frame, text="Search: ").grid(column=0, row=1, rowspan = 2,sticky=tk.NW)
    e = tk.Entry(frame, width=20)
    e.focus()
    e.grid(column=1, row=1, sticky=tk.N)
    #Entry for the search term given from the user.

    tk.Button(
        frame,
        text = "Enter",
        relief = tk.RIDGE,
        command = lambda: checksearch(tree,e.get(), message_label)).grid(column = 2, row = 1, sticky = tk.N)
    #Enter button to enter the checksearch function to process the searching.

    tk.Label(frame, text = 'Red: Overdue').grid(column = 0, row = 2)
    message_label = tk.Label(msgframe, text = "")

    for widget in frame.winfo_children():
        widget.grid(padx = 5, pady = 10)

    for widget in msgframe.winfo_children():
        widget.grid(padx = 5, pady = 10)

    frame.grid(column = 0, row = 0)
    msgframe.grid(column = 0, row = 1, sticky = tk.W)

def checksearch(tree, term, label):
    '''This function checks if the search term is valid and proceeds to continue
        with this given information. Update the tree if the term is valid, and
        show an error message if not.

    :param tree: tkinter Treeview
    :param term: string given by user
    :type term: str
    :param label: tkinter Label
    :return: enter the updatetree function if the search term is valid,
             update the label if not
    '''
    label.configure(text='')#Reset the label before working on it
    if term.isspace() or len(term) != 0:#If no term has been entered
        if type(search(term)) is list:
            updatetree(tree, search(term))
        else:
            label.configure(text = "There are no options for that search term.", fg = 'red')
    else:
        updatetree(tree, recordslist)
        #Update the tree with all the records.

def updatetree(tree, list):
    '''Update the Treeview to display the records by inserting the
        records into the Treeview.

    :param tree: tkinter Treeview
    :param list: a resulting list given by the search function in booksearch
    :type list: list[list[str]]
    :return: the Treeview will have the updated values
    '''
    for i in tree.get_children():
        tree.delete(i)
    #Delete the previous data in the Treeview to display new data.
    for i in list:
        if i[5] != '0' and dates(i[0]) >= 60:
            #Check if overdue, highlight red if it is
            tree.insert('', tk.END, values = i, tags = ('overdue',))
        else:
            tree.insert('', tk.END, values = i)

def checkout_window(container):
    '''Checkout window that handles the checkout function of the system.
        This window has two entries one for member id and book id, and
        a listbox that holds the messages for each checkout.

    :param container:the main tk window that holds the GUI
    '''
    for widget in container.winfo_children():
        widget.destroy()

    frame = ttk.Frame(container)

    listbox = tk.Listbox(
        frame,
        height = 16,
        width = 85,
        selectmode = 'browse')
    listbox.grid(row = 0, column = 5, rowspan = 3)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=6, rowspan=3, sticky=tk.NS)
    #Creation of a listbox and scroll bar, to hold the messages from the checkout function.

    tk.Button(
        frame,
        text="Back",
        relief=tk.RIDGE, font="consolas 15",
        command=lambda: main_window(container)).grid(row=0, column=0, sticky=tk.NW)

    tk.Label(
        frame,
        height=2,
        text="Book Checkout",
        font="consolas 15 underline").grid(row=0, column=1, columnspan = 2)

    tk.Label(frame, text="Book ID: ").grid(column=0, row=1, rowspan=2, sticky=tk.NW)
    e = tk.Entry(frame, width=20)
    e.focus()
    e.grid(column=1, row=1, sticky=tk.N)

    tk.Label(frame, text="Member ID: ").grid(column=0, row=2, rowspan=2, sticky=tk.NW)
    s = tk.Entry(frame, width=20)
    s.grid(column=1, row=2, sticky=tk.N)
    #Entries for the book id and member id.

    tk.Button(
        frame,
        text="Enter",
        relief=tk.RIDGE,
        command = lambda: checkout(e.get(),s.get(), listbox)
        ).grid(column=3, row=1, sticky=tk.N)
    #Enter the checkout function when pressed, passing the member id, book id and listbox as parameters.

    for widget in frame.winfo_children():
        widget.grid(pady = 5, padx = 5)

    frame.grid(row = 0, column = 0, sticky = tk.NW)

def checkout(bookid, memid, listbox):
    '''Checks are made before entering the checkout_message function. If the user
        enters a list of book id's for one member, this function handles that and
        displays the correct messages.

        If a list is entered for the book id, split the string into a list and for
        each book id, apply the bookcheckout function.

    :param bookid: the book id given by the user
    :type bookid: str
    :param memid: the member id given by the user
    :type memid: str
    :param listbox: tkinter Listbox
    '''
    if len(bookid) != 0 or len(memid) != 0:
        if "," in bookid:
            checkoutlist = bookid.split(',')#Create a list of book id's
            for id in checkoutlist:
                msg, colour, overduebooks = bookcheckout(id, memid)
                checkout_message(msg,colour,overduebooks,listbox,memid)
        else:
            msg,colour,overduebooks = bookcheckout(bookid, memid)
            checkout_message(msg,colour,overduebooks,listbox,memid)

def checkout_message(msg,colour,overduebooks,listbox,memid):
    '''Display certain messages in the listbox depending on what has been passed
        into the function.

    :param msg: a message representing the result of the checkout
    :type msg: str
    :param colour: a boolean value representing what colour should the text be
    :type colour: bool
    :param overduebooks: a list of overduebooks that the member might have
    :type overduebooks:  list[list[str]]
    :param listbox: tkinter Listbox
    :param memid: memebr id given by user
    :type memid: str
    '''
    listbox.insert('end', msg)
    if colour:
        listbox.itemconfig('end', fg='green')
    else:
        listbox.itemconfig('end', fg='red')
    if overduebooks:
    #Display error messages if there are any overdue books that the member has
        for book in overduebooks:
            overduemsg = str("Member %s is loaning Book %s for %d days.\n" % (memid, book[0], dates(book[0])))
            listbox.insert('end', overduemsg)
            listbox.itemconfig('end', fg='red')

def return_window(container):
    '''Return window, displaying the appropriate widgets for the function.
        This window holds an entry box and a listbox.

    :param container: the main tk window that holds the GUI
    '''
    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)

    listbox = tk.Listbox(
        frame,
        height = 16,
        width = 88,
        selectmode = 'browse')
    listbox.grid(row = 0, column = 3, rowspan = 3, sticky = tk.NE)
    #Creation of the listbox

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=4, rowspan=3, sticky=tk.NS)
    #Creation of the scrollbar and attach to the listbox

    tk.Button(
        frame,
        text="Back",
        relief=tk.RIDGE, font="consolas 15",
        command=lambda: main_window(container)).grid(row=0, column=0, sticky=tk.NW)

    tk.Label(
        frame,
        height=2,
        text="Book Return",
        font="consolas 15 underline").grid(row=0, column=1)

    tk.Label(frame, text="Book ID: ").grid(column=0, row=1, sticky = tk.N)
    e = tk.Entry(frame, width=20)
    e.focus()
    e.grid(column=1, row=1, sticky=tk.N)

    tk.Button(
        frame,
        text="Enter",
        relief=tk.RIDGE,
        command = lambda: returnbookcheck(e.get(),listbox)
        ).grid(column=2, row=1, sticky=tk.NE)
    #Enter button which when pressed, enters the returnbook function, passing the entry and the listbox

    for widget in frame.winfo_children():
        widget.grid(pady = 5, padx = 5)

    frame.grid(row = 0, column = 0, sticky = tk.NW)

def returnbookcheck(bookid,listbox):
    '''Apply the bookreturn function on the book id, and insert the returned message
        into the listbox.

        As bookreturn returns three values, we can decide what colour the text
        takes, representing if the message is an error message or a successful one.
        This function can also help the user by allowing them to return multiple items
        at once.

    :param bookid: book id given by the user
    :type bookid: str
    :param listbox: tkiner Listebox
    '''
    if bookid.isspace() or len(bookid) == 0:
        return
    if "," in bookid:
    #If the user wants to return a list of books
        returnlist = bookid.split(',')
        for book in returnlist:
        #Apply the function or all of the books in the list.
            msg, colour, overduemsg = bookreturn(book)
            returnbook(listbox,msg,colour,overduemsg)
    else:
        msg,colour,overduemsg = bookreturn(bookid)
        returnbook(listbox,msg,colour,overduemsg)

def returnbook(listbox,msg,colour,overduemsg):
    listbox.insert('end', msg)
    if colour:
        listbox.itemconfig('end', fg = 'green')
        #Make the label green if colour == True(i.e. a successful return).
        if overduemsg != '':
            listbox.insert('end', overduemsg)
            listbox.itemconfig('end', fg = 'red')
            #If the member is returning an overdue book, colour text red.
    else:
        listbox.itemconfig('end', fg='red')
        #If colour == False(i.e. not successful).

def recommend_window(container):
    '''Recommend window that showcases the recommend function on a matplotlib
        graph. The matplotlib bar graph represents the most popular books in
        the database, or the recommended books for a member.

    :param container: the main tk window that holds the GUI
    '''
    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)

    frame.grid_columnconfigure(0, weight=1)

    books = list(bookcount)
    count = list(bookcount.values())
    #These are the initial x and y values for the bar graph to showcase, which is the count of books in the log.

    fig = plt.figure(figsize=(8,4))
    canvas = FigureCanvasTkAgg(fig, master = frame)

    draw_graph(canvas,fig,books,count)
    #Call the draw_graph function that takes in the figure, the canvas and the x and y values.

    tk.Button(
        frame,
        text="Back",
        relief=tk.RIDGE, font="consolas 15",
        command=lambda: main_window(container)).grid(row=0, column=0, sticky=tk.NW)

    tk.Label(
        frame,
        height=2,
        text="Recommend Books",
        font="consolas 15 underline").grid(row=0, column=1)

    tk.Label(frame, text="Member ID: ").grid(column=0, row=1, sticky=tk.N)
    e = tk.Entry(frame, width=20)
    e.focus()
    e.grid(column=1, row=1, sticky=tk.N)

    tk.Button(
        frame,
        text="Enter",
        relief=tk.RIDGE,
        command = lambda: recommendbook(e.get(),canvas,fig,msg)
    ).grid(column=2, row=1, sticky=tk.NE)

    msg = tk.Label(frame, text = '', wraplength = 100)
    msg.grid(row = 1, column = 1)

    for widget in frame.winfo_children():
        widget.grid(pady=5, padx=5)

    canvas.get_tk_widget().grid(row = 0, column = 3, rowspan = 3, sticky = tk.NE)
    frame.grid(row=0, column=0, sticky=tk.NW)

def recommendbook(memberid,canvas,fig,label):
    '''Given the member id show their recommended books in a bar graph which also
        shows their popularity.

        Apply the bookrecommend function on the member id and gather its result.
        Depending on the result, the bar chart will show their recommended books.

    :param memberid: member id given by the user
    :type memberid: str
    :param canvas: a canvas which allows matplotlib graphs to be shown on a tkinter
                    GUI
    :param fig: matplotlib figure that holds the graph to be drawn
    '''
    label.configure(text = '')
    if memberid == '':
        #If the enter button is pressed without a member id, show the counts of all books.
        draw_graph(canvas,fig,list(bookcount),list(bookcount.values()))
        return
    result = bookrecommend(memberid)
    #Store the return list as result.
    if type(result) == str:
        label.configure(text = result, fg = 'red')
        return
    else:
        if result != False:
            if len(result) >= 3 or len(result) <= 10:
                draw_graph(canvas, fig, list(result), list(result.values()))
            elif len(result) > 10:
                draw_graph(canvas, fig, list(result)[-10:], list(result.values())[-10:])
                # Only recommend a certain amount, nothing over 10 books.
            else:
                draw_graph(canvas, fig, list(sortedbookcount)[-6:], list(sortedbookcount.values())[-6:])
        else:
            draw_graph(canvas, fig, list(sortedbookcount)[-6:], list(sortedbookcount.values())[-6:])
            # If the member is new recommend the top 6 most popular books.

def draw_graph(canvas,fig,books,count):
    '''The function that handles the drawing of the bar chart whenever
        the user enters a member id.

    :param canvas: matplotlib Canvas that allows to be shown in tkinter
    :param fig: matplotlib figure that holds the graph to be drawn
    :param books: the books that are being recommended, this will be used
                  as the x-axis of the graph
    :type books: list[str]
    :param count: the count of the given books in the log file, shows their
                  popularity
    :type count: list[int]
    '''
    fig.clear()
    bargraph = fig.add_subplot(1, 1, 1)
    bargraph.bar(books, count)
    bargraph.set_xlabel("Book ID's")
    fig.autofmt_xdate(rotation=45)
    bargraph.set_ylabel("Count")
    bargraph.set_title("We Recommend These Books")
    canvas.draw()
    #Redraw the graph, once any new data is passed to it.

def create_main_window():
    '''This is the creation of the main tkinter window, that sets the
        whole GUI beforehand.

    '''
    window = tk.Tk()
    window.title("Library Management System")
    window.geometry("1250x450")
    window.option_add("*font", 'consolas 13')
    window.grid_columnconfigure(0, weight = 1)

    window.protocol("WM_DELETE_WINDOW", disable_event)
    #Disable the exit button, as the matplotlib graph causes problems with closing

    main_window(window)

    window.mainloop()

def disable_event():
    #Dummy function for the window exit button
    pass

def close_window(window):
    #To prevent the program to continue when the user closes the window with a canvas drawn
    window.quit()
    window.destroy()

create_main_window()