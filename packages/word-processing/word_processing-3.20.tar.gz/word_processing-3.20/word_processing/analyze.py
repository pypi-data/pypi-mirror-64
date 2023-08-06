class Analyze:
    def __init__(self):
        """
        Word processing class for manipulating documents
        in order to yield a desired data for training
        """
    
    def readFile(self, file_name):
        """
        Args:
            file_name (string): name of a file to read from

        Returns:
            None
        """
        with open(file_name, "r") as file:
            line = file.readline()
            while line:
                print(line)
                line = file.readline()
        file.close()
    
    def __wordList(self,file_name):
        """
        Args:
            file_name (string): name of a file containing words
            to be splitted

        Returns:
            list
        """
        import re
        
        with open(file_name, "r") as file:
            data_list = []
            line = file.readline()
            while line:
                # Remove punctuation characters
                line = re.sub(r"[^a-zA-Z0-9]", " ", line)
                # Remove white space
                line = line.strip()
                if line != '':
                    data_list.extend(line.split())
                line = file.readline()
        file.close()
        return data_list
    
    def __sentenceList(self,file_name):
        """
        Args:
            file_name (string): name of a file containing sentences
            to be splitted

        Returns:
            list
        """
        import re
        
        with open(file_name, "r") as file:
            sentence_list = []
            line = file.readline()
            while line:
                # Split text by ? and .
                line = line.replace('?','.').split('.')
                for i in line:
                    if i != '\n':
                        sentence_list.append(i.strip())
                line = file.readline()
        file.close()
        return sentence_list
    
    def countWords(self,file_name,words='all'):
        """
        Args:
            file_name (string): Name of a file containing words
                to be counted
            words (string) or (list): Word or words to be counted.
                If not specified, the whole words will be counted.

        Returns:
            dictionary with key -> words to be counted
                            values -> counts of words
        """
        wordDict = {}
        wordList = self.__wordList(file_name)
        if words == 'all':
            wordDict['Total words in the text'] = len(wordList)
            return wordDict
        
        if type(words) == list:
            for i in list(words):
                wordDict[i] = wordList.count(i)
            return wordDict
        
        wordDict[words] = wordList.count(words)
        
        return wordDict
    
    def findWords(self,file_name,words):
        """
        Args:
            file_name (string): name of a file containing sentences
                to be splitted
            words (string) or (lists): word(s) to be found

        Returns:
            None
        """
        with open(file_name, "r") as file:
            line = file.readline()
            while line:
                if type(words) == list:
                    for word in words:
                        line = line.replace(word,'\033[91m'+word+'\033[0m')
                else:
                    line = line.replace(words,'\033[91m'+words+'\033[0m')
                print(line)
                line = file.readline()
        file.close()
    
    def sentencesWithWords(self,file_name,words):
        """
        Args:
            file_name (string): name of a file containing sentences
                to be splitted
            words (string) or (lists): word(s) to be found

        Returns:
            None
        """
        sentenceList = self.__sentenceList(file_name)
        for i in range(len(sentenceList)):
            if type(words) == list:
                for word in words:
                    word = self.__wordConversion(sentenceList[i], word)
                    if word in sentenceList[i]:
                        sentenceList[i] = sentenceList[i].replace(word,'\033[91m'+word+'\033[0m')
            else:
                word = self.__wordConversion(sentenceList[i], words)
                sentenceList[i] = sentenceList[i].replace(word,'\033[91m'+word+'\033[0m')
            print(sentenceList[i])
    
    def __wordConversion(self,string, word):
        """
        Takes a word and checks the postion in the string.
        Args:
            string (str)
            words (string)

        Returns:
            str
        """
        if string.startswith(word):
            word = word+' '
        elif string.endswith(word):
            word = ' '+word
        else:
            word = ' '+word+' '
        return word
