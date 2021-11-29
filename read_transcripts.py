# recommended by samar: logistic regression, support vector classifier -> vectorize
# not recommended by samar: naive bayes -> bag of words
# X: features (len, word count, etc.)
# y: price goes up or down (rise:1, fall:0)
# dimensionality reduction, PCA (use PCA to get fixed dimension output) or pad with 0
# does it matter if every vector has the same vs different features
# create list of pdf strings for tfidf (the features should be the same)

import PyPDF2

"""note- download via: pip install PyPDF2"""


class ReadTranscripts:
    def __init__(self):
        pass

    def read_transcript_to_python(self, file_name):
        # opens pdf file and creates an object
        pdf = open(file_name, mode='rb')

        # reads pdf file and creates an object
        transcript = PyPDF2.PdfFileReader(pdf)

        # loops through pages and prints them
        for page_num in range(transcript.numPages):
            page = transcript.getPage(page_num)
            print(page.extractText())


"""example output shown below"""
docs = ReadTranscripts()
docs.read_transcript_to_python('Apple Inc. (AAPL) CEO Tim Cook on Q3 2021 Results - Earnings Call Transcript | '
                                   'Seeking Alpha.pdf')
