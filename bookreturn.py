'''
Code written by F128784
Last updated: 16/12/2021

This module is responsible for the operation of returning a book given
by a member, also returning an overdue message if the member is returning
the book over 60 days. This should be used whenever a user wants to return
a book and an integer is expected to be passed into the functions.

'''

from database import *

def bookreturn(bookid):
    '''Given a book id, return a series of data each corresponding with a result
        of some validation.

        If the book id is invalid return an error message. If the book is valid but
        is already available, return an error message. If the book is available then
        return the book, also checking if the member has returned the book within
        60 days.
    :param bookid: book id given by the user
    :type bookid: str
    :return: a string which corresponds to the result, boolean value which represents
             if the message is an error message or not, and an overdue message if
             the book has been returned over 60 days.
    :rtype: str,bool,str
    '''
    overduemsg = ""
    if any(char.isdigit() for char in bookid):
        if int(bookid) < len(recordslist) and int(bookid) > -1:
        #Check if the book id is valid.
            for record in recordslist:
                if record[0] == bookid:
                    if record[5] == "0":
                    #If the book is already available.
                        return "Book %s is already available, cannot return."%(bookid),False,overduemsg
                    else:
                    #Update the records member id attribute to 0.
                        record[5] = "0"
                        update_db()
                        break
            for log in loglist:
                if log[0] == bookid and log[2] == "0":
                #If return date is 0 of the log of the book, check how long the book has been loaned for.
                    if dates(bookid) >= 60:
                        overduemsg = str("Member %s is returning book %s after %d days." % (log[3],bookid,dates(bookid)))
                    log[2] = date #Updates the return date, to be seen in the loglist.
                    break
            update_log()
            return"Book %s returned successfully."%(bookid),True,overduemsg
        else:
            return"Book-ID %s is invalid."%(bookid),False,overduemsg
    else:
        return "Book-ID %s is invalid." % (bookid), False, overduemsg

if __name__ == "__main__":
    print(bookreturn("36"))
    print(bookreturn("dnf"))