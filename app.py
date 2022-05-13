import os
import os.path
from data_processor import prepare_source_list, data_transformer

cwd_path = os.path.dirname(__file__)

# config
OUTPUT_FILE = 'championat.csv'
target_path = '.'
target_folder = os.path.abspath(target_path)
csv_path = target_folder + os.path.sep + OUTPUT_FILE
xls_name = 'игровое время.xlsx'
xls_sheetname_format = 'Итоговый формат'
xls_sheetname_sources = 'Список источников'

# define input and output paramenters, web_extraction process, save the results to csv
check_csv_file = os.path.exists(csv_path)
if check_csv_file is True:
    print('CSV file found: ', OUTPUT_FILE)
else:
    print('Job started')
    print(
        'Will save output comma separated file to folder: %s' % (
            target_folder,
        )
    )
    source_list = prepare_source_list(xls_name, xls_sheetname_sources)
    output_frame = data_transformer(
        xls_name,
        xls_sheetname_format,
        source_list
    )
    output_frame.to_csv(
        OUTPUT_FILE,
        sep=';',
        encoding='cp1251',
        header=True,
        index=False
    )
    print('Affected count or rows:', (output_frame.shape[0]))
    print('Job finished.')
