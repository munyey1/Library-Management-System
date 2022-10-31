'''
Code written by F128784
Last updated: 16/12/2021

The module is responsible for handling the database and logfile text files,
where most of the modules will repeatedly use some of the functions or data
structures. This module creates a data structure for each of the text files,
and is in control of writing back to the files, and appending to the files.
Also, there are some functions that handle date difference calculation that
some modules will also use.

'''
from datetime import datetime

recordslist = []
loglist = []
bookcount = {}
sortedbookcount= []
#Data structures used in this system.

f = open("database.txt","r")
for line in f:
    s = line.strip()
    records = s.split(",")
    recordslist.append(records)
f.close()
#Appends all the records into the 'recordslist' list.

l = open("logfile.txt","r")
for i in l:
    a = i.strip()
    log = a.split(",")
    loglist.append(log)
l.close()
#Appends all the logs into the 'loglist' list.

for i in recordslist:
    bookcount[i[0]] = 0
for j in loglist:
    for key in bookcount:
        if j[0] == key:
            bookcount[key] += 1
#Initialise the bookcount dictionary

sortedbookcount = dict(sorted(bookcount.items(), key=lambda item: item[1]))
#Sorts the bookcount dictionary into a new dictionary.

now = datetime.now()
date = now.strftime("%d/%m/%y")
#Date variable holds the current date.

def update_db():
    #Rewrites the database text file to update it with new changes.
    f = open("database.txt","w")
    for i in recordslist:
        f.write(",".join(i) + "\n")
    f.close()
    return

def update_log():
    #Rewrites the logfile to update it with new changes.
    f = open("logfile.txt","w")
    for i in loglist:
        f.write(",".join(i) + "\n")
    f.close()
    return

def append_log(memberid,bookid):
    #Appends to the logfile, this is used when checking out a book.
    f = open("logfile.txt","a")
    f.write("%s,%s,0,%s\n" % (bookid, date, memberid))
    f.close()
    return

def datecheck(d1,d2):
    #Returns the absolute difference of two dates in days.
    d1 = datetime.strptime(d1, "%d/%m/%y")
    d2 = datetime.strptime(d2, "%d/%m/%y")
    return abs((d2-d1).days)

def dates(bookid):
    #Given a book id, look through the loglist and return its length of loan time.
    for i in loglist:
        if i[0] == bookid and i[2] == "0":
            return datecheck(i[1], date)
    return 0

if __name__ == "__main__":
    update_db()
    update_log()
    append_log("coml","33")
    #A new log is expected to appear at the end of the logfile.
    print(datecheck("02/05/21","17/07/21"))
    #Print out the difference between the dates.
    print(dates("33"))
    #Print out the loan date of the book.