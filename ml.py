import csv
import pandas as pd
import string
from copy import copy

# text learning stuff
import nltk
from nltk.stem import PorterStemmer
# in command line run: python -m nltk.downloader stopwords
from nltk.corpus import stopwords
porter = PorterStemmer()
stop = set(stopwords.words('english'))

"""
Need 5 outputfiles in the same folder: 
inwords.txt,    : informative words (>= 10 found)
exwords.txt,    : excluded words
stopwords.txt,  : stopwords from nltk package
ingenres.txt,   : included genres (>= 100 found)
exgenres.txt    : excluded genres
"""

# try out some words to see how porterstemmer stems words
def test_stem():
    # print(porter.stem("office"))
    # print(porter.stem("official"))
    # print(porter.stem("series"))
    # print(porter.stem("serial"))
    # print(porter.stem("serious"))
    pass

# get a dict of informative words with frequency
# also a list with description in proper index order order
def get_words(description,length_index):
    # Punctuation to be removed in description
    # note: nltk has something similar
    punctuation = [',', '.', '!', ';', ':', '?', '(', ')', "\'", "-", '...',"\"", "\'s","s\'"]
    words_dict = dict()
    # list with the same length as #rows in csv
    wordlist = [[] for _ in range(length_index)]
    # Go through descriptions per row
    for line in enumerate(description):
        index = line[0]
        line = line[1]
        # checks something? tag panyiotis
        if len(str(line)) == 3:
            pass
        else:
  
            words_list = line.split(' ')

            for word in words_list:
                word = word.lower()
                word = word.translate(word.maketrans('', '', string.punctuation))
                word = porter.stem(word)
                wordlist[index].append(word)
                if word not in words_dict.keys():
                    words_dict[str(word)] = 1
                else:
                    words_dict[str(word)] += 1

    #print(words_dict)

    # sorts them
    marklist = sorted(words_dict.items(), key=lambda x:x[1])
    sortdict = dict(marklist)

    # dictionary with excluded words
    exdict = {}
    # dictionary with stopwords
    stopdict = {}
    keys = list(sortdict.keys())
    for entry in keys:
        word_t = 10
        # move the word to stopdict if its a stopword
        if entry in stop:
            stopdict[entry] = copy(sortdict[entry])
            sortdict.pop(entry)
        # move the word to exdict if the word frequency is less than word_t(hreshold)
        elif sortdict[entry] < word_t:
            exdict[entry] = copy(sortdict[entry])
            sortdict.pop(entry)
    # write to wordfiles
    # these files are not used anywhere else, they are moreso for reviewing
    with open("inwords.txt", "w") as o:
        try:
            for entry in sortdict.keys():
                x = str(entry) +": "+ str(sortdict[entry]) + "\n"
                # print(x)
                o.write(x)
        except:
            pass
    # print("---------------------")
    with open("exwords.txt", "w") as o:
        for entry in exdict.keys():
            try:
                x =str(entry) +": "+ str(exdict[entry]) + "\n"
                # print(x)
                o.write(x)

            except:
                pass
    # print("---------------------")
    with open("stopwords.txt", "w") as o:
        for entry in stopdict.keys():
            x = str(entry) +": "+ str(stopdict[entry]) + "\n"
            # print(x)
            o.write(x)

    return sortdict,wordlist


# get a dict of genres that are present in more than 100 entries
# Still incomplete e.g. "based on a manga" is still included with ~3000 entries
def getgenres(genres, length_index):
    genredict = {}
    # list of lists with length of entries
    # keeps track of genres with in order of the scv file
    genrelist = [[] for _ in range(length_index)]

    for entry in enumerate(genres):
        index = entry[0]
        entry = entry[1]
        # genrecell is a stringed list, not a list type
        # Might need to be more generalized when looking at other datasets
        entry = list(entry.strip('][').split(', '))
        # Goes through each genre of the current serie/entry
        for genre in entry:
            genre = genre.strip('\'')
            if genre in genredict:
                genredict[genre] += 1
            else:
                genredict[genre] = 1
            genrelist[index].append(genre)
    
    keys = list(genredict.keys())
    exgenres = {}
    # filter genres
    for entry in keys:
        # treshold for how many times a genre needs to ahve appeared
        genre_t = 100
        # moves genre to excluded genres
        if genredict[entry] <= genre_t:
            exgenres[entry] = copy(genredict[entry])
            genredict.pop(entry)
    # print(genredict)
    # writes to genre txt files, not used anywhere else moreso for review
    with open("ingenres.txt", "w") as o:
        try:
            for entry in genredict.keys():
                x = str(entry) +": "+ str(genredict[entry]) + "\n"
                # print(x)
                o.write(x)
        except:
            pass
    
    with open("exgenres.txt", "w") as o:
        try:
            for entry in exgenres.keys():
                x = str(entry) +": "+ str(exgenres[entry]) + "\n"
                # print(x)
                o.write(x)
        except:
            pass
    
    #note: multiple seasons with the same genres might become problematic

    return genredict,genrelist

# give each genre words with predictive qualities
def word_to_genre(worddict, wordlist, genredict,genrelist,length_index):
    informative_words = worddict.keys()
    genre_wordq = copy(genredict)

    # create a dict with the relevant genres as keys
    # genre_wordq(uantity)
    for key in genre_wordq.keys():
        genre_wordq[key] = {}

    # genrelist and wordlist have the same indices for series
    for index in range(length_index):
        description = wordlist[index]
        genres = genrelist[index]
        # go through all genres of current series
        for genre in genres:
            # Check if current genre is relevant
            if genre in genredict.keys():
                # check for all words in description
                for word in description:
                    # check if word is informative
                    if word in informative_words:
                        # check if word has been found before for the current genre
                        if word not in genre_wordq[genre].keys():
                            genre_wordq[genre][word] = 1
                        else:
                            genre_wordq[genre][word] += 1
    # print genre and its associated word quantity
    for key in genre_wordq.keys():
        print("---------------------------")
        print(key)
        print(genre_wordq[key])


# give each word genre weights; 
def genre_to_word(worddict, genres):
    pass


if __name__ == '__main__':
    file_2 = pd.read_csv('anime.csv', delimiter = ",", encoding='utf-8')
    description = file_2.iloc[:,8]
    genres = file_2.iloc[:,10]

    length_index = len(genres)

    # counts and filters genres
    genredict,genrelist = getgenres(genres,length_index)

    # counts and filters words 
    worddict,wordlist = get_words(description,length_index)
    
    word_to_genre(worddict, wordlist, genredict, genrelist, length_index)
    # genretoword()