import os
import re
from dotenv import load_dotenv
from seo_fetcher import get_seo_data

load_dotenv()

try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    OPENAI_AVAILABLE = True if openai.api_key else False
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI package not available")


print(f"OPENAI_AVAILABLE = {OPENAI_AVAILABLE}")

def generate_blog_post(keyword, seo_data):
    """
    Generate a blog post using OpenAI API based on keyword and SEO data
    Args:
        keyword (str): The target keyword for the blog post
        seo_data (dict): Complete SEO metrics including volume, difficulty, CPC
        
    Returns:
        str: Generated blog post content with affiliate links
    """
    print(f"Generating blog post for keyword: {keyword}")
    
    # Check if OpenAI is available
    if not OPENAI_AVAILABLE:
        print("OpenAI not available, using fallback content")
        return "This would be fallback content for: " + keyword
    else:
        print("OpenAI available but real API call not implemented yet")
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {
                        "role" : "system",
                        "content" : "You are an expert blog writer."
                    },
                    {
                        "role" : "user",
                        "content" : f"Write a 200-word blog post about {keyword}."
                    }
                ],
                max_tokens = 300,
                temperature = 0.7
            )
            blog_content = response.choices[0].message.content.strip()
            print("OpenAI API call successful!")
            return blog_content
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"API failed, fallback content for: {keyword}"
    
if __name__ == "__main__":
    keyword_given = "coffee maker"
    seo_data = get_seo_data(keyword_given)
    test_result = generate_blog_post(keyword_given,seo_data)
    print("Result : ", test_result)
    
    