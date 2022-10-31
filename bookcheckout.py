'''
Code written by F128784
Last updated: 16/12/2021

This module is responsible for checking out a book for a member to loan.
This program will return many messages for the user as there must be many
validation checks to be made. This program should be expected to be used
with an integer for the book id and a valid member id.

'''

from database import *

def bookcheckout(bookid, memberid):
    '''Returns a series of messages and data, each corresponding with the result
        of a book checkout.

        Some validation checks are made before iterating through the recordslist
        to find the given book and updating its member id attribute in the
        database, then logging the checkout to the logfile.

    :param bookid: book id given by user
    :param memberid: member id given by user
    :type bookid: str
    :type memberid: str
    :return: a string which corresponds to the result, a bool which indicates
             an error/unsuccessful message, a list which has standing overdue
             books loaned by the user
    :rtype: str, bool, list[list[str]]
    '''
    overduebooks = []
    if any(char.isdigit() for char in memberid) or len(memberid) != 4:
        #Check if member id is invalid(i.e has any digits or does not have length 4).
        return"Member-ID %s is invalid."%(memberid),False,overduebooks
    for record in recordslist:
        if record[5] == memberid:
            #Check if the member has any standing overdue books to return, and append to a list.
            if dates(record[0]) >= 60:
                overduebooks.append(record[:-1])

    if any(char.isdigit() for char in bookid):
        #Check id bookid is valid
        if int(bookid) < len(recordslist) and int(bookid) > -1:
            #Check if the book id is valid.
            for record in recordslist:
                if record[0] == bookid:
                #Iterate through recordslist to find the book
                    if record[5] == "0":
                        #If the book is not loaned already, update the database and logfile
                        record[5] = memberid
                        append_log(memberid, bookid)
                        update_db()
                        return"Checkout of book %s was successful."%(bookid),True,overduebooks
                    else:
                        return"Book %s is still on loan."%(bookid),False,overduebooks
        else:
            return"Book-ID %s is invalid."%(bookid),False,overduebooks
    else:
        return "Book-ID %s is invalid." % (bookid), False, overduebooks

if __name__ == "__main__":
    print(bookcheckout("24","coml"))
    print(bookcheckout("fn","fdm3kds"))