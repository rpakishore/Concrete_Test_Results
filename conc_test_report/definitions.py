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
    report_date: date = field(default=date)
    set_num: str = field(default_factory=str)
    specimens: int = field(default_factory=int)
    cast_date: date = field(default=date)
    transport_date: date = field(default=date)
    specified_str: float = field(default_factory=float)
    specified_str_days: int = field(default_factory=int)
    mix_num: int = field(default_factory=int)
    load_vol: float = field(default_factory=float)
    slump: float = field(default_factory=float)
    specified_slump: float = field(default_factory=float)
    air: float = field(default_factory=float)
    specified_air: float = field(default_factory=float)
    admixtures: list = field(default_factory=list)
    location_comments: list = field(default_factory=list)
    other_comments: list = field(default_factory=list)
    errors: pd.DataFrame = field(default=pd.DataFrame(columns=['Error Code', 'Description']))
    test_data: pd.DataFrame = field(default=pd.DataFrame(columns=['Specimen','Cure','Test_Date', 'Age', 'Compressive_Str']))
    filename: str = field(default_factory=str)

    def __post_init__(self):
        self.filename = self.filepath.name