import sklearn
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score


# ตัวอย่างข้อมูลข้อความ
texts = ["I love programming", "Python is amazing", "I hate bugs", "Coding is fun", "I dislike errors"]
labels = [1, 1, 0, 1, 0]  # 1=Positive, 0=Negative

# แปลงข้อความเป็น TF-IDF เวกเตอร์
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# แบ่งข้อมูลออกเป็นชุดฝึกและชุดทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)

# สร้างโมเดล SVM
model = svm.SVC(kernel='linear')  # ใช้ kernel แบบเส้นตรง
model.fit(X_train, y_train)  # ฝึกโมเดล

# ทำนายผลลัพธ์
predictions = model.predict(X_test)

# ตรวจสอบความแม่นยำ
print("Accuracy:", accuracy_score(y_test, predictions))