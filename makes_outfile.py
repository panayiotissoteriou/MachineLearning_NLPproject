import pandas as pd

file_2 = pd.read_csv('/Users/panayiotissoteriou/Desktop/UvA_VUA/machine_learning/project/anime.csv', delimiter = ",", encoding='utf-8')
title = file_2.iloc[:,0]         # write the index of the title column
genre = file_2.iloc[:,10]       # write the index of the genre column
description = file_2.iloc[:,8]      #write the index of the description column

title_genre_desc = pd.DataFrame(data=[title, genre, description]).transpose()
title_genre_desc.columns = ['title', 'genre', 'description']

title_genre_desc.to_csv("title_genre_desc.csv")

