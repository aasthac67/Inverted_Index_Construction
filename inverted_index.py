import nltk

class Node:
	def __init__(self,val,nxt=None):
		self.data=val
		self.next=nxt

class LinkedList:
	def __init__(self):
		self.head=None

	def insertSorted(self,x):
		newnode=Node(x)
		if self.head is None:
			newnode.next=self.head
			self.head=newnode
			return 
		elif self.head.data >= newnode.data:
			newnode.next=self.head
			self.head=newnode
			return
		else:
			curr=self.head
			while curr.next!=None and curr.next.data<newnode.data :
				curr=curr.next
			newnode.next=curr.next
			curr.next=newnode
			return

	def insert(self,x): #to insert at the end of the Linked List
		newnode=Node(x)
		if self.head == None:
			self.head=newnode
		else:
			temp=self.head
			while temp.next!=None:
				temp=temp.next
			temp.next=newnode

	def printlist(self):
		temp=self.head
		s=''
		while temp!=None:
			s+=str(temp.data)+' '
			temp=temp.next
		print(s)

class InvertedIndex:
	def __init__(self,docs):
		self.dict={}
		self.docid={}
		i=1
		for doc in docs:
			self.docid[doc]=i
			i+=1

	def insertTokens(self,tokens,doc):
		for token in tokens:
			if token not in self.dict:
				self.dict[token] = LinkedList()
			self.dict[token].insertSorted(self.docid[doc])

		# for token in tokens:
		# 	temp=self.dict[token].head
		# 	while temp.next!=None:
		# 		if temp.data==temp.next.data:
		# 			new=temp.next.next
		# 			temp.next=None
		# 			temp.next=new
		# 		else:
		# 			temp=temp.next

	def printInvertedIndex(self):
		print(self.dict)

	def andquery(self,posting1,posting2):
		temp=LinkedList()
		n1=posting1.head
		n2=posting2.head
		while n1 and n2:
			if n1.data == n2.data:
				temp.insert(n1.data)
				n1=n1.next
				n2=n2.next
			elif n1.data < n2.data:
				n1=n1.next
			elif n1.data > n2.data:
				n2=n2.next
		# print("AND Query")
		# temp.printlist()
		return temp

	def orquery(self,posting1,posting2):
		temp=LinkedList()
		n1=posting1.head
		n2=posting2.head
		while n1 and n2:
			if n1.data==n2.data:
				temp.insert(n1.data)
				n1=n1.next
				n2=n2.next
			elif n1.data < n2.data:
				temp.insert(n1.data)
				n1=n1.next
			elif n1.data > n2.data:
				temp.insert(n2.data)
				n2=n2.next
		while n1:
			temp.insert(n1.data)
			n1=n1.next
		while n2:
			temp.insert(n2.data)
			n2=n2.next
		return temp

	def notquery(self,posting1):
		temp=LinkedList()
		n1=posting1.head
		l = [1 for i in range(len(self.docid))]
		while n1:
			l[n1.data-1]=0
			n1=n1.next

		for i in range(len(self.docid)):
			if l[i]==1:
				temp.insert(i+1)

		return temp

def main():
	file1 = open('animal_list.txt','r')
	lines = file1.readlines()

	docs = []
	for line in lines:
		animal = line.strip()
		docs.append(animal)

	#creating an inverted index
	inverted = InvertedIndex(docs)

	for line in lines:
		animal = line.strip()
		f1 = open(f'preprocessed_data/{animal}.txt','r')
		text = f1.read().split(' ')
		inverted.insertTokens(text,animal)

	#inverted.andquery(inverted.dict['old'],inverted.dict['family'])
	#inverted.printInvertedIndex()

	query = input("Enter a query:")
	query = nltk.word_tokenize(query)
	query = [i.lower() for i in query]

	#processing the query
	conn_words = []
	token_words = []
	flag=0
	for word in query:
		if word!="and" and word!="or" and word!="not":
			if word not in inverted.dict:
				print("Invalid word: "+ word)
				flag=1
				break
			token_words.append(word)
		else:
			conn_words.append(word)

	# x1=inverted.dict['old']
	# x2=inverted.dict['family']
	# x3=inverted.dict['africa']
	# print()
	# print("old: ")
	# x1.printlist()
	# print()
	# print("family: ")
	# x2.printlist()
	# print()
	# print("africa: ")
	# x3.printlist()
	# print()

	if flag==0:
		j=0
		word1 = inverted.dict[token_words[j]]
		if j+1<len(token_words):
			word2 = inverted.dict[token_words[j+1]]
		ans=word1
		for i in range(len(conn_words)):
			if conn_words[i] == "and":
				if i+1<len(conn_words) and conn_words[i+1]=="not":
					i+=1
					word2 = inverted.notquery(word2)
				ans = inverted.andquery(word1,word2)
				j+=2
			elif conn_words[i] == "or":
				if i+1<len(conn_words) and conn_words[i+1]=="not":
					i+=1
					word2 = inverted.notquery(word2)
				ans = inverted.orquery(word1,word2)
				j+=2
			elif conn_words[i]=="not":
				ans = inverted.notquery(word1)
				j+=1

			word1 = ans
			if j<len(token_words):
				word2 = inverted.dict[token_words[j]]

		print("Result: ")
		ans.printlist()


if __name__ == "__main__":
	main()