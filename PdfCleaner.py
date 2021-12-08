import pdfplumber
import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
import re

class PdfCleaner:

  def __init__ (self,pdf_file_path):
   """ Use provided path to get and read pdf file """
    self.__path__ = pdf_file_path
    text = ""
    with pdfplumber.open(self.__path__) as pdf:
      for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = text + str(page.extract_text())
    self.__original_text__ = text
    self.__cleaned_text__= self.clean_stopwords_punctuation()
    self.__nonum_text__ = self.clean_nums()

  def lenBeforeClean(self):
    """ Returns length of pdf file text before cleaning """
    return len(self.__original_text__)

  def lenAfterClean(self):
    """ Returns length of pdf file text after cleaning """
    return len(self.__cleaned_text__)

  def print_originalText(self):
    """ Prints out original text before cleaning"""
    print(self.__original_text__)

  def print_cleanedText(self):
    """ Prints out cleaned tet """
    print(self.__cleaned_text__)

  def clean_stopwords_punctuation(self):
    """ Removes stopwords from text"""
    cleaned_text = remove_stopwords(self.__original_text__)
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~©'''
    for ele in cleaned_text:
      if ele in punc:
         cleaned_text = cleaned_text.replace(ele, "")
    return cleaned_text

  def clean_nums(self):
    """ Removes numbers from text """
    nonum_text = re.sub(r'\d+', '', self.__cleaned_text__)
    return nonum_text
