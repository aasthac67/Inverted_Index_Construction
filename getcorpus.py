import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')

file1 = open('animal_list.txt','r')
lines = file1.readlines()
for line in lines:
    animal = line.strip()
    page_py = wiki_wiki.page(animal)
    if(page_py.exists()):
        f1 = open(f'corpus/{animal}.txt','w')
        f1.write(page_py.text)
        print(animal)