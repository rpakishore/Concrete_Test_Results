from conc_test_report.company import Company
from conc_test_report.definitions import ReportPattern, ReportData

class McElhanney(Company):
    PATTERN = ReportPattern(
        testdata = r".*([A-Z]) *Cylinder *(Lab|Field) *(\d*) *((\d{2}-\w{3})-? *(\d*) *[A-Za-z ]*)?\d{3}.\d *\d{3}.\d( *\d* *(\d*.\d))?",
        specified_str = r"SPECIFIED STRENGTH\s*(\d*)MPa *@ *(\d*) DAYS",
        set_data = r".*SET *NO.(\d*) *SPECIMENS *(\d*) *CAST *(\d{2}-\w{3}-\d{4}) *TRANSPORTED *(\d{2}-\w{3}-\d{4})",
        report_date = r".*Page *1 *of *\d* *(\d{4}.\w{3}.\d*)|(\d*-\w{3}-\d{4})",
        air = r".*AIR *(\d{1,2}.?\d?) *% *SPEC. *(\d{1,2}.?\d?) *± *(\d{1,2}.?\d?)",
        slump = r".*SLUMP *(\d*) *mm *SPEC. *(\d*) *± *(\d*)",
        mix = r".*MIX *NO. *(.*)$",
        load_vol = r"^LOAD *VOL. *(\d*) m3" )

    def __init__(self, textblob: str):
        Company.__init__(self, textblob)
        self.name = "McElhanney"

    def __str__(self) -> str:
        return f"Company parser for McElhanney"

    def extract_data(self) -> ReportData:
        pass