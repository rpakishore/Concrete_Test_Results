from typing import Union
from conc_test_report.c_mcelhanney import McElhanney
from conc_test_report.c_kontur import Kontur
from pathlib import Path
from conc_test_report.definitions import ReportData
import pandas as pd

class Company:
    def __init__(self, textblob: str, filepath: str, company: str):
        self.textblob = textblob
        self.filepath = Path(str(filepath))
        self.filename = self.filepath.name
        self.data = ReportData(filepath=self.filepath, company=company)
        self.company = company
    
    def __repr__(self) -> str:
        textblob = self.textblob
        filepath = self.filepath
        return f"Company({filepath=},{textblob=})"

    def __str__(self) -> str:
        return f"Company parser for {self.company} ({self.filename})"

    def _log_error(self, code, desc) -> None:
        """Collects the specified errorcode and description into the `errors` attribute
        """
        df = pd.DataFrame([[code, desc]],columns = ['Error Code', 'Description'])
        self.data.errors = pd.concat([self.data.errors, df], ignore_index=True)

def identify_company_from_text(pdf_text: str, filepath: str) -> Union[McElhanney, Kontur, None]:
    """ Checks to see which of the defined company specific identifiers match
        to identify the company
    """
    if 'mcelhanney' in pdf_text.split('\n')[0].lower():
        return McElhanney(pdf_text, filepath)
    elif 'kontur' in pdf_text.split('\n')[0].lower():
        return Kontur(pdf_text, filepath)
    return None