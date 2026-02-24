## 📦 Инсталация

### 1️⃣ Клониране на проекта:

git clone https://github.com/RaliHristova/ErmaInsProject.git  
cd ErmaInsProject

### 2️⃣ Създаване на виртуална среда:
python -m venv .venv  
-Windows:
.venv\Scripts\activate  
-Mac/Linux:
source .venv/bin/activate

### 3️⃣ Инсталиране на зависимости:
pip install -r requirements.txt

### 4️⃣ Прилагане на миграции:
python manage.py migrate

### 5️⃣ Стартиране на сървъра:
python manage.py runserver

### 🚀 Отвори в браузър:
http://127.0.0.1:8000/

### 🔐 Production настройки:
За да работи custom error страницата:
- DEBUG = False  
- ALLOWED_HOSTS = [*]