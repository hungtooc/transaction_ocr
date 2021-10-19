import ntpath
import glob
import json
import re
import csv
import sys
import os
from xlrd import open_workbook
from xlutils.copy import copy
from pathlib import Path
import argparse
from tqdm import tqdm
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-dir', type=str, required=True, help='csv dir')
    parser.add_argument('--output-dir', type=str, default=ROOT / 'data/export/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/',
                        help='output dir')
    parser.add_argument('--transaction-template', type=str, default=ROOT / 'utils/documment/transaction-report-template.xls',
                        help='dir to save transaction content')
    parser.add_argument('--filename', type=str, default='', help='output filename, leave blank to set default')
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    csv_dir = opt.csv_dir
    # csv_dir = f"{ROOT}/data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/1. TRANG 1 -1000.pdf"
    output_dir = opt.output_dir
    transaction_template = opt.transaction_template
    output_filename = opt.filename if opt.filename != '' else f"{csv_dir.split('/')[-1].replace('.pdf', '.xls')}"
    output_file_path = f"{output_dir}/{output_filename}"
    rb = open_workbook(transaction_template, encoding_override='utf8')
    wb = copy(rb)
    s = wb.get_sheet(0)
    line_margin = 1
    line_count = 0
    for csv_path in tqdm(sorted(glob.glob(f"{csv_dir}/*.csv"), key=lambda k: int(ntpath.basename(k).split('_')[-1].replace(".csv", "")))):
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                else:
                    tqdm.write(" | ".join(row))
                    for index, cell in enumerate(row):
                        s.write(line_margin + line_count, index, row[index])
                    line_count += 1
        wb.save(output_file_path)
