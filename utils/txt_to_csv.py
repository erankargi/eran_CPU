import csv


txt_file_path = 'data/case1.txt'
csv_file_path = 'data/case1.csv'


with open(txt_file_path, 'r') as txt_file:
   
    lines = txt_file.readlines()

    
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        
        writer.writerow(lines[0].strip().split(','))

        
        for line in lines[1:]:
            writer.writerow(line.strip().split(','))
            
print(f"TXT dosyası {csv_file_path} olarak başarıyla kaydedildi.")
