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
                        "content" : f"""Write a 200-word blog post about {keyword}
                        Include 2-3 product recommendations and use these placeholders for affiliate links:
                            - {{{{AFF_LINK_1}}}} for the first product recommendation
                            - {{{{AFF_LINK_2}}}} for the second product recommendation  
                            - {{{{AFF_LINK_3}}}} for the third product recommendation

                        Make the content engaging and helpful with natural product recommendations.
                        """
                    }
                ],
                max_tokens = 300,
                temperature = 0.7
            )
            blog_content = response.choices[0].message.content.strip()
            blog_content = replace_aff_placeholder(blog_content,keyword)
            print("OpenAI API call successful!")
            return blog_content
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return f"API failed, fallback content for: {keyword}"
        
def replace_aff_placeholder(content,keyword):
    """
    Replace affiliate link placeholders with dummy URLs
    """
    keyword_slug = keyword.lower().replace(' ','-').replace('_','-')
    dummy_affiliates = {
        '{{AFF_LINK_1}}' : f'https://amazon-affiliate.com/best-{keyword_slug}-recommendation-1?ref=ai-blog',
        '{{AFF_LINK_2}}': f'https://affiliate-network.com/{keyword_slug}-top-choice?source=blog-ai',
        '{{AFF_LINK_3}}': f'https://product-affiliate.com/recommended-{keyword_slug}-deals?utm_source=ai-generated'
    }
    for placeholder,dummy_url in dummy_affiliates.items():
        content = content.replace(placeholder,dummy_url)
    return content

def test_aff_replace():
    test_content = """sumary_line
        Check out {{AFF_LINK_1}} for the best choice and {{AFF_LINK_2}} for budget option.
    Also consider {{AFF_LINK_3}} for premium features.
    """
    result = replace_aff_placeholder(test_content,'coffee-maker')
    print("Testing affiliate replacement : ")
    print(result)    
    
if __name__ == "__main__":
    # test_aff_replace()
    # print("\n" + "="*50 + "\n")
    keyword_given = "coffee maker"
    seo_data = get_seo_data(keyword_given)
    test_result = generate_blog_post(keyword_given,seo_data)
    print("Result : ", test_result)
    
    