from conc_test_report.company import Company
from conc_test_report.definitions import ReportPattern, ReportData

class Kontur(Company):
    PATTERN = ReportPattern(
        testdata = r"([A-Z]) *Cylinder *(\d*) *(Lab|Field) *((\d{2}-\w{3})|(\w{3}.\d{2})-? *(\d*) *[A-Za-z ]*)?\d{3}.\d *\d{3}.\d( *\d* *(\d*.\d))?",
        specified_str = r"SPECIFIED *STRENGTH: *(\d*) *MPa *@ *(\d*) * DAYS",
        set_data = r"SET *NO.:(\d*) *SPECIMENS: *(\d*) *CAST: *(\d{4}.\w{3}.\d{2}) *TRANSPORTED: *(\d{4}.\w{3}.\d{2})",
        report_date = r".*Page *1 *of *\d* *(\d*.\w{3}.\d*)|(\d*-\w{3}-\d{4})",
        air = r".*AIR: *(\d{1,2}.?\d?) *% *SPEC.: *(\d{1,2}.?\d?) *± *(\d{1,2}.?\d?)",
        slump = r".*SLUMP: *(\d*) *mm *SPEC.: *(\d*) *± *(\d*)",
        mix = r".*MIX *NO.:? *(.*)$",
        load_vol = r"^LOAD *VOL.: *(\d*) m3" )

    def __init__(self, textblob: str):
        Company.__init__(self, textblob)
        self.name = "Kontur Geotechnical Consultants"
        
    def __str__(self) -> str:
        return f"Company parser for Kontur"

    def extract_data(self) -> ReportData:
        pass