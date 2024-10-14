# นำเข้าไลบรารี
from pythainlp.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
import pandas as pd

# นำเข้าข้อมูล
data = pd.read_csv("data.csv")  # เปลี่ยนเป็นชื่อไฟล์ของคุณ
print(data)

# แยกข้อมูลเป็น features และ labels
X = data['text']
y = data['label']

# แบ่งข้อมูลเป็นชุดฝึกและชุดทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# สร้าง TfidfVectorizer
vectorizer = TfidfVectorizer(tokenizer=word_tokenize)  # ใช้ tokenizer ของ ThaiNLP
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# สร้างโมเดล SVM
model = svm.SVC(kernel='linear')
model.fit(X_train_vect, y_train)

# ทำนายข้อมูลทดสอบ
y_pred = model.predict(X_test_vect)

# แสดงผลการทำนาย
print(classification_report(y_test, y_pred))

# ฟังก์ชันทำนายข้อความใหม่
# ฟังก์ชันทำนายข้อความใหม่
def predict_new_text(text):
    words = word_tokenize(text)  # แยกคำก่อนการทำนาย
    print("คำที่แยกออกมา:", words)  # แสดงคำที่แยกออกมา
    text_vect = vectorizer.transform([text])  # แปลงข้อความเป็น feature vector
    prediction = model.predict(text_vect)  # ทำนายด้วยโมเดล
    return "คำหยาบ" if prediction[0] == 1 else "ไม่เป็นคำหยาบ"

# ตัวอย่างการทดสอบ
new_text = input("กรุณาใส่ข้อความที่ต้องการตรวจสอบ: ")
print("ข้อความ:", new_text)
print("ผลลัพธ์:", predict_new_text(new_text))

