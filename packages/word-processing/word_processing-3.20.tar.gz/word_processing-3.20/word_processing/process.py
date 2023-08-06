class Process:
    def __init__(self):
        """
        Word processing class for processing documents ML for training data
        """
    
    def readFiles(self, file_name):
        """
        Args:
            file_name (string): name of a file to read from

        Returns:
            str
        """
        with open(file_name, "r", encoding="utf8") as file:
            line = file.read()
        return line
    
    def removePunctuations(self, string):
        """
        Args:
            string (str): string to work on

        Returns:
            str
        """
        return re.sub(r"[^a-zA-Z0-9]", " ", string)
    
    def convert2Lower(self, string):
        """
        Args:
            file_name (string): name of a file to read from

        Returns:
            str
        """
        return string.lower()
    
    def word2List(self, string):
        """
        Args:
            string (str): string to convert

        Returns:
            list
        """
        return string.split()
    
    def removeEnglishStopwords(self, listfile):
        """
        Args:
            string (list): list to operate on
            stopwords (str): stopwords txt file name

        Returns:
            list
        """
        stopwords = self.readFiles('stopwords.txt').split()
        return [w for w in listfile if w not in stopwords]
