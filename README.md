
# 🚀 Project - Backend & Frontend

This project consists of a **backend** in Python (FastAPI) and a **frontend** in Node.js.

---

## 📌 Requirements

- **Backend**
  - Python 3.9+
  - pip

- **Frontend**
  - Node.js 16+
  - npm

---

## ⚙️ Backend Setup

1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Start the server in /backend:
   \`\`\`bash
   uvicorn app.main:app --reload
   \`\`\`

3. To add new dependencies to \`requirements.txt\`:
   \`\`\`bash
   pip freeze > requirements.txt
   \`\`\`

---

## 💻 Frontend Setup

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Start the development server in /frontend:
   \`\`\`bash
   npm run dev
   \`\`\`

---

## 📂 Project Structure

\`\`\`
project/
├── backend/
│   ├── requirements.txt
│   └── app/
│        ├── main.py
│        └── ...
└── frontend/
    ├── package.json
    ├── src/
    └── ...
\`\`\`

---

## 🛠️ Technologies Used

- **Backend:** FastAPI, Uvicorn
- **Frontend:** Node.js, npm

