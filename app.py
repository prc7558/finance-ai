from flask import Flask, render_template, request, jsonify, session, send_file
import os
import pandas as pd
import json
from datetime import datetime
from process_data import process_csv, calculate_dashboard_metrics, generate_insights, normalize_csv
from gemini_helper import ask_gemini
from pdf_generator import generate_pdf_report

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-key-change-this-in-env')

UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'user_data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# Store user data in JSON file
USER_DATA_FILE = os.path.join(DATA_FOLDER, 'users.json')

def load_users():
    """Load user data from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user data to JSON file"""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user_folder(user_id):
    """Get user-specific folder for storing accounts"""
    folder = os.path.join(DATA_FOLDER, f"user_{user_id}")
    os.makedirs(folder, exist_ok=True)
    return folder

# ------------------- Home Page -------------------
@app.route('/')
def home():
    """Show home page"""
    return render_template('home.html')

# ------------------- Landing Page -------------------
@app.route('/landing')
def landing():
    """Show landing page for user registration"""
    return render_template('landing.html')

# ------------------- Register User -------------------
@app.route('/register', methods=['POST'])
def register():
    """Register new user and create session"""
    data = request.get_json()
    
    # Generate user ID
    users = load_users()
    user_id = str(len(users) + 1)
    
    # Store user info
    users[user_id] = {
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'address': data.get('address'),
        'created_at': datetime.now().isoformat(),
        'accounts': []
    }
    save_users(users)
    
    # Create session
    session['user_id'] = user_id
    session['user_name'] = data.get('name')
    
    return jsonify({'success': True, 'user_id': user_id})

# ------------------- Dashboard -------------------
@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    if 'user_id' not in session:
        return render_template('landing.html')
    return render_template('index_enhanced.html')

# ------------------- Get User Accounts -------------------
@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Get all connected accounts for current user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    users = load_users()
    user = users.get(session['user_id'], {})
    accounts = user.get('accounts', [])
    
    return jsonify({'accounts': accounts})

# ------------------- Upload CSV with Bank Name -------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload CSV file and associate with bank/platform name"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    bank_name = request.form.get('bank_name', 'Unknown Bank')
    account_type = request.form.get('account_type', 'Bank')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Read CSV
        df = pd.read_csv(file)
        
        # Save file to user folder
        user_folder = get_user_folder(session['user_id'])
        filename = f"{bank_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(user_folder, filename)
        df.to_csv(filepath, index=False)
        
        # Process and get summary
        summary = process_csv(df)
        
        # Add to user's accounts
        users = load_users()
        user = users[session['user_id']]
        
        account = {
            'id': len(user['accounts']) + 1,
            'bank_name': bank_name,
            'account_type': account_type,
            'filepath': filepath,
            'uploaded_at': datetime.now().isoformat(),
            'rows': len(df),
            'columns': list(df.columns),
            'balance': summary.get('total_balance', 0)
        }
        
        user['accounts'].append(account)
        save_users(users)
        
        return jsonify({
            'success': True,
            'account': account,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- Delete Account -------------------
@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Delete a connected account"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    users = load_users()
    user = users[session['user_id']]
    
    # Find and remove account
    user['accounts'] = [acc for acc in user['accounts'] if acc['id'] != account_id]
    save_users(users)
    
    return jsonify({'success': True})

# ------------------- Get Dashboard Metrics -------------------
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Calculate and return dashboard metrics from all accounts"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    users = load_users()
    user = users.get(session['user_id'], {})
    accounts = user.get('accounts', [])
    
    if not accounts:
        return jsonify({
            'total_balance': 0,
            'total_income': 0,
            'total_expenses': 0,
            'net_change': 0,
            'insights': []
        })
    
    # Load all account data
    all_transactions = []
    for account in accounts:
        try:
            df = pd.read_csv(account['filepath'])
            df['bank_name'] = account['bank_name']
            all_transactions.append(df)
        except Exception as e:
            print(f"Error loading {account['filepath']}: {e}")
    
    if not all_transactions:
        return jsonify({'error': 'No valid data found'}), 400
    
    # Combine all data
    combined_df = pd.concat(all_transactions, ignore_index=True)
    
    # Calculate metrics
    metrics = calculate_dashboard_metrics(combined_df)
    insights = generate_insights(combined_df)
    
    return jsonify({
        **metrics,
        'insights': insights,
        'account_count': len(accounts)
    })

# ------------------- Chat with AI -------------------
@app.route('/chat', methods=['POST'])
def chat():
    """Chat with AI using all account data as context"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    question = data.get('question', '')
    
    users = load_users()
    user = users.get(session['user_id'], {})
    accounts = user.get('accounts', [])
    
    if not accounts:
        return jsonify({'answer': 'Please upload at least one CSV file first!'})
    
    # Load all transaction data
    all_data = []
    for account in accounts:
        try:
            df = pd.read_csv(account['filepath'])
            df = normalize_csv(df)  # Ensure data is normalized
            df['bank_name'] = account['bank_name']
            all_data.append(df)
        except Exception as e:
            print(f"Error processing {account['filepath']}: {e}")
            continue
    
    if not all_data:
        return jsonify({'answer': 'Error loading your financial data.'})
    
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Create context with recent transactions and summary
    data_preview = combined_df.tail(20).to_string(index=False)
    
    # Add summary statistics
    summary_stats = f"""
    Total Accounts: {len(accounts)}
    Total Transactions: {len(combined_df)}
    Date Range: {combined_df['date'].min()} to {combined_df['date'].max()}
    """
    
    answer = ask_gemini(question, data_preview, summary_stats)
    return jsonify({'answer': answer})

# ------------------- Export PDF Report -------------------
@app.route('/export-pdf', methods=['GET'])
def export_pdf():
    """Generate and download PDF financial report"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    users = load_users()
    user = users.get(session['user_id'], {})
    accounts = user.get('accounts', [])
    
    if not accounts:
        return jsonify({'error': 'No accounts to export'}), 400
    
    # Load all data
    all_data = []
    for account in accounts:
        try:
            df = pd.read_csv(account['filepath'])
            df = normalize_csv(df)  # Ensure data is normalized
            df['bank_name'] = account['bank_name']
            all_data.append(df)
        except Exception as e:
            print(f"Error processing {account['filepath']}: {e}")
            continue
    
    combined_df = pd.concat(all_data, ignore_index=True)
    metrics = calculate_dashboard_metrics(combined_df)
    insights = generate_insights(combined_df)
    
    # Generate PDF
    pdf_path = generate_pdf_report(user, accounts, metrics, insights, combined_df)
    
    return send_file(pdf_path, as_attachment=True, download_name='financial_report.pdf')

# ------------------- Logout -------------------
@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return render_template('landing.html')

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode)
