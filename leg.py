from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize, word_tokenize 
english_stop_words = stopwords.words('english')
import pickle

word_weights = {}
data = []
def remove_stop_words(corpus):
    removed_stop_words = []
    for review in corpus.split():
        removed_stop_words.append(
            ' '.join([word for word in review.split() 
                    if word not in english_stop_words])
        )
    print('Done stop words')
    return ' '.join(removed_stop_words)

def get_lemmatized_text(text):
    lemmatizer = WordNetLemmatizer()
    #return [' '.join([lemmatizer.lemmatize(word) for word in review.split()]) for review in corpus]
    sp = [lemmatizer.lemmatize(word) for word in text.split()]
    return sp

def extractWords():
    ne = open('finaldict.txt','w+')
    with open('down.txt','r') as f:
        p = f.readlines()
        for a in p:
            if '**' in a:
                co = a.find('**')
                print(a[co+2:])
                ne.write(a[co+2:]+'\n')
    ne.close()

def preprocess(para):
    term = remove_stop_words(para)
    term = get_lemmatized_text(term)
    return term

def dictcreator():
    sav = open('dict.pkl','wb')
    for a in english_stop_words:
        word_weights[a.strip()]=1
    with open('finaldict.txt','r') as f:
        p = f.readlines()
        key = word_weights.keys()
        for a in p:
            if a not in key:
                word_weights[a.strip()]=1.5
    print(word_weights)
    pickle.dump(word_weights,sav)

def vec(text):
    
    for i in sent_tokenize(text):
        temp = []
        for j in word_tokenize(i): 
            temp.append(j.lower()) 
        data.append(temp) 

    return vec

def retSimilarity(text1,text2):

    sim = 0
    with open('dict.pkl','rb') as f:
        d = pickle.load(f)
    t1 = preprocess(text1)
    t2 = preprocess(text2)
    for a in t1:
        if (a in t2) and (d[a]==1.5):
            sim+=1.5
        elif (a in t2) and (d[a]==1):
            sim+=1
    similarity =  sim/max(len(text1),len(text2))
    print(similarity)
    return similarity


#extractWords()
#dictcreator()
#vec("There is nothing in the provisions of the Act to indicate that the framers of the Act ever intended that a joint Hindu family should be considered to be one single unit as Bhumidhar. Had they envisaged any such contingency they were bound to indicate how succession was to be governed in the case of a joint Hindu family. On the other hand the only inference which can be drawn from Section 175 of the Act is that a group of persons holding bhumidhari interest were to hold the same as tenants in common.")

retSimilarity("There is nothing in the provisions of the Act to indicate that the framers of the Act ever intended that a joint Hindu family should be considered to be one single unit as Bhumidhar. Had they envisaged any such contingency they were bound to indicate how succession was to be governed in the case of a joint Hindu family. On the other hand the only inference which can be drawn from Section 175 of the Act is that a group of persons holding bhumidhari interest were to hold the same as tenants in common.","In view of my observation herein above, present suit is CS No.08/14 Pg 3 of 4 M/s.. H.M. Dayal & Co. Vs. M/s. Nitya Electrical Contractors Pvt. Ltd hereby decreed for a sum of Rs.1,00,000/­ with cost of the suit. However, plaintiff has not claimed any interest on the suit amount in the plaint, still the court considering that transaction between the parties is commercial one, hence plaintiff is awarded interest @ 6% per annum (simple) from the date of filing of the suit till realization of the decreetal amount, on the suit amount.")