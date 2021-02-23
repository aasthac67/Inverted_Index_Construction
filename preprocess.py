import nltk
import unidecode
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from prettytable import PrettyTable

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

table = PrettyTable()
table.field_names = ["File Name","Initial Words","Tokenization","Normalization","Stemming","Lemmatization","Stopword Removal","Unique Words"]
total_table = PrettyTable()
total_table.field_names = ["Corpus","Initial Words","Tokenization","Normalization","Stemming","Lemmatization","Stopword Removal"]

t_words = set()
t_token = set()
t_norm = set()
t_stem = set()
t_lemm = set()
t_stop = set()
t_uni = set()

file1 = open('animal_list.txt','r')
lines = file1.readlines()
for line in lines:
	animal = line.strip()
	f1 = open(f'corpus/{animal}.txt','r')
	text = f1.read()
	print(animal)

	total_words = text.split(' ')
	for word in total_words:
		t_words.add(word)

	#-------- Tokenization --------
	tokens = nltk.word_tokenize(text)

	f2 = open(f'tokenization/{animal}.txt','w')
	for i in tokens:
		t_token.add(i)
		f2.write(i)
		f2.write(" ")


	#-------- Normalization --------

	#remove periods
	newlist = []
	for i in tokens:
		newlist.append(i.replace('.',''))

	#take only alphanumeric tokens
	newlist = [i for i in newlist if i.isalpha()]

	#lowercase
	newlist = [i.lower() for i in newlist]

	#remove hyphens 
	newlist1 = []
	for i in newlist:
		newlist1.append(i.replace('-',''))

	#removing accents
	normalize = [unidecode.unidecode(i) for i in newlist1]
	f3 = open(f'normalize/{animal}.txt','w')
	for i in normalize:
		t_norm.add(i)
		f3.write(i)
		f3.write(" ")


	# ----------- Stemming -------------
	stemmer = PorterStemmer()
	stemming = [stemmer.stem(i) for i in normalize]
	f4 = open(f'stemming/{animal}.txt','w')
	for i in stemming:
		t_stem.add(i)
		f4.write(i)
		f4.write(" ")


	# ----------- Lemmatization ---------
	lemmatizer = WordNetLemmatizer() 
	lemmatize = [lemmatizer.lemmatize(i) for i in normalize]
	f5 = open(f'lemmatize/{animal}.txt','w')
	for i in lemmatize:
		t_lemm.add(i)
		f5.write(i)
		f5.write(" ")


	# --------- Stopword Removal --------
	preprocessed = [i for i in lemmatize if i not in stopwords.words('english')]

	# --------- Unique Words ------------
	s = set()
	for token in preprocessed:
		t_stop.add(token)
		s.add(token)
	final = list(s)
	final.sort()

	f6 = open(f'preprocessed_data/{animal}.txt','w')
	for i in final:
		f6.write(i)
		f6.write(" ")

	table.add_row([animal,len(total_words),len(tokens),len(normalize),len(stemming),len(lemmatize),len(preprocessed),len(final)])

print("Table wrt 100 Documents:")
print(table)
total_table.add_row(["List of 100 Animals",len(t_words),len(t_token),len(t_norm),len(t_stem),len(t_lemm),len(t_stop)])
print("Table wrt the whole Corpus:")
print(total_table)