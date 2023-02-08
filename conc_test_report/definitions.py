from dataclasses import dataclass, field
from pathlib import Path
from datetime import date
import pandas as pd

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

@dataclass
class ReportData:
    filepath: Path
    company: str
    report_date: date
    set_num: str
    specimens: int
    cast_date: date
    transport_date: date
    specified_str: float
    specified_str_days: int
    mix_num: int
    load_vol: float
    slump: float
    specified_slump: float
    air: float
    specified_air: float
    admixtures: list = field(default=[])
    location_comments: list = field(default=[])
    other_comments: list = field(default=[])
    errors: pd.DataFrame = field(default=pd.DataFrame(columns=['Error Code', 'Description']))
    test_data: pd.DataFrame = field(default=pd.DataFrame(columns=['Specimen','Cure','Test_Date', 'Age', 'Compressive_Str']))
    filename: str = field(default=None)

    def __post_init__(self):
        self.filename = self.filepath.name