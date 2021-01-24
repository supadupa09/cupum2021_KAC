
#!/usr/bin/env python
# coding: utf-8

'''
@authors: 
Dayeen F.R. & Sharma A. S.
'''

# # <center> Literature Topic Co-occurrence and Frequency (LiTCoF) tool </center>
# ### <center>Fazle Rabbi Dayeen, Abhinav S. Sharma, Sybil Derrible</center>
# 

# # Introduction

# This is the code we have used for the paper ***Industrial Ecology for Climate Change Adaptation and Resilience
# literature review using text mining***. And this is the tutorial. By using Jupyter notebook, you can run the code and see the results as you progress: just press `Shift+Enter` on your keyboard to run each cell. 

# **Disclaimer** # This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. If you use this code in your project please consider citing our paper as well (link).
# 
# For further information about the program and downloads, please visit the [CSUN website](https://csun.uic.edu/codes/LiTCoF.html). 

'''
Before running the code:
 1) Create folders: src, data,plots.
 2) Copy the LiTCoF.py and new_stop_words.txt to the 'src' folder.
 3) Copy your data files to 'data' folder. Abstract data needs be in .pkl/ .csv format and co-occurence table needs to be in .csv/.xls/ .xlsx format.
 4) Run. 
'''
# In[13]:

# ## Necessary Libraries

# First of all, importing libraries is absolutely necessary. We are going to use scikit learn and matplotlib for ploting the graphs, gensim for topic modeling and few other useful libraries. We have used Python 3.6.8 throughout the project. If you get *module not found* error, install the modules by running the command ``pip install module-name`` or ``conda install module-name`` in your command prompt.


import nltk
import csv
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import gensim
from gensim import corpora
from gensim.models import Phrases
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure
import os
import seaborn as sns
from IPython.display import Image
sns.set(style='darkgrid')
output_notebook()


# ## Temorary fix for deprecation and overflow error

# Running the code may lead to certain deprecation and overflow errors. The code below a quick workaround to avoid those.

# In[19]:


import warnings
import sys
maxInt = sys.maxsize

# next two lines download the necessery stopwords and punctuation list for the wordlist. They only needed to be run once.
nltk.download('punkt')
nltk.download('stopwords')
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)
# Temporary fix for persistent warnings of an api change between pandas and seaborn.
warnings.filterwarnings('ignore')

#  In our dataset we have three columns


# First column contains the Publication year ('Publication_Year'), second column is the number of publications ('Number') and third column is the abstracts ('Abstracts'). Publication_Year and Number are expected to be integers, while Abstracts for a given year is a single string containing the text for all abstracts in that year. We have our dataset saved as `pickle` format for convenience. If your data is in excel/csv format, you can import it and export it in `pickle` format using pandas.
# 
# Here you need to define the path of your file directory. Change the `path` according to your system. 
# 
# 'base_dir' is the first part of your path upto the folder in which your file is contained.
# 
# 'data_dir' is the name of the folder in which your file is contained. It is advised to give the folder a relevant name as it is used to name all saved figures
# 
# 'file_name' is the name of your file.
# 
# Please also create a folder named 'plots' in your base directory as all figures and plots will be saved there.

# In[15]:

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        return 0
    else:
        return yes_or_no("Please Enter (y/n) ")


while True:
    print("Please copy the file inside the ../data directory \n ")
    if(yes_or_no('Did you copy the file into ../data directory? ')):
        break


file_name = input("Enter the name of your file (only supports .pkl or .csv): ")

base_dir = '../'
data_dir = 'data'
file_name = file_name
file_dir = os.path.join(base_dir, data_dir, file_name)

# ## Word Tokenization

# In this step, we will tokenize our abstracts, remove punctuations and common words such as prepositions, conjunctions and articles called stopwords. Python NLTK module has a built-in library for english stopwords. We have implemented this here.

# In[20]:


stoplist = stopwords.words('english')
abstrct = []
ngram = Phrases()

# creating dataframe
if file_name[-3:] == 'pkl':
    datadf = pd.read_pickle(file_dir) 
if file_name[-3:] == 'csv':
    datadf = pd.read_csv(file_dir)

years = np.array(datadf.Publication_Year)

for i in np.arange(len(datadf.index)):
    texts = [word
                    for word in nltk.word_tokenize(datadf.iloc[i]['Abstracts'].lower())
                    if word not in string.punctuation and word not in stoplist 
                    ]
    abstrct.append(texts)
    ngram.add_vocab([texts])


# ## Removing unimportant words from the bag of words

# There are also some unimportant words which are not included in the NLTK stopword list. So we have created a text file and put those stopwords and clean our data.

# In[21]:


f = open('new_stop_words.txt', 'r') # open file in read mode
new_stopwords_list = f.read()      # copy to a string

stoplist += new_stopwords_list.split()

N = 0 #for phrase


# ## Most frequent words in the collection of abstracts

# One of the easiest markers of the importance of a specific word in an article is the number of times
# it occurs, i.e, its frequency. `ngram_model_counter.most_common(50)` will print out the top 50 most frequent words. Change the value based on your needs. A histogram of the frequency of these top 50 words will be created and saved.

# In[22]:


ngram_model = Word2Vec(ngram[abstrct], size=100)
ngram_model_counter = Counter()
for key in ngram_model.wv.vocab.keys():
    if key not in stoplist:
        if len(key.split("_")) > N:
            ngram_model_counter[key] += ngram_model.wv.vocab[key].count
                      
keyword_list = []
for key, counts in ngram_model_counter.most_common(100):
    print ('{0: <20} {1}'.format(key, counts))
    keyword_list.append(key)
    plt.bar(key, counts)
    plt.xticks(rotation=90)

save_freq = os.path.join(base_dir, 'plots/') + 'term_frequency.png'
print(save_freq)


plt.tight_layout()
plt.savefig(save_freq, dpi=300)
plt.show()

# ## Topic modeling

# Here we are building the dataframe based on most frequent phrases we have generated above and then used scikit learn to do topic modeing. You can change the number of features, number of topics and number of words. For the details, please check `Latent Dirichlet Allocation` section of the paper.

# In[24]:


def show_topics(model, feature_names, top_words):
    df = pd.DataFrame()
    for topic_idx, topic in enumerate(model.components_):
        df["Topic %d:" % topic_idx] = [feature_names[i] for i in topic.argsort()[:-top_words - 1:-1]]
        with open('topics_table.tex','w') as tf:
            tf.write(df.to_latex())
    return df
    

#Number of features to consider (i.e., individual token occurrence frequency)
features = 3000
#Number of topics

topics_num = int(input('Please enter the number of topics you would like to investigate using topic modeling: '))

# Number of topic words
top_words = int(input('Please enter the number of words per topic: '))


vectorized_term_freq = CountVectorizer(max_df=1, min_df=0.02, max_features=features, stop_words='english')
term_freq = vectorized_term_freq.fit_transform(keyword_list)
tf_features = vectorized_term_freq.get_feature_names()

# Run LDA
build_lda = LatentDirichletAllocation(n_components=topics_num, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(term_freq)

topic_table=show_topics(build_lda, tf_features, top_words)
print(topic_table)
table_savepath = os.path.join(base_dir, data_dir) + '/topic_table.csv'
topic_table.to_csv(table_savepath)
print('topic table saved as csv')
# ## Topic modeling using gensim

# In our previous part of the code we have run the topic modeling only on high frequency keywords. However, this part considers all the words in the text of the abstracts for topic modeling. `Gensim` has some really good features to do that.

# First we have built a dictionary of words and a corpus based on the words we have already tokenized.

# In[25]:


dictionary = corpora.Dictionary(abstrct)
corpus = [dictionary.doc2bow(text) for text in abstrct]


# ## Optimal number of topics

# Optimal number of topics can be calculated by using either coherence score (higher the better) or preplexity score (lower the better). Here we have used them as a guide to figure out the optimal number of topics. We checked the scores for 5, 10, 15, 20 and 25. Further values can be added to 'num_of_topics' if required. 
# 
# The scores will be plotted against number of topics and the plots will be saved.

# In[31]:


# Compute Perplexity and Coherence scores
# Good models have low Perplexity and high Coherence scores
num_of_topics = [5, 10, 15, 20, 25, 30, 40, 50]
coherence_scores = []
perplexity_scores = []
for i in num_of_topics:
    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics = i, id2word=dictionary, passes=15)
    cm = gensim.models.coherencemodel.CoherenceModel(model=lda_model, corpus=corpus, coherence='u_mass')
    coherence_scores.append(cm.get_coherence())
    perplexity_scores.append(lda_model.log_perplexity(corpus))


plt.figure()
plt.scatter(num_of_topics, perplexity_scores)
plt.xlabel("Number of Topics")
plt.ylabel("Perplexity score")

Perplexity_fig = os.path.join(base_dir, 'plots/') + 'perplexity_scores.png'

plt.savefig(Perplexity_fig, dpi=300)

plt.figure()
plt.scatter(num_of_topics, coherence_scores)
plt.xlabel("Number of Topics")
plt.ylabel("Coherence score")

Coherence_fig = os.path.join(base_dir, 'plots/') + 'coherence_scores.png'

plt.savefig(Coherence_fig, dpi=300)

plt.show()





# ## Topics from the abstract

# Once we know the value for optimal topics, we will now run the code below to extract the topics from the abstracts

# In[ ]:


ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 20, id2word=dictionary, passes=15)
topics = ldamodel.print_topics(num_words=10)
for topic in topics:
    print(topic)


# The code above prints the topics and their corresponding weights. But we are only interested in learning about the words. So we have removed the weight from the result and output as list of words.

# In[ ]:


gensim_topics = ldamodel.show_topics(num_topics=10, num_words=10,formatted=False)
topics_words = [(topc[0], [wrd[0] for wrd in topc[1]]) for topc in gensim_topics]

#Prints Topics and Words
for topic,words in topics_words:
    print(str(topic)+ "::"+ str(words))
print()



# ## Keyword relative frequency heatmap

# This part of the code plots the scaled frequency of the keywords with time as a 'heatmap'. if use_wordlist is set to True, it plots only the words specified in 'wordlist'. If set to False, it plots the 'word_number' most common words of the text. word_tuples is a list of 3-tuples to be used if the frequency of similar keywords needs to be combined. The first two entries are the words to be combined, and the third entry is the user set name for the combined keyword. 
# 
# The heatmap generated will be saved.

# In[27]:




sns.set(font_scale=2)
wordlist=[]

word_num = input('Please enter the number of terms you would like to plot a relative frequency evolution map for: ')
word_num = int(word_num)
counter = 0

while counter<word_num:
    word = input('Please enter term {}: '.format(counter+1))
    wordlist.append(word)
    counter+=1


use_wordlist = True
word_number = 30
freqdata = []
agg_keys = []

for i in np.arange(len(abstrct)):
    ngram_model = Word2Vec(ngram[[abstrct[i]]], size=100, min_count=1)
    ngram_model_counter = Counter()
    for key in ngram_model.wv.vocab.keys():

        if key not in stoplist:
            if use_wordlist:
                if key in wordlist:
                    
                    if len(key.split("_")) > N:
                        ngram_model_counter[key] += ngram_model.wv.vocab[key].count
            else:
                if len(key.split("_")) > N:
                        ngram_model_counter[key] += ngram_model.wv.vocab[key].count
                
                
    freqdf = pd.DataFrame(ngram_model_counter.most_common(word_number))
    if len(freqdf.index) == 0:
        freqdf[0] = wordlist
        freqdf[1] = 0

    word_tuples=[]
    for w in word_tuples:
        if w[0] in wordlist and w[1] in wordlist:
            f = 0
            drops_w = []
            
            for j in np.arange(len(freqdf.index)):
                if freqdf.iloc[j][0] == w[0] or freqdf.iloc[j][0] == w[1]:
                    
                    f += freqdf.iloc[j][1]
                    drops_w.append(j)
                
            freqdf = freqdf.drop(drops_w, axis = 0)        
            append_data = pd.DataFrame({0:[w[2]],1:[f]})
            freqdf = freqdf.append(append_data,ignore_index=True)
            freqdf = freqdf.reset_index(drop=True)
            
                    
    #Normalizing the frequency by the total number of non-stopword tokens 
    freqdf['prob'] = freqdf[1]/(len(abstrct[i]))

    agg_keys += np.array(freqdf[0]).tolist()
    freqdata.append(freqdf)  
    
    
unqkeys = np.unique(np.array(agg_keys))

heatmap = np.zeros([unqkeys.size,len(freqdata)])

for i in np.arange(years.size):
    
    for j in np.arange(unqkeys.size):
        
        for k in np.arange(len(freqdata[i].index)):
        
            if freqdata[i].iloc[k][0] == unqkeys[j]:
                heatmap[j,i] = freqdata[i].iloc[k]['prob']

fig, ax = plt.subplots(figsize = (40, 26))

ax = sns.heatmap(heatmap, annot = False,linewidths = .9,cmap = 'Oranges' ,cbar_kws={'label': 'Relative Frequency'})
ax.figure.axes[-1].yaxis.label.set_size(35)


ax.grid(False)

ax.set_yticks(np.arange(len(unqkeys))+0.5) #Adding 0.5 offset
ax.set_xticks(np.arange(len(years))+0.5)
ax.set_yticklabels(unqkeys,rotation= 0, fontsize = 50.0)
ax.set_xticklabels(years,rotation='vertical', fontsize = 50.0)
ax.set_xlabel('Publication Year', fontsize = 40.0, labelpad = 40)
ax.set_ylabel('Terms',fontsize = 40.0, labelpad = 5)

plt.show()
image_path =  os.path.join(base_dir, 'plots/') + 'term_evolution_map.png'
fig.savefig(image_path, dpi=300)


# In[ ]:





# ## Keyword co-occurrence

# This part takes an excel file with a co-occurrence matrix with publication numbers, calculates a matrix of co-occurrence coefficients and plots it. The format for the excel file is shown below (a section of the matrix we used in our paper):
# ![image.png](attachment:image.png)

# The element M_ij of the co-occurrence matrix is the number of publications that the keywords i and j both appear in.
# 
# Please replace the 'path' variable with the location of your excel file. You can toggle between log and linear scale for the figure by setting 'log_colorbar' as True or False. 
# 
# The generated co-occurrence matrix figure will be saved.
# 
# **Note:** *If you get "Missing optional dependency 'xlrd'" error, use pip or conda to install xlrd.* 

# In[30]:


def yes_or_no2(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return 1
    elif reply[0] == 'n':
        sys.exit()
    else:
        return yes_or_no2("Please Enter (y/n) ")


while True:
    print("If you would like to generate the co-occurence of the words please copy the .xls or .csv file inside the ../data directory \n ")
    if(yes_or_no2('Did you copy the file into ../data directory? ')):
        break


cooc_file_name = input("What is the name of your file (only supports .xls/.xlsx or .csv): ")

file_name2 = cooc_file_name
path = os.path.join(base_dir, data_dir, file_name2)

cooccurence_df = pd.read_excel(path)
matrix=cooccurence_df.as_matrix()

logcb_yn = yes_or_no("Would you like a logarithmic colorbar for the co-occurrence matrix plot?")

if logcb_yn:
    log_colorbar = True
else:
    log_colorbar = False


#Function for colorbar formatting
def fmt(x, pos):
    a, b = '{:.0e}'.format(x).split('e')
    b = int(b)
    return r'$10^{{{}}}$'.format(b)


keywords = []

num_matrix = np.delete(matrix,0,1)
coeff_matrix = np.zeros([num_matrix.shape[0],num_matrix.shape[1]])


keywords = np.array(cooccurence_df.columns[1:])

for i in np.arange(num_matrix.shape[0]):
    
    for j in np.arange(num_matrix.shape[1]):
        
        coeff_matrix[i,j] = (num_matrix[i,j]**2)/(num_matrix[i,i]*num_matrix[j,j])

fig, ax = plt.subplots(figsize = (20, 20))

mask = np.ones(coeff_matrix.shape, dtype=bool)
np.fill_diagonal(mask, 0)
masked_matrix=np.ma.array(coeff_matrix, mask=~mask)
        

if log_colorbar:
    im = ax.imshow(masked_matrix, norm=colors.LogNorm(), cmap='Blues')
else:
    im = ax.imshow(masked_matrix, cmap = 'Blues')
    
if log_colorbar:
    cbar = fig.colorbar(im, format=ticker.FuncFormatter(fmt), fraction=0.046, pad=0.04)
else:
    cbar = fig.colorbar(im, fraction=0.046, pad=0.04)
      
cbar.ax.set_ylabel('Co-occurence coefficient', rotation=90,labelpad=5, y=0.45, fontsize = 50)

cbar.ax.tick_params(labelsize=40)


    

ax.set_yticks(np.arange(len(keywords)))
ax.set_xticks(np.arange(len(keywords)))
ax.set_yticklabels(keywords, fontsize = 50)
ax.set_xticklabels(keywords, rotation=90, fontsize = 50)
ax.grid(False)


plt.savefig('../plots/co-occurence.png', dpi=300)


# %%
