def get_seo_data(keyword):
    """
    Get SEO data for a given keyword.
    For now, i am using mock data with realistic patterns.
    
    Args:
        keyword (str): The keyword to analyze
        
    Returns:
        dict: SEO metrics including search volume, keyword difficulty, and avg CPC
    """
    mock_seo_database = {
        "wireless earbuds" : {
            "search_volume": 74000,
            "keyword_difficulty": 78,
            "avg_cpc": 1.85
        },
        "best laptops": {
            "search_volume": 135000,
            "keyword_difficulty": 82,
            "avg_cpc": 2.15
        },
        "coffee maker": {
            "search_volume": 60500,
            "keyword_difficulty": 65,
            "avg_cpc": 1.45
        },
        "running shoes": {
            "search_volume": 201000,
            "keyword_difficulty": 75,
            "avg_cpc": 1.92
        },
        "smartphone": {
            "search_volume": 823000,
            "keyword_difficulty": 88,
            "avg_cpc": 2.85
        }        
    }
    normalized_keyword = keyword.lower().strip()
    if normalized_keyword in mock_seo_database:
        seo_data = mock_seo_database[normalized_keyword].copy()
        print(f"Found data for '{keyword}'")
    else:
        seo_data = {
            "search_volume": 25000,
            "keyword_difficulty": 50,
            "avg_cpc": 1.25
        }    
        print(f"Generated fallback data for '{keyword}'")
    seo_data["keyword"] = keyword
    seo_data["data_source"] = "mock_api"
    
    return seo_data
    
if __name__ == "__main__":
    print("Testing SEO Fetcher...")
    
    # Testing with known keyword
    result1 = get_seo_data("wireless earbuds")
    print("Known keyword result:")
    print(result1)
    print()
    
    # Testing with unknown keyword  
    result2 = get_seo_data("magic flying carpet")
    print("Unknown keyword result:")
    print(result2)
    print()
    
    # Testing with different case
    result3 = get_seo_data("COFFEE MAKER")
    print("Different case result:")
    print(result3)