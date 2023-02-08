import re, pdfplumber, os
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Union
from conc_test_report.company import identify_company_from_text
from conc_test_report import stru_checks
from conc_test_report.definitions import ReportData


class Report():
    def __init__(self, file: Union[str, Path]):
        self.file = Path(str(file))

        self.pdf_text = extract_text_from_pdf(file)

        self.company = identify_company_from_text(self.pdf_text)
        if self.company:
            report = self.company.extract_data()
            self.report = self.check_errors(report)
        else:
            self.report = ReportData(self.file)
            self._log_error('a',self.pdf_text.split('\n')[0].strip())
            

    def __repr__(self) -> str:
        file = self.file
        return f"Report({file=})"

    def __str__(self) -> str:
        return f"Report Parser Class for {self.file.name}"

    def _log_error(self, code, desc) -> None:
        """Collects the specified errorcode and description into the `errors` attribute
        """
        df = pd.DataFrame([[code, desc]],columns = ['Error Code', 'Description'])
        self.report.errors = pd.concat([self.report.errors, df], ignore_index=True)


    def check_errors(self, x: ReportData) -> ReportData:
        """ Performs custom defined checks on the sample data to confirm if 
            item values are in expected ranges
        """
        # Error Codes for reference
        # 'a':'Template for this company is not defined',
        # 'b': 'Specimen # in extracted PDF does not match scrapped test data from PDF',
        # 'c': 'Slump issue',
        # 'd': 'Air % Issue',
        # 'e': 'Missing Information',
        # 'z': 'Some other error'

        # <!------- Check number of specimens ------->
        if len(x.test_data) != x.specimens:
            self._log_error('b', f"Specimens: {x.specimens}, Avail. Data: {len(x.test_data)}")

        # <!------- Check Air content ------->
        if x.air and x.specified_air:
            options = ["", self.log_error('d', f"Air: {x.air}% > Allow. max:{x.specified_air[1]}%"),
                self.log_error('d', f"Air: {x.air}% < Allow. min:{x.specified_air[0]}%")]
            options[stru_checks.air(x.air, x.specified_air[0], x.specified_air[1])]
        else:
            self._log_error('e', 'Air content data missing.')

        # <!------- Check Slump ------->
        if x.slump and x.specified_slump:
            options = ["", self.log_error('c', f"Slump: {x.slump}mm > Allow. max:{x.specified_slump[1]}mm"),
                self.log_error('c', f"Slump: {x.slump}mm <  Allow. min:{x.specified_slump[0]}mm")]
            options[stru_checks.slump(x.slump, x.specified_slump[0], x.specified_slump[1])]
        else:
            self._log_error('e', 'Slump info missing.')


        x.errors = self.errors
        return x

def extract_text_from_pdf(filepath: Path) -> str:
    """Extracts the contents of a pdf documentand returns the text
    """
    with pdfplumber.open(filepath) as pdf:
        data = [page.extract_text() for page in pdf.pages]
        return "\n".join(data)