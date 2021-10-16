# Transaction OCR
## 1. Repair data input
### 1.1 Download raw data
- Download raw pdf files from Drive link: https://drive.google.com/drive/folders/1SoWOGaAy92tZUgG7mwhJzoeBsDpxVO80?usp=sharing
- Extra & put it in **data/input** </br>
### 1.2 Convert pdf files to image
PDF password:   `Vcbsaoke@2021`
``` 
python tools/pdf-to-images.py --pdf-password Vcbsaoke@2021
```
```
usage: pdf-to-images.py [-h] [--pdf-dir PDF_DIR] [--output-dir OUTPUT_DIR] [--pdf-password PDF_PASSWORD] [--from-page-no FROM_PAGE_NO] [--to-page-no TO_PAGE_NO] [--fix-page-number FIX_PAGE_NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  --pdf-dir PDF_DIR     dir to pdf files
  --output-dir OUTPUT_DIR
                        dir to save images
  --pdf-password PDF_PASSWORD
                        pdf password
  --from-page-no FROM_PAGE_NO
                        extra image from page
  --to-page-no TO_PAGE_NO
                        extra image to page
  --fix-page-number FIX_PAGE_NUMBER
                        fix page number (page_no += fix_page_number)
```

## 2. Extract transaction information
```
python run.py 
```
```
usage: run.py [-h] [--image-dir IMAGE_DIR] [--output-respone-dir OUTPUT_RESPONE_DIR] [--output-content-dir OUTPUT_CONTENT_DIR] [--processed-log-file PROCESSED_LOG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --image-dir IMAGE_DIR
                        dir to images
  --output-respone-dir OUTPUT_RESPONE_DIR
                        dir to save api respone
  --output-content-dir OUTPUT_CONTENT_DIR
                        dir to save transaction content
  --processed-log-file PROCESSED_LOG_FILE
                        path to log file
```
#### File `run.py` perform 7 main stages: 
- Step 1. Find header & footer. </br>
- Step 2. Re-rotate image based on header-corner.</br>
- Step 3. Clean image.</br>
- Step 4. Call request google-ocr api. (include:text-detection & text-recognization </br>
- Step 5. Detect transaction line.</br>
![processing-step-boder](https://user-images.githubusercontent.com/24487114/136387897-961d28ec-c064-4191-b135-836cfaf3753e.gif) </br> </br>
- Step 6. Classify transaction content each line & each content type.</br>
![read-transactions-border](https://user-images.githubusercontent.com/24487114/136387974-751258bc-8ed1-4388-ad41-b176a9ec16c8.gif) </br> </br>
- Step 7. Save transactions content to csv. </br>

|TNX Date  |Doc No     |Debit|Credit    |Balance|Transaction in detail                                                                                                                |(note)|
|----------|-----------|-----|----------|-------|-------------------------------------------------------------------------------------------------------------------------------------|------|
|13/10/2020|5091.55821 |     |100.000   |       |586062.131020.075756.Ung ho mien trung FT20287151644070                                                                              |page_1|
|13/10/2020|5091.56080 |     |1.000.000 |       |586279.131020.075829.Ung ho dong bao mien Trung FT20287592192480                                                                     |page_1|
|13/10/2020|5091.56138 |     |200.000   |       |219987.131020.075839.Trinh Thi Thu Thuy chuyen tien ung ho mien Trung                                                                |page_1|
|13/10/2020|5091.56155 |     |100.000   |       |586295.131020.075826.UH mien trung FT20287432289640                                                                                  |page_1|
|13/10/2020|5078.68388 |     |500.000   |       |MBVCB.807033343.PHAM THUY TRANG chuyen tien ung ho tu thien.CT tu 0561000606153 PHAM THUY TRANG toi 0181003469746 TRAN THI THUY TIEN |page_1|
|13/10/2020|5091.56261 |     |1.000.000 |       |184997.131020.075853.Em gui giup do ba con vung lu                                                                                   |page_1|
|13/10/2020|5078.68496 |     |200.000   |       |MBVCB.807033583.Ung ho mien trung.CT tu 0051000531310 HUYNH THI NHU Y toi 0181003469746 TRAN THI THUY TIEN                           |page_1|
|13/10/2020|5078.68526 |     |100.000   |       |MBVCB.807033514.ung ho mien trung.CT tu 0481000903279 NGUYEN THI HUONG AN toi 0181003469746 TRAN THI THUY TIEN                       |page_1|
|13/10/2020|5091.56381 |     |100.000   |       |479592.131020.075909.ho tro mien trung                                                                                               |page_1|
|13/10/2020|5078.68537 |     |500.000   |       |MBVCB.807034561.Ung ho Mien trung.CT tu 0721000588146 LE THI HONG DIEM toi 0181003469746 TRAN THI THUY TIEN                          |page_1|
|13/10/2020|5091.56405 |     |200.000   |       |292363.131020.075845.Ngan hang TMCP Ngoai Thuong Viet Nam 0181003469746 LUC NGHIEM LE chuyen khoan ung ho mien trung                 |page_1|
|13/10/2020|5091.56410 |     |500.000   |       |479627.131020.075913.Ung ho mien trung     |page_1|
## 3. Export Excel
Export each csv directory to an excel file. Example:
```
python tools/export-excel.py --csv-dir "data/content/TÀI KHOẢN XXX746 (Pass_ Vcbsaoke@2021)/TỪ 13.10.20 ĐẾN 23.11.20/1. TRANG 1 -1000.pdf"
```
```
usage: export-excel.py [-h] --csv-dir CSV_DIR [--output-dir OUTPUT_DIR] [--transaction-template TRANSACTION_TEMPLATE] [--filename FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --csv-dir CSV_DIR     csv dir
  --output-dir OUTPUT_DIR
                        output dir
  --transaction-template TRANSACTION_TEMPLATE
                        dir to save transaction content
  --filename FILENAME   output filename, leave blank to set default

```
