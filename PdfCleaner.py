import pdfplumber
import gensim

class PdfCleaner:

  def __init__ (self,pdf_file_path):
    self.__path__ = pdf_file_path
    text = ""
    with pdfplumber.open(self.__path__) as pdf:
      for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = text + str(page.extract_text())
    self.__original_text__ = text
    self.__cleaned_text__= self.clean_stopwords_punctuation()

  def lenBeforeClean(self):
    return len(self.__original_text__)

  def lenAfterClean(self):
    return len(self.__cleaned_text__)

  def print_originalText(self):
    print(self.__original_text__)

  def print_cleanedText(self):
    print(self.__cleaned_text__)

  def clean_stopwords_punctuation(self):
    from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
    cleaned_text = remove_stopwords(self.__original_text__)
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~©'''
    for ele in cleaned_text:
      if ele in punc:
         cleaned_text = cleaned_text.replace(ele, "")
    return cleaned_text



# Test
# origin = PdfCleaner("APPL_2016Q3.pdf")
# cleaned_text=origin.clean_stopwords_punctuation()
# origin.print_cleanedText()
# print(origin.lenBeforeClean())
# print(origin.lenAfterClean())