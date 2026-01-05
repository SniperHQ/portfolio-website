# Portfolio Website

This is **Mqondisi Ntshangase’s personal portfolio website**, built using **Django**, **HTML**, **CSS**, and **JavaScript**.

It showcases:

- Hero section with introduction and profile image  
- Timeline / Journey / Skills  
- Project gallery and project details  
- Contact form with email and WhatsApp integration  
- Fully responsive design for mobile and desktop  

---

## 🔹 Features

- Dynamic content managed via **Django Admin**  
- Smooth animations & reveal effects  
- Skills displayed as circular progress bars  
- Timeline section for education & work experience  
- Project slider & detailed project pages  
- Contact form with validation

---

## 🔹 Installation

```bash
git clone https://github.com/SniperHQ/portfolio-website.git
cd portfolio-website
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
