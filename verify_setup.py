"""
Verification Script for Finance AI Enhancements
Run this to check if all files are in place and configured correctly
"""

import os
import sys

def check_file(path, description):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory(path, description):
    """Check if a directory exists"""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("=" * 60)
    print("Finance AI Enhancement Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check directories
    print("📁 Checking Directories...")
    all_good &= check_directory("static", "Static folder")
    all_good &= check_directory("templates", "Templates folder")
    all_good &= check_directory("User_data_samples", "Sample data folder")
    print()
    
    # Check new files
    print("📄 Checking New Files...")
    all_good &= check_file("static/styles.css", "CSS file")
    all_good &= check_file("static/app.js", "Main JS file")
    all_good &= check_file("static/charts.js", "Charts JS file")
    all_good &= check_file("static/i18n.js", "Translation JS file")
    all_good &= check_file("templates/index_enhanced.html", "Enhanced template")
    print()
    
    # Check modified files
    print("🔧 Checking Modified Files...")
    all_good &= check_file("process_data.py", "Data processor")
    all_good &= check_file("app.py", "Flask app")
    print()
    
    # Check sample CSV files
    print("📊 Checking Sample CSV Files...")
    all_good &= check_file("User_data_samples/hdfc_savings_account.csv", "HDFC CSV")
    all_good &= check_file("User_data_samples/icici_credit_card.csv", "ICICI CSV")
    all_good &= check_file("User_data_samples/zerodha_demat_account.csv", "Zerodha CSV")
    all_good &= check_file("User_data_samples/sample_data.csv", "Sample CSV")
    print()
    
    # Check if app.py uses enhanced template
    print("🔍 Checking Configuration...")
    try:
        with open("app.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if 'index_enhanced.html' in content:
                print("✅ app.py is configured to use enhanced template")
            else:
                print("⚠️  app.py is NOT using enhanced template - update manually!")
                all_good = False
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        all_good = False
    print()
    
    # Check if normalize_csv is updated
    print("🔍 Checking CSV Parser...")
    try:
        with open("process_data.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if 'date_formats' in content and 'normalize_csv' in content:
                print("✅ CSV parser has enhanced date handling")
            else:
                print("⚠️  CSV parser might not be fully updated")
    except Exception as e:
        print(f"❌ Error reading process_data.py: {e}")
        all_good = False
    print()
    
    # Final summary
    print("=" * 60)
    if all_good:
        print("🎉 All checks passed! Your setup is ready!")
        print()
        print("Next steps:")
        print("1. Run: python app.py")
        print("2. Navigate to: http://localhost:5000")
        print("3. Test CSV uploads from User_data_samples/")
        print("4. Try dark mode (🌙 button)")
        print("5. Switch languages (dropdown)")
        print("6. View Analytics tab after uploading data")
    else:
        print("⚠️  Some files are missing or not configured correctly.")
        print("Please check the messages above and fix any issues.")
    print("=" * 60)

if __name__ == "__main__":
    main()
