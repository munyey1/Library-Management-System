'''
Code written by F128784
Last updated: 16/12/2021

This module is responsible for checking in the database, and returning all the
occurrences of a search term that has been provided. This module should be used
whenever the user wishes to search for something in the database.
'''

from database import *

def search(term):
    '''Return separate lists depending if any search term has been found.

        Iterate through the recordslist to check if the term is present in the name,
        if not, then check through all attributes to check if the term is equal to it.

    :param term: search term given by the user
    :type term: str
    :return: searchlist or recordslist, if no search term present or if user queries all
    :rtype: list[list[str]]
    '''
    found = False
    searchlist = []
    if term.lower() == 'all':
        return(recordslist)
    for record in recordslist:
        if term.lower() in record[2].lower():
            #If the term is present in the books name, append the record.
            searchlist.append(record)
            found = True
            continue
        for att in record:
            if term.lower() == att.lower():
                #If the term is present in any of the attributes, append to the list.
                searchlist.append(record)
                found = True
                break
    if found:
        return(searchlist)
    else:
        return

if __name__ == "__main__":
    print(search("horror"))
    #This should print a series of books with the genre of 'horror'.