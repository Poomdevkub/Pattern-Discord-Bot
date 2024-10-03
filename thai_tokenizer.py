# Runใน Terminal "python thai_tokenizer.py"
# นำเข้าไลบรารี
from pythainlp.tokenize import word_tokenize

# รับข้อความจากผู้ใช้
text = input("กรุณากรอกข้อความภาษาไทย: ")

# แยกคำ
words = word_tokenize(text, engine="newmm")

# แสดงผล
print("คำที่ถูกแยกออกมา:")
print(words)
