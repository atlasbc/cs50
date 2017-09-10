import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # initialize instance variables to set type
        self.positives = set()
        self.negatives = set()
        
        # load positive words to memory
        p_file = open(positives, "r")
        for line in p_file:
            # ignore comments and blank lines
            if (line.startswith(';') == False and 
                line.startswith(' ') == False):
                self.positives.add(line.rstrip("\n"))
        p_file.close()  
                
        # load negative words to memory
        n_file = open(negatives, "r")
        for line in n_file:
            # Ignore comments and blank lines
            if (line.startswith(';') == False and 
                line.startswith(' ') == False):
                self.negatives.add(line.rstrip("\n"))
        n_file.close() 

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        # tokenize 
        # Tknzr # 
        # lowers words' letters with preserve_case, 
        # strips @name with strip_handles
        # reduces repeated letters(greater than 3) with reduce_len
        tknzr = nltk.tokenize.TweetTokenizer(preserve_case = False,
                                             strip_handles = True,  
                                             reduce_len = True)
        self.text = text                                     
        tokens = tknzr.tokenize(self.text)
        
        # Analyze tokens
        self.score = 0
        for token in tokens:
            if token in self.positives:
                self.score += 1
            elif token in self.negatives:
                self.score -= 1
        
        return self.score
