import pandas as pd
import glob


def get_output_format(xls_name, sheetname):
    list_files = glob.glob('*xlsx*')
    for filename in list_files:
        if filename == xls_name:
            xl_file = pd.ExcelFile(filename)
            dfs = {
                sheet_name: xl_file.parse(
                    sheet_name
                ) for sheet_name in xl_file.sheet_names
            }
            columns = dfs[sheetname].columns
    return columns


def get_source_list(xls_name, sheetname):
    list_files = glob.glob('*xlsx*')
    for filename in list_files:
        if filename == xls_name:
            xl_file = pd.ExcelFile(filename)
            dfs = {
                sheet_name: xl_file.parse(
                    sheet_name
                ) for sheet_name in xl_file.sheet_names
            }
            source_list = dfs[sheetname].values
    return source_list
