# =============================================================================
# Here you go. Use this with the data.txt file. The new_corpus data frame has the 
# responses to questions asked on formspring, as well as, whether that post is considered 
# bullying or not(1 - yes, 0 - no. Corpi is answers only, but with the lemmetization of the 
# word(root of the word) and the removal of stopwords and punctuation. X and y 
# below (in Bag of Words section) is the features and classification, respectively. 
# You will need both for the testing of your classifier. Good luck and let me know 
# if you have any questions.
# corpus: if you want to see only the answers before pre-processing
# new_corpus: For table including both the answers(pre-processed) and manual classification
# X: if you want to see a table with a lot of zeros. These are the features
# y: if you want to only see the manual classification. 
# Note: Bottom comment out section is what I did for the SVM classifier
# =============================================================================

import json
import pandas as pd
import numpy as np


with open('data.txt', encoding='utf-8-sig') as fh:
    data = json.load(fh)

dt = data['dataset']['FORMSPRINGID']

arr = []
    
for i in range(0, len(dt)):
    arr.append(dt[i]['POST'])

#Extract whether post is cyberbullying or not
is_bullying = []
for i in range(0, len(arr)):
    if type(arr[i]) is dict:
        count = 0
        for j in range(0, len(arr[i]['LABELDATA'])):
            if arr[i]['LABELDATA'][j]['ANSWER'].lower() == 'Yes':
                count+=1
        if count >= 2:
            is_bullying.append(1)
        else:
            is_bullying.append(0)
            
for i in range(0, len(arr)):
    if type(arr[i]) is list:
        for j in range(0, len(arr[i])):
            count = 0
            for k in range(0, len(arr[i][j]['LABELDATA'])):
                if arr[i][j]['LABELDATA'][k]['ANSWER'] == 'Yes':
                    if arr[i][j]['LABELDATA'][k]['ANSWER'] == 'Yes':
                        count+=1
            if count >= 2:
                is_bullying.append(1)
            else:
                is_bullying.append(0)
    
# Extract question and answers from file
corpus = []

for i in range(0, len(arr)):
    if type(arr[i]) is dict:
        corpus.append(arr[i]['TEXT'])

for i in range(0, len(arr)):
    if type(arr[i]) is list:
        for j in range(0, len(arr[i])):
            corpus.append(arr[i][j]['TEXT'])
            

# Removing question, leaving only the answer. Then removing 'A:' and '<br>'
for i in range(0, len(corpus)):
    index = corpus[i].find('<br>')
    if index != -1:
        corpus[i] = corpus[i][index:]
    corpus[i] = corpus[i].replace('A:', '').replace('<br>', ' ')

# Creation of pandas dataframe
new_corpus = pd.DataFrame(data=corpus, columns=['Answers'])
new_corpus['bully_post'] = is_bullying

# Loading spacy preprocessing library
nlp = spacy.load('en_core_web_sm')

# function that using lemmetization methods onto array
def lemmetization(arr, doc):
    for token in doc:
        arr.append(token.lemma_)
        
    return arr

# Removal of stop words
def stopwords_removal(arr):
    for word in arr:
        if word in nlp.Defaults.stop_words or word == "-PRON-":
            arr.remove(word)
    
    for i in arr:
        if i == "-PRON-":
            arr.remove(i)
        if i == "i":
            arr.remove(i)
            
    return arr

corpi = []
for i in range(0, len(new_corpus)):
    # Removal of punctuation in dataset
    review = re.sub('[^a-zA-Z]', ' ', new_corpus['Answers'][i]).lower()
    doc = nlp(review)
    
    arr = []
    
    lemmetization(arr, doc)
    stopwords_removal(arr)
    
    arr = " ".join(arr)
    corpi.append(arr)
    
# ----------Creating Bag of Words model----------
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
# matrix of features
X = cv.fit_transform(corpi).toarray()
# dependent variable
y = new_corpus.iloc[:, 1].values 


# =============================================================================
# # ----- SVM Classifier ----- 93%
# # Splitting the dataset into the Training set and Test set
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
# 
# # Fitting SVM to the Training set
# from sklearn.svm import SVC
# classifier = SVC(kernel = 'linear', random_state = 0)
# classifier.fit(X_train, y_train)
# 
# # Predicting the Test set results
# y_pred = classifier.predict(X_test)
# 
# # Making the Confusion Matrix 
# from sklearn.metrics import confusion_matrix
# cm = confusion_matrix(y_test, y_pred)
# =============================================================================
"""