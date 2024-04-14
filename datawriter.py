import pandas as pd
from collections import defaultdict
from typing import DefaultDict, Dict, Optional, List
from dataformat import ITableRow_1 , ITableRow_2 , ITableRow_3 , ITableRow_US, IEtimilogia_US

class DataWriter():
    """ Takes default dicts as input and writes excel reports from them"""
    def __init__(self, outfile_path) -> None:
        self.outfile_path = outfile_path

    def change_path(self, outfile) -> None:
        self.outfile_path = outfile
    # You dont really need 3 different functions. But its good practice to keep them
    # separate in case the ITableRow_X drastically change
    def write_excel_table1(self , data : DefaultDict[str,ITableRow_1]) -> None:
        "Takes a default dictionary and writes the raw data"
        df = pd.DataFrame.from_dict(data, orient='index').reset_index()
        df.rename(columns={'index': 'Identifier'}, inplace=True)
        with pd.ExcelWriter(self.outfile_path , engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

    def write_excel_table2(self , data : DefaultDict[str,ITableRow_2]) -> None:
        "Takes a default dictionary and writes the raw data"
        df = pd.DataFrame.from_dict(data, orient='index').reset_index()
        df.rename(columns={'index': 'Identifier'}, inplace=True)
        with pd.ExcelWriter(self.outfile_path , engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

    def write_excel_table3(self , data : DefaultDict[str,ITableRow_3]) -> None:
        "Takes a default dictionary and writes the raw data"
        df = pd.DataFrame.from_dict(data, orient='index').reset_index()
        df.rename(columns={'index': 'Identifier'}, inplace=True)
        with pd.ExcelWriter(self.outfile_path , engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

    def write_us_table(self , data : List[ITableRow_US]) -> None:
        "Takes a list of TableRows"
        df = pd.DataFrame(data)
        df.rename(columns={'index': 'Identifier'}, inplace=True)
        with pd.ExcelWriter(self.outfile_path , engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

    def write_us_etimologia(self , data : List[IEtimilogia_US]) -> None:
        "Takes a list of IEtiomologias"
        df = pd.DataFrame(data)
        df.rename(columns={'index': 'Identifier'}, inplace=True)
        with pd.ExcelWriter(self.outfile_path , engine="openpyxl") as writer:
            df.to_excel(writer, index=False)