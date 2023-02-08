from dataclasses import dataclass

#NEXT STEPS
#Break down the report patters so that each patter is only picking up one item. 
#This will make it easier to write a function `_extract_report_fields_from_txt`
#that will work for all the companies.
@dataclass
class ReportPattern:
    testdata: str
    specified_str: str
    specified_str_days: str
    set_num: str
    specimens: str
    cast_date: str
    transport_date: str
    set_data: str
    report_date: str
    air: str
    slump: str
    mix: str
    load_vol: str
    

COMPANY_PATTERNS = {
    "Kontur Geotechnical Consultants": ReportPattern(
        testdata = r"([A-Z]) *Cylinder *(\d*) *(Lab|Field) *((\d{2}-\w{3})|(\w{3}.\d{2})-? *(\d*) *[A-Za-z ]*)?\d{3}.\d *\d{3}.\d( *\d* *(\d*.\d))?",
        specified_str = r"SPECIFIED *STRENGTH: *(\d*) *MPa *@ *\d* * DAYS",
        specified_str_days = r"SPECIFIED *STRENGTH: *\d* *MPa *@ *(\d*) * DAYS",
        set_num = r"SET *NO.:(\d*) *SPECIMENS: *\d* *CAST: *\d{4}.\w{3}.\d{2} *TRANSPORTED: *\d{4}.\w{3}.\d{2}",
        specimens = r"SET *NO.:\d* *SPECIMENS: *(\d*) *CAST: *\d{4}.\w{3}.\d{2} *TRANSPORTED: *\d{4}.\w{3}.\d{2}",
        cast_date = r"SET *NO.:\d* *SPECIMENS: *\d* *CAST: *(\d{4}.\w{3}.\d{2}) *TRANSPORTED: *\d{4}.\w{3}.\d{2}",
        trasport_date = r"SET *NO.:\d* *SPECIMENS: *\d* *CAST: *\d{4}.\w{3}.\d{2} *TRANSPORTED: *(\d{4}.\w{3}.\d{2})",
        report_date = r".*Page *1 *of *\d* *(\d*.\w{3}.\d*)|(\d*-\w{3}-\d{4})",
        air = r".*AIR: *(\d{1,2}.?\d?) *% *SPEC.: *(\d{1,2}.?\d?) *± *(\d{1,2}.?\d?)",
        slump = r".*SLUMP: *(\d*) *mm *SPEC.: *(\d*) *± *(\d*)",
        mix = r".*MIX *NO.:? *(.*)$",
        load_vol = r"^LOAD *VOL.: *(\d*) m3"
        ),
    "McElhanney": ReportPattern(
        testdata = r".*([A-Z]) *Cylinder *(Lab|Field) *(\d*) *((\d{2}-\w{3})-? *(\d*) *[A-Za-z ]*)?\d{3}.\d *\d{3}.\d( *\d* *(\d*.\d))?",
        specified_str = r"SPECIFIED STRENGTH\s*(\d*)MPa *@ *\d* DAYS",
        specified_str_days = r"SPECIFIED STRENGTH\s*\d*MPa *@ *(\d*) DAYS",
        set_num = r".*SET *NO.(\d*) *SPECIMENS *\d* *CAST *\d{2}-\w{3}-\d{4} *TRANSPORTED *\d{2}-\w{3}-\d{4}",
        specimens = r".*SET *NO.\d* *SPECIMENS *(\d*) *CAST *\d{2}-\w{3}-\d{4} *TRANSPORTED *\d{2}-\w{3}-\d{4}",
        cast_date = r".*SET *NO.\d* *SPECIMENS *\d* *CAST *(\d{2}-\w{3}-\d{4}) *TRANSPORTED *\d{2}-\w{3}-\d{4}",
        trasport_date = r".*SET *NO.\d* *SPECIMENS *\d* *CAST *\d{2}-\w{3}-\d{4} *TRANSPORTED *(\d{2}-\w{3}-\d{4})",
        report_date = r".*Page *1 *of *\d* *(\d{4}.\w{3}.\d*)|(\d*-\w{3}-\d{4})",
        air = r".*AIR *(\d{1,2}.?\d?) *% *SPEC. *(\d{1,2}.?\d?) *± *(\d{1,2}.?\d?)",
        slump = r".*SLUMP *(\d*) *mm *SPEC. *(\d*) *± *(\d*)",
        mix = r".*MIX *NO. *(.*)$",
        load_vol = r"^LOAD *VOL. *(\d*) m3"
    )
}