from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
import os
import re
import pandas as pd

positive_socre = []
negative_socre = []
polarity_socre = []
subjectivity_socre = []
avg_sentence_length = []
percentage_of_complex_word = []
fog_index = []
complex_word_count = []
word_count =[]
personal_pronoun = []
avg_word_length = []
syllable_count_per_word = []
average_number_of_words_per_sentence = []
personal_pronoun = []


vol = ['a','e','i','o','u']
personl_pro = ['I','we','my','ours','us']
stop_word = stopwords.words('english') # from nltk packge
stop_w = open('./stop/st.txt','r') # stopWord form blackcoffe
positive = open('./positive-negative-text/positive-words.txt','r')
positive_testing_words = positive.read()
negative = open('./positive-negative-text/negative-words.txt','r')
negative_testing_word = negative.read()

files = os.listdir("./articles") # fetch articles files 

for f in range(len(files)):
    for j in range(len(files)-1):
        if int(files[j].removesuffix('.txt')) >int(files[j+1].removesuffix('.txt')):
            files[j],files[j+1] = files[j+1],files[j]



for file in files:
    articles_text = open(f'./articles/{file}','r',encoding='utf-8')
    article = articles_text.read()
    words = word_tokenize(article)
    sentences = sent_tokenize(article)

    # for word count filter word
    filter_words = []
    for w in words:
        if w not in stop_word:
            if len(w)>1:
                filter_words.append(w)

    word_count.append(len(filter_words))

    # filter word for calculate positive and nagative score
    filter_word2 = []
    for w in words:
        if w not in stop_w:
            if len(w)> 3:
                filter_word2.append(w)

    ps = 0
    ns = 0

    for  i in filter_word2:
        if i in positive_testing_words:
            ps+=1
        elif i in negative_testing_word:
            ns-=1        

    positive_socre.append(ps)
    negative_socre.append(ns*-1)
    polarity_socre.append((ps-(ns*-1))/(ps+(ns*-1)+0.000001))
    subjectivity_socre.append(ps+(ns*-1)/ len(words)+0.000001)
    avg_sentence_length.append(len(words)/len(sentences))

    c_w = []

    for i in filter_words:
        c=0
        for j in range(len(vol)):
            if vol[j] in i :
                c+=1
            elif c>2:
                    c_w.append(i)  
                    continue

    complex_word_count.append(len(c_w))

    percentage_of_complex_word.append(len(c_w)/len(words))

    fog_index.append(0.4*((len(words)/len(sentences))+(len(c_w)/len(words))))

    s_c=0                  #syllable count per word
    

    for i in filter_words:
        if not str(i).endswith('es') or str(i).endswith('ed'):
            for j in range(len(vol)):
                if vol[j] in i :
                    s_c+=1

    syllable_count_per_word.append(s_c)
    average_number_of_words_per_sentence.append(len(words)/len(sentences))

    word_len = 0 

    for w in words:
        word_len+=len(w)

    avg_word_length.append(word_len/len(words))

    c=0
    for i in personl_pro:
        m = re.search(i,article)
        if m is not None:
            c+=1

    personal_pronoun.append(c)

df = pd.read_csv('./input2.csv')

output = pd.DataFrame({'URL_ID':df.URL_ID,'URL':df.URL,'POSITIVE SCORE':positive_socre,'NEGATIVE SCORE':negative_socre,'POLARITY SCORE':polarity_socre,'SUBJECTIVITY SCORE':subjectivity_socre,'AVG SENTENCE LENGTH':avg_sentence_length,'PERCENTAGE OF COMPLEX WORDS':percentage_of_complex_word,'FOG INDEX':fog_index,'AVG NUMBER OF WORDS PER SENTENCE':average_number_of_words_per_sentence,'COMPLEX WORD COUNT':complex_word_count,'WORD COUNT':word_count,'SYLLABLE PER WORD':syllable_count_per_word,'PERSONAL PRONOUNS':personal_pronoun,'AVG WORD LENGTH':avg_word_length})
        
output.to_csv('./output/output.csv',index=False)