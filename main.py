import requests
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary
import os
import random

dictionary=PyDictionary()

class Searching:

    def __init__(self):
        pass

    def sentence_parser(self, word):

        response = requests.get('https://sentence.yourdictionary.com/{}'.format(word))
        soup = BeautifulSoup(response.text, 'lxml')
        raw_sentence_box = soup.find_all('span', {'class': 'sentence-item__text'})
        sentence_box = []

        for sentence in raw_sentence_box[0:5]:
            sentence_box.append(sentence.text)

        return sentence_box

    def definition(self, word):

        raw_result = dictionary.meaning(word)
        return_box = []
        
        try:
            for instances in raw_result:
                return_box.append(instances)
                instance_box = raw_result[instances]
                
                for item in instance_box:
                    return_box.append(f"● {item}")

            return return_box

        except:
            return "error"

class SeeFavorites:

    def __init__(self):
        pass

    def import_favor(self):
        path = './favorites/'
        file_list = os.listdir(path)
        file_list_py = [file for file in file_list if file.endswith('.txt')]
        index = 0

        for title in file_list_py:
            file_list_py[index] = title.split(".")[0]
            index += 1

        return file_list_py

    def specify_favor(self, word):

        try:
            word_file = open(f"favorites/{word}.txt", "rt", encoding= "utf-8")
            word_page = word_file.read()
            print("\n" + word_page)
            word_file.close()
        
        except:
            print("\n해당 단어는 목록에 존재하지 않습니다.\n")

class Quiz:

    def __init__(self):
        pass

    def synonym_parser(self, word):

            response = requests.get('https://thesaurus.yourdictionary.com/{}'.format(word))
            soup = BeautifulSoup(response.text, 'lxml')
            raw_syno_box = soup.find_all('a', {'class': 'synonym-link'})
            syno_box = []

            for syno in raw_syno_box[0:7]:
                syno_box.append(syno.text)

            return syno_box

    def quiz_maker(self, word):
        print("\n아래 단어들은 정답 단어의 유의어입니다.\n정답 단어에 가장 알맞은 단어를 쓰세요.\n")
        for syno in self.synonym_parser(word):
            print(syno)
        
        answer = input("답: ")

        if answer == word:
            return "correct"

        else: 
            return word

class Session(Searching,SeeFavorites, Quiz):

    def __init__(self):
        super().__init__()
    
    def search(self):
        print("\n=========검색=========\n")
        word = input("검색어: ")

        result = self.definition(word)
        if result == "error":
            print("오류 - 검색어를 재확인 해보십시오")

        else:    
            result.append("\n예문\n")
            result += self.sentence_parser(word)

            for i in result: #유저에게 출력
                print(i)

            save_or_not = input("\n단어를 저장하시려면 y를 입력하세요: ")

            if save_or_not == "y":
                f = open(f'favorites\{word}.txt', 'w', encoding="utf-8")
                for ln in result:
                    f.write(ln+"\n")
                f.close()
                print("\n저장 완료\n")

    def favor(self):

        print("\n=========저장한 단어=========\n")

        for word in self.import_favor():
            print(word)

        key = input("\n단어를 선택하십시오: ")
        self.specify_favor(key)

    def quiz(self):
        quiz_box = self.import_favor()
        random.shuffle(quiz_box)
        print("=========퀴즈=========\n")

        for word in quiz_box:
            quiz_result = self.quiz_maker(word)

            if quiz_result == "correct":
                print("\n정답입니다.\n")

            else:
                print(f"\n오답입니다. (정답: {word})\n")

user = Session()

while True:
    
    print("\n=========영영 사전과 퀴즈==========\n")
    menu = input("1. 검색\n2. 찜한 단어 보기\n3. 찜한 단어 퀴즈\n")
    if menu == "1":
        user.search()

    elif menu == "2":
        user.favor()

    elif menu == "3":
        user.quiz()