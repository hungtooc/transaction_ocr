# transaction_ocr
**Step 1. Find header & footer. </br>** 
**Step 2. Re-rotate image based on header-corner.</br>**
**Step 3. Clean image.</br>**
**Step 4. Call request google-ocr api.** (include:text-detection & text-recognization </br>
**Step 5. Detect transaction line.</br>**
![processing-step](https://user-images.githubusercontent.com/24487114/136381548-0e7daab6-a3aa-41d4-bdc7-bb57ed6b76b6.gif) (red)</br>
**Step 6. Read transactions content in image.</br>**
![read-transactions](https://user-images.githubusercontent.com/24487114/136383334-5ff62fca-1d5e-4118-b07c-111e40948bac.gif) </br>
**Step 7. Save transactions content to csv.</br>**
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
|13/10/2020|5091.56410 |     |500.000   |       |479627.131020.075913.Ung ho mien trung     
