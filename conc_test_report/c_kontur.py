from conc_test_report.company import Company
from conc_test_report.definitions import ReportPattern, ReportData
import re
from datetime import datetime
import pandas as pd

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

    def __init__(self, textblob: str, filepath: str):
        Company.__init__(self, textblob, filepath)
        self.name = "Kontur Geotechnical Consultants"
        
    def __str__(self) -> str:
        return f"Company parser for Kontur"

    def extract_data(self) -> ReportData:
        try:
            # pattern = {
            #     "Test Data": r"([A-Z]) *Cylinder *(\d*) *(Lab|Field) *((\d{2}-\w{3})|(\w{3}.\d{2})-? *(\d*) *[A-Za-z ]*)?\d{3}.\d *\d{3}.\d( *\d* *(\d*.\d))?",
            #     "Specified Strength": r"SPECIFIED *STRENGTH: *(\d*) *MPa *@ *(\d*) * DAYS",
            #     "Set Data": r"SET *NO.:(\d*) *SPECIMENS: *(\d*) *CAST: *(\d{4}.\w{3}.\d{2}) *TRANSPORTED: *(\d{4}.\w{3}.\d{2})",
            #     "Report Date": r".*Page *1 *of *\d* *(\d*.\w{3}.\d*)|(\d*-\w{3}-\d{4})",
            #     "Air": r".*AIR: *(\d{1,2}.?\d?) *% *SPEC.: *(\d{1,2}.?\d?) *± *(\d{1,2}.?\d?)",
            #     "Slump": r".*SLUMP: *(\d*) *mm *SPEC.: *(\d*) *± *(\d*)",
            #     "Mix": r".*MIX *NO.:? *(.*)$",
            #     "Load Volume": r"^LOAD *VOL.: *(\d*) m3"
            # }
            pattern = self.PATTERN
            for i, line in enumerate(self.data.split('\n')):
                specified_strength = re.match(pattern.specified_str, line.strip())
                if specified_strength:
                    self.data.specified_str = int(specified_strength.group(1))
                    self.data.specified_str_days = int(specified_strength.group(2))

                set_data = re.match(pattern.set_data, line)
                if set_data:
                    self.data.set_num = set_data.group(1)
                    self.data.specimens = int(set_data.group(2))
                    self.data.cast_date = datetime.strptime(set_data.group(3),"%Y.%b.%d")
                    self.data.transport_date = datetime.strptime(set_data.group(4),"%Y.%b.%d")
                    continue

                test_data = re.match(pattern.testdata, line)
                if test_data:
                    data = [test_data.group(1), test_data.group(3), test_data.group(6), test_data.group(7), test_data.group(9)]
                    if data[2]:
                        if datetime.strptime(data[2] + "-" +str(datetime.now().year), "%b.%d-%Y") > datetime.now():
                            data[2] = datetime.strptime(data[2] + "-" +str(datetime.now().year - 1), "%b.%d-%Y")
                        else:
                            data[2] = datetime.strptime(data[2] + "-" +str(datetime.now().year), "%b.%d-%Y")
                    df = pd.DataFrame([data],columns = self.test_data_cols)
                    self.data.test_data = pd.concat([self.data.test_data, df], ignore_index=True)
                    continue
                
                report_date = re.match(pattern.report_date, line)
                if report_date:
                    if report_date.group(1):
                        self.data.report_date = datetime.strptime(report_date.group(1),"%Y.%b.%d")
                    else:
                        self.data.report_date = datetime.strptime(report_date.group(2),"%d-%b-%Y")
                    continue

                air = re.match(pattern.air, line)
                if air:
                    self.data.air = float(air.group(1))
                    self.data.specified_air = [float(air.group(2))-float(air.group(3)), float(air.group(2))+float(air.group(3))]
                    continue

                if line.lower().strip().startswith('admixtures'):
                    for j in range(i, len(self.data.split('\n'))):
                        if self.data.split('\n')[j].lower().strip().startswith('curing'):
                            self.data.admixtures = self.data.split('\n')[i+1:j]
                            break
                    continue

                if line.lower().strip() == "location:":
                    for j in range(i, len(self.data.split('\n'))):
                        if self.data.split('\n')[j].lower().strip().startswith('supplier'):
                            self.data.location_comments = self.data.split('\n')[i+1:j]
                            break
                    continue

                if line.lower().strip() == "comments:":
                    for j in range(i, len(self.data.split('\n'))):
                        if self.data.split('\n')[j].lower().strip().startswith('load'):
                            self.data.other_comments = self.data.split('\n')[i+1:j]
                            break
                    continue
                
                slump = re.match(pattern.slump, line)
                if slump:
                    self.data.slump = int(slump.group(1))
                    try:
                        self.data.specified_slump = [int(slump.group(2))-int(slump.group(3)),int(slump.group(2))+int(slump.group(3))]
                    except:
                        self.data.specified_slump = []
                    continue

                mix = re.match(pattern.mix, line)
                if mix:
                    self.data.mix_num = mix.group(1)
                    continue

                load = re.match(pattern.load_vol, line.strip())
                if load:
                    try:
                        self.data.load_vol = float(load.group(1))
                    except:
                        self.log_error('e', 'Missing information on Load volume')

        except Exception as e:
            self.log_error('z',str(e))