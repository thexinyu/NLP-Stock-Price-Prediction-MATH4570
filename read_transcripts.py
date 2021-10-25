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
