# 💰 Finance AI – Personal Financial Assistant

A web application that helps users analyze their financial habits by uploading **CSV files** of bank statements and interacting with an **AI assistant Chatbot**.

---

## 🚀 Features

### 🎯 Core Features
- **User Registration & Sessions** – Landing page for user onboarding and session-based authentication
- **Multiple Account Management** – Upload and manage multiple bank or investment accounts using CSV files
- **AI-Powered Chat** – Interactive chat with Gemini AI for financial insights and personalized advice
- **Comprehensive Dashboard** – Real-time overview of financial health with dynamic metrics
- **Visual Analytics** – Interactive charts powered by Chart.js for spending categories and trends
- **PDF Export** – Generate detailed financial reports and download them as PDFs
- **Multi-language Support** – Support for English, Hindi, and Marathi

---

## 📊 Dashboard Metrics
- 💵 Total Balance  
- 📈 Total Income & Expenses  
- 🔄 Net Change  
- 🏦 Connected Accounts Count  
- 🧾 Category-wise Spending Breakdown  
- 🤖 AI-Generated Financial Insights  
- ⚠️ Spending Trends & Alerts  

---

## 💬 AI Chat Features
- Ask natural language questions about your **spending patterns**
- Get **personalized financial advice** based on your data
- Analyze **transactions across multiple accounts**
- Receive **context-aware** responses powered by Gemini AI

---

## 📄 PDF Report Contents
- Personal information
- Financial summary
- Connected accounts
- Spending by category
- AI-generated insights
- Recent transactions

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Flask (Python) |
| **AI** | Google Gemini 3 Flash |
| **Data Processing** | Pandas |
| **PDF Generation** | ReportLab |
| **Frontend** | HTML, CSS, JavaScript (Vanilla) |
| **Storage** | JSON + CSV files |

---

## 📁 Project Structure
```
finance_ai/
├── app.py              # Main Flask application
├── gemini_helper.py    # Gemini AI integration
├── process_data.py     # Data processing & analytics
├── pdf_generator.py    # PDF report generation
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (API keys)
│
├── templates/
│   ├── landing.html         # User registration page
│   ├── index_enhanced.html  # Main dashboard with charts
│   └── home.html            # Introduction page
│
├── static/
│   ├── styles.css      # Styles for frontend
│   ├── app.js          # Dashboard logic
│   ├── charts.js       # Chart.js configurations
│   └── i18n.js         # Multi-language translations
│
├── uploads/            # Temporary CSV uploads
├── user_data/          # User info & financial data
│   ├── users.json      # User database
│   └── user_*/         # Individual user folders
│
└── temporary/          # Generated PDF reports
```
---

```bash
🪜 Step 1: Clone or Download the Project

git clone https://github.com/yourusername/finance_ai.git
cd finance_ai


🪜 Step 2: Create a Virtual Environment (Recommended)
python -m venv venv
# Activate the virtual environment:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate


🪜 Step 3: Install Dependencies
pip install -r requirements.txt


🪜 Step 4: Set Up Environment Variables
Create a .env file in the project root and add:
GOOGLE_API_KEY=your_gemini_api_key_here

🔑 How to Get Gemini API Key
Visit Google AI Studio
Sign in with your Google account
Click "Create API Key"
Copy and paste the key into your .env file


🪜 Step 5: Run the Application
python app.py
Open your browser and visit:
👉 http://127.0.0.1:5000/


🧭 Usage Guide

1️⃣ Register
Open the app in your browser.
Fill in your name, email, phone, and address on the landing page.

2️⃣ Upload Bank Statements
Go to the dashboard and upload one or more CSV files from your bank or investment accounts.

3️⃣ View Dashboard
Instantly view income, expenses, balances, category-wise spending, and more.

4️⃣ Chat with AI
Use the integrated chat to ask questions like:
“How much did I spend on food last month?”
“What’s my biggest expense category?”
“Am I saving more than last quarter?”

5️⃣ Generate PDF Report
Click the Download Report button to export a detailed financial report in PDF format.


🧰 Future Enhancements
🔐 Advanced multi-user authentication (passwords/OAuth)
☁️ Cloud database integration (MongoDB or Firebase)
💬 Voice-based AI assistant
📆 Budget goal tracking & reminders
📊 Automated expense categorizer (ML based)


👩‍💻 Contributing
Contributions are welcome!
To contribute:
Fork the repository
Create a new branch (feature/my-feature)
Commit your changes
Push and open a Pull Request


🪪 License
This project is licensed under the MIT License – see the LICENSE file for details.


🧑‍💼 Author
Yugant Varekar
Parth Chaudhari
Khilesh Chaudhari
Yagnesh Paliwal
📍 India
💬 Building AI-powered financial tools to help people understand their money better.


⭐ Acknowledgements
Google Gemini API
Flask
ReportLab
Pandas


“Finance AI — Because understanding your money should be as easy as talking to a friend.”