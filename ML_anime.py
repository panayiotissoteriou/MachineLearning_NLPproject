import csv
import pandas as pd
import string
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
nltk.download('stopwords')


#file_2 = pd.read_csv('/Users/panayiotissoteriou/Desktop/UvA_VUA/machine_learning/project/anime_edit.csv', delimiter = ",", encoding='utf-8')
file_2 = pd.read_csv('/Users/panayiotissoteriou/Desktop/UvA_VUA/machine_learning/project/anime.csv', delimiter = ",", encoding='utf-8')

description = file_2.iloc[:,8]
empty_count = 0
non_empty_count = 0
punctuation = [',', '.', '!', ';', ':', '?', '(', ')', "'", "-", '...']
words_dict = dict()
for line in description:
    if len(str(line)) == 3:
        empty_count += 1
        pass
    else:
        non_empty_count += 1

        words_list = line.split(' ')

        for word in words_list:
            word = word.lower()
            word = word.translate(word.maketrans('', '', string.punctuation))

            if word not in words_dict.keys():
                words_dict[str(word)] = 1
            else:
                words_dict[str(word)] += 1

#print(words_dict)

# sorts them
marklist = sorted(words_dict.items(), key=lambda x:x[1])
sortdict = dict(marklist)
#print(sortdict)
print(string.punctuation)

print('original')
print(len(sortdict))



#HISTOGRAM w/ stopwords
# plt.bar(list(sortdict.keys()), sortdict.values(), color='g')
# plt.ylim(top=500) #ymax is your value
#
# plt.show()

word_list = list(sortdict.keys())
for word in word_list:
    if word in stop:
        word_list.remove(word)
print('the' in word_list)

print('no stopwords')
print(len(stop))
print(int(len(sortdict.keys())) - int(len(word_list)))

print('empty descriptions')
print(empty_count)

print('non empty descriptions')
print(non_empty_count)
new_dict = {}
for w in word_list:
    new_dict[w] = sortdict[w]


#print(new_dict)

#plt.bar(list(new_dict.keys()), new_dict.values(), color='g')
#plt.ylim(top=500) #ymax is your value

#plt.show()


