import os
import subprocess
import glob
import ntpath
from pdf2image import convert_from_path, convert_from_bytes
if __name__ == '__main__':
    files_dir = "/home/hungtooc/Documents/SAOKE_THUYTIEN/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)"
    password = "Vcbsaoke@2021"
    output_dir = "/home/hungtooc/Documents/SAOKE-ThuyTien/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)"
    # make dirs
    for file_dir in glob.glob(f"{files_dir}/*/*/"):
        os.mkdir(file_dir)
    for file_path in glob.glob(f"{files_dir}/*/*.pdf"):
        print(" ".join([f'pdftk', f"{file_path}", "input_pw", f"{password}", "output",
                        f'"{output_dir}/{ntpath.basename(file_path)}"']))
        subprocess.run(
            [f'pdftk', f'"{file_path}"', '"input_pw"', f'"{password}"', "output",
             f'"{output_dir}/{ntpath.basename(file_path)}"'])
        input()
