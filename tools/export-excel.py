import ntpath
import glob
import json
import re
from xlrd import open_workbook
from xlutils.copy import copy
import csv

if __name__ == '__main__':
    csv_dir = "data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/1. TRANG 1 -1000.pdf"
    csv_dir = "data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/2. TRANG 1001-2000.pdf"
    csv_dir = "data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/3. TRANG 2001-3000.pdf"
    csv_dir = "data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/4. TRANG 3001-4000.pdf"
    rb = open_workbook("utils/documment/transaction-report - template.xls", encoding_override='utf8')
    wb = copy(rb)
    s = wb.get_sheet(1)
    export_filename = "data/export/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/" + csv_dir.split("/")[-1].replace(".pdf", ".xls")
    line_margin = 1
    line_count = 0
    for csv_path in sorted(glob.glob(f"{csv_dir}/*.csv"), key=lambda k: int(ntpath.basename(k).split('_')[-1].replace(".csv", ""))):
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i == 0:
                    print(f'Column names are {", ".join(row)}')
                else:
                    print(row)
                    for index, cell in enumerate(row):
                        s.write(line_margin + line_count, index, row[index])
                    line_count += 1
            print(f'Processed {line_count} lines.')
        wb.save(export_filename)
