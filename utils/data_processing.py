import json
import csv


def save_content(file_path, header, contents):
    with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # write the data
        for data in contents:
            writer.writerow(data)


def save_respone(textsOCR, input_image_path, output_file_path):
    data = {"image_path": input_image_path, "respone": []}
    for text in textsOCR:
        data["respone"].append({"desc": text.description, "vertices": [[[vertice.x, vertice.y] for vertice in text.bounding_poly.vertices]]})
    with open(output_file_path, 'w', encoding="utf8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def append_processed(log_file, image_path):
    flog = open(log_file, "a", encoding='utf8')
    flog.write(f"{image_path}\n")
