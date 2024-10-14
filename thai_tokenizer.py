# นำเข้าไลบรารี
import pandas as pd
from pythainlp.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# ขั้นตอนที่ 1: โหลดข้อมูล
data = pd.read_csv('data.csv')  # เปลี่ยนชื่อไฟล์เป็นชื่อไฟล์ของคุณ

# แสดงข้อมูลเบื้องต้น
print(data.head())

# ขั้นตอนที่ 2: แบ่งข้อมูลเป็น training และ testing set
X = data['text']  # ข้อความ
y = data['label']  # ป้ายกำกับ (0 = ไม่เป็นคำหยาบ, 1 = เป็นคำหยาบ)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ขั้นตอนที่ 3: สร้างโมเดล SVM
# ใช้ TfidfVectorizer และ SVM ใน pipeline
model = make_pipeline(TfidfVectorizer(tokenizer=word_tokenize), SVC(kernel='linear'))

# ขั้นตอนที่ 4: เทรนโมเดล
model.fit(X_train, y_train)

# ขั้นตอนที่ 5: ทำนายผล
y_pred = model.predict(X_test)

# ขั้นตอนที่ 6: แสดงผลลัพธ์
print(classification_report(y_test, y_pred))

# ขั้นตอนที่ 7: ทดสอบข้อความใหม่
def predict_new_text(text):
    words = word_tokenize(text)  # แยกคำก่อนการทำนาย
    prediction = model.predict([' '.join(words)])  # รวมคำที่แยกออกมาเป็นข้อความ
    return "คำหยาบ" if prediction[0] == 1 else "ไม่เป็นคำหยาบ"

# ตัวอย่างการทดสอบ
new_text = "สัส"
print("ข้อความ:", new_text)
print("ผลลัพธ์:", predict_new_text(new_text))
