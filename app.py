from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load datasets with different variable names
predictor_df = pd.read_csv('jossa_combined.csv')
college_df = pd.read_csv('all college.csv', encoding='latin1')

# Make sure rank columns are numeric in predictor_df
predictor_df['Opening Rank'] = pd.to_numeric(predictor_df['Opening Rank'], errors='coerce')
predictor_df['Closing Rank'] = pd.to_numeric(predictor_df['Closing Rank'], errors='coerce')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')
@app.route('/mbbs')
def mbbs():
    return render_template('mbbs.html')

@app.route('/searchcollege', methods=['GET', 'POST'])
def searchcollege():
    college_info = None
    if request.method == 'POST':
        query = request.form['college_name']
        result = college_df[college_df['Name'].str.contains(query, case=False, na=False)]
        if not result.empty:
            college_info = result.to_dict('records')
    return render_template('searchcollege.html', college_info=college_info)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/openclose', methods=['POST'])
def openclose():
    # Get form data
    category = request.form.get('category', '').strip()
    gender = request.form.get('gender', '').strip()
    quota = request.form.get('quota', '').strip()
    round_num = request.form.get('round', '').strip()
    university_type = request.form.get('university_type', '').strip()
    rank = request.form.get('rank', '').strip()

    filtered = predictor_df.copy()  # Use predictor_df, not df!

    # Apply filters
    if category:
        filtered = filtered[filtered['Category'].str.lower() == category.lower()]

    if gender:
        filtered = filtered[filtered['Gender'].str.lower() == gender.lower()]

    if quota:
        filtered = filtered[filtered['Quota'].str.lower() == quota.lower()]

    if round_num:
        try:
            round_num = int(round_num)
            filtered = filtered[filtered['Round'] == round_num]
        except ValueError:
            pass

    if university_type:
        filtered = filtered[filtered['Type Of University'].str.lower() == university_type.lower()]

    if rank:
        try:
            rank = int(rank)
            filtered = filtered[
                (filtered['Opening Rank'] <= rank) & 
                (filtered['Closing Rank'] >= rank)
            ]
        except ValueError:
            pass

    if not filtered.empty:
        table_html = filtered.to_html(classes='table table-bordered', index=False)
    else:
        table_html = "<p style='color:red;'>No matching records found.</p>"

    return render_template('result.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
