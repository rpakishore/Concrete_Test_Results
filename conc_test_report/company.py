from typing import Union
from conc_test_report.c_mcelhanney import McElhanney
from conc_test_report.c_kontur import Kontur

class Company:
    def __init__(self, textblob: str):
        self.textblob = textblob
        #self.name = _identify_company_from_text(textblob)
    
    def __repr__(self) -> str:
        textblob = self.textblob
        return f"Company({textblob=})"

def identify_company_from_text(pdf_text: str) -> Union[McElhanney, Kontur, None]:
    """ Checks to see which of the defined company specific identifiers match
        to identify the company
    """
    if 'mcelhanney' in pdf_text.split('\n')[0].lower():
        return McElhanney(pdf_text)
    elif 'kontur' in pdf_text.split('\n')[0].lower():
        return Kontur(pdf_text)
    return None