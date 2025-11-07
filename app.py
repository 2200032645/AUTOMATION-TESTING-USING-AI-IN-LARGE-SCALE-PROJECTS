# ai_testing_app/app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv 

# Load environment variables from .env file immediately
load_dotenv() 

# Import the core logic 
from core.ai_agent import AITestingAgent 

app = Flask(__name__)

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """Displays the search bar page."""
    if request.method == 'POST':
        target_url = request.form.get('url')
        if target_url:
            return redirect(url_for('run_test_and_show_report', url=target_url))
        
    return render_template('index.html')

@app.route('/report')
def run_test_and_show_report():
    """Runs the AI test and displays the results."""
    target_url = request.args.get('url')

    if not target_url:
        return redirect(url_for('index'))

    # Check for API key BEFORE running the agent
    if not os.getenv('GEMINI_API_KEY'):
        error_msg = "FATAL ERROR: GEMINI_API_KEY not found in environment. Did you set it in Railway Variables?"
        return render_template(
            'report.html', 
            report={'url': target_url, 'actions': [{'step': 1, 'action': error_msg, 'status': 'FATAL_ERROR'}], 'summary': 'Setup Error'},
            success=False
        )

    try:
        # 1. Initialize and run the autonomous agent
        agent = AITestingAgent(target_url)
        final_report = agent.run_tests()
        
        # 2. Display the final report
        return render_template(
            'report.html', 
            report=final_report, 
            success=True
        )

    except Exception as e:
        error_message = f"FATAL ERROR during test execution: {e}. Check your Chrome WebDriver setup."
        return render_template(
            'report.html', 
            report={'url': target_url, 'actions': [{'step': 1, 'action': error_message, 'status': 'FATAL_ERROR'}], 'summary': 'Execution Failed'},
            success=False
        )


# ✅ Required update for Railway Deployment
if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    print(f"✅ Flask server running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT)
