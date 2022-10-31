'''
Code written by F128784
Last updated: 16/12/2021

This module is responsible for recommending books for a new member or an existing
member. This should be used whenever the user wishes to recommend books to a
library member.

'''
from database import *

def bookrecommend(memberid):
    '''Given a member id, return a list of the most popular books in the last genre the
        member has read.

        If the member is new, return the 6 most popular books. Else, go through the loglist
        and append books that have already been read by the user. Then get the last genre
        that the user has read, and append that to the genre list, where a genre dictionary
        is made that holds the books in most popular order.

    :param memberID: member id given by the user
    :type memberID: str
    :return: dictionary that represents the most popular books in a certain genre,
             False if the member is new
    :rtype: bool or dictionary
    '''
    readbooks = []
    genredict = {}
    genrelist = []
    if any(char.isdigit() for char in memberid) or len(memberid) != 4:
    # Check if member id is invalid(i.e has any digits or does not have length 4).
        return "Member-ID %s is invalid." % (memberid)

    for log in loglist:
    #Append all the books that the user has read, else return False.
        if log[3] == memberid:
            readbooks.append(log[0])
    if not readbooks:
        return(False)

    lastbook = readbooks[-1][0]
    for record in recordslist:
        if record[0] == lastbook:
        #Get the last book and find its genre
            genre = record[1]
            break

    for record in recordslist:
    #Get all the books of that genre
        if record[1] == genre:
            genrelist.append(record[0])

    for book in genrelist:
        for key,value in sortedbookcount.items():
        #Append the book in the genre list wtih its count value in a new dictionary.
            if book == key:
                genredict[key] = value
                break
    genredict = dict(sorted(genredict.items(),key=lambda item: item[1]))
    #Sort the genre dictionary
    return(genredict)

if __name__ == "__main__":
    print(bookrecommend("qmqw"))
    print(bookrecommend("fd"))