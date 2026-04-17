import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def normalize_csv(df):
    """
    Normalize different CSV formats to standard format with date, description, amount columns
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Normalize column names to lowercase and remove spaces
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    
    # Handle different date column names
    date_columns = ['date', 'transaction_date', 'trade_date']
    date_col = None
    for col in date_columns:
        if col in df.columns:
            date_col = col
            break
    
    if date_col:
        df.rename(columns={date_col: 'date'}, inplace=True)
    else:
        raise ValueError("No date column found in CSV")
    
    # Handle different description column names
    desc_columns = ['description', 'merchant', 'symbol', 'transaction_type', 'remarks', 'category']
    desc_col = None
    for col in desc_columns:
        if col in df.columns:
            desc_col = col
            break
    
    if desc_col:
        df.rename(columns={desc_col: 'description'}, inplace=True)
    else:
        # Create description column if not found
        df['description'] = 'Transaction'
    
    # Handle amount column - this is the most complex part
    if 'amount' in df.columns:
        # Already has amount column - just ensure it's numeric
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    elif 'deposit' in df.columns and 'withdrawal' in df.columns:
        # Bank statement format (HDFC style)
        df['deposit'] = pd.to_numeric(df['deposit'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['withdrawal'] = pd.to_numeric(df['withdrawal'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        df['interest'] = pd.to_numeric(df.get('interest', 0), errors='coerce').fillna(0)
        
        # Combine: deposits and interest are positive, withdrawals are negative
        df['amount'] = df['deposit'] + df['interest'] - df['withdrawal']
    elif 'net_amount' in df.columns:
        # Investment format (Zerodha style)
        df['net_amount'] = pd.to_numeric(df['net_amount'].astype(str).str.replace(',', ''), errors='coerce')
        
        # Determine if transaction is buy/sell based on transaction_type or amount sign
        if 'transaction_type' in df.columns:
            # Buy = negative (money out), Sell/Dividend = positive (money in)
            df['amount'] = df.apply(lambda row: 
                -abs(row['net_amount']) if str(row.get('transaction_type', '')).lower() == 'buy' 
                else abs(row['net_amount']), axis=1)
        else:
            df['amount'] = df['net_amount']
    elif 'total_value' in df.columns:
        # Alternative investment format
        df['total_value'] = pd.to_numeric(df['total_value'].astype(str).str.replace(',', ''), errors='coerce')
        df['fees'] = pd.to_numeric(df.get('fees', 0), errors='coerce').fillna(0)
        
        if 'transaction_type' in df.columns:
            df['amount'] = df.apply(lambda row: 
                -(row['total_value'] + row['fees']) if str(row.get('transaction_type', '')).lower() == 'buy' 
                else (row['total_value'] - row['fees']), axis=1)
        else:
            df['amount'] = df['total_value'] - df['fees']
    else:
        # No recognizable amount column
        raise ValueError("Could not find amount columns in CSV. Expected: 'amount', 'deposit/withdrawal', 'net_amount', or 'total_value'")
    
    # Ensure we have the required columns
    required = ['date', 'description', 'amount']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        raise ValueError(f"Missing required columns after normalization: {missing}")
    
    # Convert date - try multiple formats
    date_formats = ['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format='mixed', dayfirst=True)
    
    # If date parsing failed, try each format explicitly
    if df['date'].isna().all():
        for fmt in date_formats:
            try:
                df['date'] = pd.to_datetime(df['date'], format=fmt, errors='coerce')
                if not df['date'].isna().all():
                    break
            except:
                continue
    
    # Convert amount to numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Fill empty descriptions
    df['description'] = df['description'].fillna('Transaction')
    
    # Enhance description for better categorization
    if 'category' in df.columns and 'merchant' in df.columns:
        df['description'] = df['merchant'] + ' - ' + df['category']
    elif 'merchant' in df.columns:
        df['description'] = df['merchant']
    
    # Return only the required columns, dropping rows with NaN dates or amounts
    result = df[['date', 'description', 'amount']].copy()
    result = result.dropna(subset=['date', 'amount'])
    
    return result


def process_csv(df):
    """
    Process uploaded CSV and extract basic information
    """
    try:
        # Normalize the CSV format
        df = normalize_csv(df)
        
        # Remove rows with NaN amounts or dates
        df = df.dropna(subset=['amount', 'date'])
        
        # Calculate total balance
        total_balance = df['amount'].sum()
        
        summary = {
            "columns": df.columns.tolist(),
            "rows": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "total_balance": float(total_balance),
            "date_range": {
                "start": str(df['date'].min().date()) if not df['date'].isna().all() else None,
                "end": str(df['date'].max().date()) if not df['date'].isna().all() else None
            },
            "preview": df.head(5).to_dict(orient="records")
        }
        return summary
        
    except Exception as e:
        return {"error": str(e)}


def calculate_dashboard_metrics(df):
    """
    Calculate comprehensive financial metrics from transaction data
    """
    try:
        # Normalize if not already normalized
        if 'amount' not in df.columns or 'date' not in df.columns:
            df = normalize_csv(df)
        
        # Ensure date column is datetime and amount is numeric
        df = df.copy()  # Avoid SettingWithCopyWarning
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Remove any rows with NaN amounts or dates
        df = df.dropna(subset=['amount', 'date'])
        
        # Separate income and expenses
        income = df[df['amount'] > 0]['amount'].sum()
        expenses = abs(df[df['amount'] < 0]['amount'].sum())
        net_change = income - expenses
        
        # Calculate current balance
        total_balance = df['amount'].sum()
        
        # Monthly breakdown
        df['month'] = df['date'].dt.to_period('M')
        monthly_summary = df.groupby('month')['amount'].sum().to_dict()
        monthly_summary = {str(k): float(v) for k, v in monthly_summary.items()}
        
        # Daily spending (rolling 30 days from the latest data point)
        df_sorted = df.sort_values('date')
        if not df_sorted.empty and not df_sorted['date'].isna().all():
            max_date = df_sorted['date'].max()
            start_date = max_date - timedelta(days=30)
            last_30_days = df_sorted[df_sorted['date'] >= start_date]
            daily_spending = last_30_days.groupby(last_30_days['date'].dt.date)['amount'].sum().to_dict()
        else:
            daily_spending = {}
        
        daily_spending = {str(k): float(v) for k, v in daily_spending.items()}
        
        # Category analysis
        categories = categorize_transactions(df)
        
        # Top expenses
        top_expenses = df[df['amount'] < 0].nlargest(10, 'amount', keep='first')[['date', 'description', 'amount']].to_dict('records')
        top_expenses = [{**exp, 'date': str(exp['date'].date()), 'amount': float(exp['amount'])} for exp in top_expenses]
        
        # Spending trends
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_month_df = df[(df['date'].dt.month == current_month) & 
                              (df['date'].dt.year == current_year)]
        current_month_spending = abs(current_month_df[current_month_df['amount'] < 0]['amount'].sum())
        
        # Previous month
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        prev_month_df = df[(df['date'].dt.month == prev_month) & 
                          (df['date'].dt.year == prev_year)]
        prev_month_spending = abs(prev_month_df[prev_month_df['amount'] < 0]['amount'].sum())
        
        # Calculate percentage change
        if prev_month_spending > 0:
            spending_change_pct = ((current_month_spending - prev_month_spending) / prev_month_spending) * 100
        else:
            spending_change_pct = 0
        
        return {
            "total_balance": float(total_balance),
            "total_income": float(income),
            "total_expenses": float(expenses),
            "net_change": float(net_change),
            "monthly_summary": monthly_summary,
            "daily_spending": daily_spending,
            "categories": categories,
            "top_expenses": top_expenses,
            "current_month_spending": float(current_month_spending),
            "prev_month_spending": float(prev_month_spending),
            "spending_change_pct": float(spending_change_pct)
        }
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        import traceback
        traceback.print_exc()
        return {
            "total_balance": 0,
            "total_income": 0,
            "total_expenses": 0,
            "net_change": 0,
            "error": str(e)
        }


def categorize_transactions(df):
    """
    Categorize transactions based on description keywords
    """
    categories = {
        "Food & Dining": ["swiggy", "zomato", "restaurant", "food", "cafe", "dinner", "lunch", "dominos", "pizza", "meal", "delivery"],
        "Shopping": ["amazon", "flipkart", "myntra", "shopping", "purchase", "croma", "online"],
        "Bills & Utilities": ["electricity", "water", "gas", "bill", "recharge", "utilities", "mobile"],
        "Transportation": ["uber", "ola", "petrol", "fuel", "parking", "indigo", "makemytrip", "cab", "travel", "flight", "hotel"],
        "Entertainment": ["netflix", "prime", "spotify", "movie", "game", "bookmyshow", "entertainment"],
        "Investment": ["mutual fund", "dividend", "stock", "sip", "reliance", "tcs", "infy", "hdfc", "axis", "sbin", "icici", "buy", "sell", "trade"],
        "Salary & Income": ["salary", "income", "credit"],
        "ATM & Cash": ["atm", "withdrawal", "cash"],
        "Rent & Housing": ["rent", "housing", "transfer"],
        "Insurance": ["insurance", "premium"],
        "Sports & Fitness": ["gym", "decathlon", "sports", "fitness", "gear"],
        "Groceries": ["grocery", "bigbasket"],
        "Electronics": ["apple", "electronics", "gadget", "appliance", "accessories"]
    }
    
    category_totals = {}
    
    for category, keywords in categories.items():
        mask = df['description'].str.lower().str.contains('|'.join(keywords), na=False, regex=True)
        total = abs(df[mask]['amount'].sum())
        if total > 0:
            category_totals[category] = float(total)
    
    # Uncategorized
    categorized_mask = pd.Series([False] * len(df), index=df.index)
    for keywords in categories.values():
        categorized_mask |= df['description'].str.lower().str.contains('|'.join(keywords), na=False, regex=True)
    
    uncategorized = abs(df[~categorized_mask]['amount'].sum())
    if uncategorized > 0:
        category_totals["Other"] = float(uncategorized)
    
    return category_totals


def generate_insights(df):
    """
    Generate AI-like insights from financial data
    """
    insights = []
    
    try:
        # Normalize if needed
        if 'amount' not in df.columns:
            df = normalize_csv(df)
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['amount'])
        
        # Insight 1: Spending trend
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_month_df = df[(df['date'].dt.month == current_month) & 
                              (df['date'].dt.year == current_year)]
        current_month_spending = abs(current_month_df[current_month_df['amount'] < 0]['amount'].sum())
        
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        prev_month_df = df[(df['date'].dt.month == prev_month) & 
                          (df['date'].dt.year == prev_year)]
        prev_month_spending = abs(prev_month_df[prev_month_df['amount'] < 0]['amount'].sum())
        
        if prev_month_spending > 0:
            change_pct = ((current_month_spending - prev_month_spending) / prev_month_spending) * 100
            if change_pct > 10:
                insights.append({
                    "type": "warning",
                    "title": "Spending Alert",
                    "message": f"You've spent ₹{current_month_spending - prev_month_spending:,.0f} ({change_pct:.1f}%) more this month compared to last month."
                })
            elif change_pct < -10:
                insights.append({
                    "type": "success",
                    "title": "Great Job!",
                    "message": f"You've reduced spending by ₹{prev_month_spending - current_month_spending:,.0f} ({abs(change_pct):.1f}%) this month."
                })
        
        # Insight 2: Top spending category
        categories = categorize_transactions(df[df['amount'] < 0])
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1])
            insights.append({
                "type": "info",
                "title": "Top Spending Category",
                "message": f"{top_category[0]} accounts for ₹{top_category[1]:,.0f} of your expenses."
            })
        
        # Insight 3: Savings rate
        income = df[df['amount'] > 0]['amount'].sum()
        expenses = abs(df[df['amount'] < 0]['amount'].sum())
        if income > 0:
            savings_rate = ((income - expenses) / income) * 100
            if savings_rate > 20:
                insights.append({
                    "type": "success",
                    "title": "Strong Savings",
                    "message": f"You're saving {savings_rate:.1f}% of your income. Keep it up!"
                })
            elif savings_rate < 10:
                insights.append({
                    "type": "warning",
                    "title": "Low Savings Rate",
                    "message": f"Your savings rate is {savings_rate:.1f}%. Consider reducing non-essential expenses."
                })
        
        # Insight 4: High value transactions
        high_expenses = df[df['amount'] < -5000]
        if len(high_expenses) > 0:
            insights.append({
                "type": "info",
                "title": "Large Transactions",
                "message": f"You have {len(high_expenses)} transactions over ₹5,000 totaling ₹{abs(high_expenses['amount'].sum()):,.0f}."
            })
        
        # Insight 5: Average daily spending
        if len(df) > 0:
            days = (df['date'].max() - df['date'].min()).days + 1
            avg_daily_spending = abs(df[df['amount'] < 0]['amount'].sum()) / max(days, 1)
            insights.append({
                "type": "info",
                "title": "Daily Average",
                "message": f"Your average daily spending is ₹{avg_daily_spending:,.0f} over the past {days} days."
            })
        
    except Exception as e:
        print(f"Error generating insights: {e}")
    
    return insights
