// Multi-language translations
const translations = {
  en: {
    app_title: "Finance AI",
    app_subtitle: "Your personal financial assistant",
    logout: "Logout",
    tab_dashboard: "Dashboard",
    tab_charts: "Analytics", 
    tab_chat: "Chat with AI",
    tab_accounts: "Accounts",
    tab_export: "Export Report",
    total_balance: "Total Balance",
    loading: "Loading...",
    total_income: "Total Income",
    total_expenses: "Total Expenses",
    connected_accounts: "Connected Accounts",
    financial_insights: "Financial Insights",
    upload_data_prompt: "Upload your financial data to see insights...",
    analytics_title: "Financial Analytics",
    spending_category: "Spending by Category",
    monthly_trend: "Monthly Trend",
    daily_spending: "Daily Spending (Last 30 Days)",
    ai_assistant: "Finance AI Assistant",
    ready_to_help: "● Ready to help",
    welcome_message: "Hi! I'm your personal finance AI assistant. Upload your financial data and ask me anything!",
    ask_finances: "Ask about your finances...",
    send: "Send",
    connected_accounts_title: "Connected Accounts",
    loading_accounts: "Loading accounts...",
    add_new_account: "➕ Add New Account",
    bank_name_label: "Bank/Platform Name *",
    bank_name_placeholder: "e.g., HDFC Bank, Zerodha",
    account_type_label: "Account Type *",
    account_type_bank: "Bank Account",
    account_type_credit: "Credit Card",
    account_type_investment: "Investment",
    account_type_wallet: "Digital Wallet",
    upload_csv_label: "Upload CSV File *",
    csv_requirement: "CSV must have columns: date, description, amount",
    upload_connect: "Upload & Connect Account",
    export_title: "📄 Export Financial Report",
    export_description: "Generate a comprehensive PDF report of all your financial data.",
    report_includes: "Report includes:",
    report_item_1: "Personal information",
    report_item_2: "Financial summary (income, expenses, balance)",
    report_item_3: "All connected accounts",
    report_item_4: "Spending breakdown by category",
    report_item_5: "AI-generated insights",
    report_item_6: "Recent transactions",
    download_pdf: "Download PDF Report",
    delete: "Delete",
    transactions: "transactions",
    no_accounts: "No accounts connected yet. Add one below!",
    account_deleted: "Account deleted successfully!",
    account_connected: "Account connected successfully!",
    confirm_delete: "Are you sure you want to delete this account?",
    upload_failed: "Failed to upload file.",
    pdf_generated: "PDF downloaded successfully!",
    pdf_failed: "Failed to generate PDF. Please try again.",
    error_occurred: "Sorry, I encountered an error. Please try again.",
    this_period: "this period"
  },
  hi: {
    app_title: "फाइनेंस एआई",
    app_subtitle: "आपका व्यक्तिगत वित्तीय सहायक",
    logout: "लॉगआउट",
    tab_dashboard: "डैशबोर्ड",
    tab_charts: "विश्लेषण",
    tab_chat: "एआई से बात करें",
    tab_accounts: "खाते",
    tab_export: "रिपोर्ट निर्यात",
    total_balance: "कुल बैलेंस",
    loading: "लोड हो रहा है...",
    total_income: "कुल आय",
    total_expenses: "कुल खर्च",
    connected_accounts: "जुड़े खाते",
    financial_insights: "वित्तीय अंतर्दृष्टि",
    upload_data_prompt: "अंतर्दृष्टि देखने के लिए अपना वित्तीय डेटा अपलोड करें...",
    analytics_title: "वित्तीय विश्लेषण",
    spending_category: "श्रेणी के अनुसार खर्च",
    monthly_trend: "मासिक रुझान",
    daily_spending: "दैनिक खर्च (पिछले 30 दिन)",
    ai_assistant: "फाइनेंस एआई सहायक",
    ready_to_help: "● मदद के लिए तैयार",
    welcome_message: "नमस्ते! मैं आपका व्यक्तिगत वित्त एआई सहायक हूं। अपना वित्तीय डेटा अपलोड करें और कुछ भी पूछें!",
    ask_finances: "अपने वित्त के बारे में पूछें...",
    send: "भेजें",
    connected_accounts_title: "जुड़े खाते",
    loading_accounts: "खाते लोड हो रहे हैं...",
    add_new_account: "➕ नया खाता जोड़ें",
    bank_name_label: "बैंक/प्लेटफॉर्म का नाम *",
    bank_name_placeholder: "उदा., एचडीएफसी बैंक, ज़ेरोधा",
    account_type_label: "खाते का प्रकार *",
    account_type_bank: "बैंक खाता",
    account_type_credit: "क्रेडिट कार्ड",
    account_type_investment: "निवेश",
    account_type_wallet: "डिजिटल वॉलेट",
    upload_csv_label: "CSV फाइल अपलोड करें *",
    csv_requirement: "CSV में कॉलम होने चाहिए: तारीख, विवरण, राशि",
    upload_connect: "अपलोड करें और खाता जोड़ें",
    export_title: "📄 वित्तीय रिपोर्ट निर्यात करें",
    export_description: "अपने सभी वित्तीय डेटा की व्यापक PDF रिपोर्ट बनाएं।",
    report_includes: "रिपोर्ट में शामिल है:",
    report_item_1: "व्यक्तिगत जानकारी",
    report_item_2: "वित्तीय सारांश (आय, खर्च, बैलेंस)",
    report_item_3: "सभी जुड़े खाते",
    report_item_4: "श्रेणी के अनुसार खर्च का विवरण",
    report_item_5: "एआई द्वारा उत्पन्न अंतर्दृष्टि",
    report_item_6: "हाल के लेन-देन",
    download_pdf: "PDF रिपोर्ट डाउनलोड करें",
    delete: "हटाएं",
    transactions: "लेन-देन",
    no_accounts: "अभी तक कोई खाता नहीं जोड़ा गया। नीचे एक जोड़ें!",
    account_deleted: "खाता सफलतापूर्वक हटाया गया!",
    account_connected: "खाता सफलतापूर्वक जोड़ा गया!",
    confirm_delete: "क्या आप वाकई इस खाते को हटाना चाहते हैं?",
    upload_failed: "फ़ाइल अपलोड करने में विफल।",
    pdf_generated: "PDF सफलतापूर्वक डाउनलोड हुआ!",
    pdf_failed: "PDF बनाने में विफल। कृपया पुनः प्रयास करें।",
    error_occurred: "क्षमा करें, मुझे एक त्रुटि का सामना करना पड़ा। कृपया पुन: प्रयास करें।",
    this_period: "इस अवधि में"
  },
  mr: {
    app_title: "फायनान्स एआय",
    app_subtitle: "तुमचा वैयक्तिक आर्थिक सहाय्यक",
    logout: "लॉगआउट",
    tab_dashboard: "डॅशबोर्ड",
    tab_charts: "विश्लेषण",
    tab_chat: "एआयशी बोला",
    tab_accounts: "खाती",
    tab_export: "अहवाल निर्यात",
    total_balance: "एकूण शिल्लक",
    loading: "लोड होत आहे...",
    total_income: "एकूण उत्पन्न",
    total_expenses: "एकूण खर्च",
    connected_accounts: "जोडलेली खाती",
    financial_insights: "आर्थिक अंतर्दृष्टी",
    upload_data_prompt: "अंतर्दृष्टी पाहण्यासाठी तुमचा आर्थिक डेटा अपलोड करा...",
    analytics_title: "आर्थिक विश्लेषण",
    spending_category: "श्रेणीनुसार खर्च",
    monthly_trend: "मासिक ट्रेंड",
    daily_spending: "दैनिक खर्च (गेले 30 दिवस)",
    ai_assistant: "फायनान्स एआय सहाय्यक",
    ready_to_help: "● मदत करण्यासाठी तयार",
    welcome_message: "नमस्कार! मी तुमचा वैयक्तिक वित्त एआय सहाय्यक आहे. तुमचा आर्थिक डेटा अपलोड करा आणि काहीही विचारा!",
    ask_finances: "तुमच्या वित्ताबद्दल विचारा...",
    send: "पाठवा",
    connected_accounts_title: "जोडलेली खाती",
    loading_accounts: "खाती लोड होत आहेत...",
    add_new_account: "➕ नवीन खाते जोडा",
    bank_name_label: "बँक/प्लॅटफॉर्मचे नाव *",
    bank_name_placeholder: "उदा., एचडीएफसी बँक, झेरोधा",
    account_type_label: "खात्याचा प्रकार *",
    account_type_bank: "बँक खाते",
    account_type_credit: "क्रेडिट कार्ड",
    account_type_investment: "गुंतवणूक",
    account_type_wallet: "डिजिटल वॉलेट",
    upload_csv_label: "CSV फाईल अपलोड करा *",
    csv_requirement: "CSV मध्ये स्तंभ असणे आवश्यक आहे: तारीख, वर्णन, रक्कम",
    upload_connect: "अपलोड करा आणि खाते जोडा",
    export_title: "📄 आर्थिक अहवाल निर्यात करा",
    export_description: "तुमच्या सर्व आर्थिक डेटाचा सर्वसमावेशक PDF अहवाल तयार करा.",
    report_includes: "अहवालात समाविष्ट आहे:",
    report_item_1: "वैयक्तिक माहिती",
    report_item_2: "आर्थिक सारांश (उत्पन्न, खर्च, शिल्लक)",
    report_item_3: "सर्व जोडलेली खाती",
    report_item_4: "श्रेणीनुसार खर्चाचा तपशील",
    report_item_5: "एआय-निर्मित अंतर्दृष्टी",
    report_item_6: "अलीकडील व्यवहार",
    download_pdf: "PDF अहवाल डाउनलोड करा",
    delete: "हटवा",
    transactions: "व्यवहार",
    no_accounts: "अद्याप कोणतीही खाती जोडलेली नाहीत. खाली एक जोडा!",
    account_deleted: "खाते यशस्वीरित्या हटवले!",
    account_connected: "खाते यशस्वीरित्या जोडले!",
    confirm_delete: "तुम्हाला खात्री आहे की तुम्ही हे खाते हटवू इच्छिता?",
    upload_failed: "फाइल अपलोड करण्यात अयशस्वी.",
    pdf_generated: "PDF यशस्वीरित्या डाउनलोड झाला!",
    pdf_failed: "PDF तयार करण्यात अयशस्वी. कृपया पुन्हा प्रयत्न करा.",
    error_occurred: "माफ करा, मला एक त्रुटी आली. कृपया पुन्हा प्रयत्न करा.",
    this_period: "या कालावधीत"
  }
};

let currentLang = 'en';

function changeLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('preferredLang', lang);
  updatePageLanguage();
}

function updatePageLanguage() {
  const t = translations[currentLang];
  
  // Update all elements with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(element => {
    const key = element.getAttribute('data-i18n');
    if (t[key]) {
      element.textContent = t[key];
    }
  });
  
  // Update placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
    const key = element.getAttribute('data-i18n-placeholder');
    if (t[key]) {
      element.placeholder = t[key];
    }
  });
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
  const savedLang = localStorage.getItem('preferredLang') || 'en';
  document.getElementById('langSelector').value = savedLang;
  changeLanguage(savedLang);
  
  // Initialize theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    document.querySelector('.theme-toggle').textContent = '☀️';
  }
});

// Theme toggle
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  const themeToggle = document.querySelector('.theme-toggle');
  themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
}

// Export to make functions available globally
if (typeof window !== 'undefined') {
  window.changeLanguage = changeLanguage;
  window.toggleTheme = toggleTheme;
  window.translations = translations;
  window.getCurrentLang = () => currentLang;
}
