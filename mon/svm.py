# นำเข้าไลบรารี
from pythainlp.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from joblib import dump
import pandas as pd
import warnings

# ปิดคำเตือนเกี่ยวกับ 'token_pattern'
warnings.filterwarnings("ignore", message="The parameter 'token_pattern' will not be used since 'tokenizer' is not None")

# นำเข้าข้อมูล
data = pd.read_csv("data.csv")  # เปลี่ยนเป็นชื่อไฟล์ของคุณ
print(data)

# แยกข้อมูลเป็น features และ labels
X = data['text']
y = data['label']

# แบ่งข้อมูลเป็นชุดฝึกและชุดทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# สร้าง TfidfVectorizer โดยใช้ tokenizer ของ ThaiNLP
vectorizer = TfidfVectorizer(tokenizer=word_tokenize, max_features=1000)  # สามารถกำหนด max_features เพื่อลดขนาดข้อมูลได้

# แปลงข้อมูลชุดฝึกและชุดทดสอบเป็นเวกเตอร์
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# สร้างโมเดล SVM
model = svm.SVC(kernel='linear')
model.fit(X_train_vect, y_train)

# ทำนายข้อมูลทดสอบ
y_pred = model.predict(X_test_vect)

# แสดงผลการทำนาย พร้อมจัดการ zero_division เพื่อป้องกัน undefined metric
print(classification_report(y_test, y_pred, zero_division=1))

# บันทึกโมเดล SVM และ vectorizer ลงไฟล์
dump(model, 'svm_profanity_model.joblib')
dump(vectorizer, 'vectorizer.joblib')

print("โมเดลและ vectorizer ถูกบันทึกเรียบร้อยแล้ว.")
