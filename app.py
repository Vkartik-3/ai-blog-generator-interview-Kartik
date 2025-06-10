from flask import Flask,jsonify,request
import os
from datetime import datetime
import json
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from seo_fetcher import get_seo_data
from ai_generator import generate_blog_post

load_dotenv()
app = Flask(__name__)

# print(f"__name__ is: {__name__}")
# app = Flask(__name__)
# print(f"Flask app name is: {app.name}")

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/generate',methods=['GET'])
def generate():
    """
    API endpoint to generate a blog post for a given keyword
    Usage: GET /generate?keyword=your_keyword
    """
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({
                'error': 'Keyword parameter is required',
                'usage': '/generate?keyword=your_keyword'
            }),400
        print(f"API request for keyword: {keyword}")
        seo_data = get_seo_data(keyword)
        blog_content = generate_blog_post(keyword,seo_data)
        
        result = {
            'keyword': keyword,
            'seo_data': seo_data,
            'blog_post': blog_content,
            'generated_at': datetime.now().isoformat(),
            'status': 'success'
        }
        return jsonify(result)
    except Exception as e:
        print(f"Error in API: {str(e)}")
        return jsonify({
            'error': f'Failed to generate blog post: {str(e)}',
            'status': 'error'
        }), 500
        
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'AI Blog Generator API is running'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with usage instructions"""
    return jsonify({
        'message': 'AI Blog Post Generator API',
        'version': '1.0',
        'endpoints': {
            '/generate?keyword=<keyword>': 'Generate a blog post for the specified keyword',
            '/health': 'Check API health status',
            '/': 'This help message'
        },
        'example': '/generate?keyword=wireless%20earbuds',
        'documentation': 'Send GET request to /generate with keyword parameter'
    })

def daily_blog_generation():
    """
    Function that runs daily to generate a blog post for a predefined keyword
    """
    try:
        predefined_keyword = "wireless earbuds"
        print(f"[DAILY JOB] Starting daily blog generation for keyword: {predefined_keyword}")
        
        # Get SEO data
        seo_data = get_seo_data(predefined_keyword)
        
        # Generate blog post
        blog_content = generate_blog_post(predefined_keyword, seo_data)
        
        # Save to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"daily_generated_post_{timestamp}.json"
        
        daily_result = {
            'keyword': predefined_keyword,
            'seo_data': seo_data,
            'blog_post': blog_content,
            'generated_at': datetime.now().isoformat(),
            'type': 'daily_automated'
        }
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(daily_result, f, indent=2, ensure_ascii=False)
        
        print(f"[DAILY JOB] Blog post saved to {filename}")
        print(f"[DAILY JOB] Daily generation completed successfully")
        
    except Exception as e:
        print(f"[DAILY JOB] Error in daily blog generation: {str(e)}")

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Ensure scheduler shuts down when app exits
atexit.register(lambda: scheduler.shutdown())

@app.route('/test-daily', methods=['GET'])
def test_daily():
    """Test the daily generation manually"""
    daily_blog_generation()
    return jsonify({"message": "Daily generation triggered manually"})

if __name__ == "__main__":
    scheduler.add_job(
        func=daily_blog_generation,
        trigger=CronTrigger(hour=10, minute=0),
        id='daily_blog_job',
        name='Daily Blog Post Generation',
        replace_existing=True
    )
    print("AI Blog Post Generator API starting...")
    print("Available endpoints:")
    print("   - GET /generate?keyword=<keyword>")
    print("   - GET /health")
    print("   - GET /")
    print("   - GET /test-daily")
    print("Daily automation scheduled for 10:00 AM") 
    print("Server will run on: http://localhost:5001") 
    app.run(debug=True,host='0.0.0.0', port=5001)
else:
    print("File was imported, not starting server")