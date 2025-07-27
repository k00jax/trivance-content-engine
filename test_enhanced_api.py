"""
Test the enhanced post generation API with style control.
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_enhanced_generation():
    """Test post generation with different styles."""
    
    sample_article = {
        "title": "Small Business AI Adoption Surges 75% in Q4",
        "summary": "New research from TechBiz Analytics shows small business AI adoption increased 75% in Q4 2024. The study of 1,200 companies found that 68% are using AI for customer service, while 45% leverage it for inventory management. 'We're seeing a fundamental shift in how SMBs approach technology,' said lead researcher Dr. Maria Santos. Companies report average cost savings of $15,000 annually.",
        "source": "TechBiz Analytics",
        "link": "https://example.com/smb-ai-study",
        "post_style": "consultative"
    }
    
    styles = ["consultative", "punchy", "casual"]
    
    print("🧪 Testing Enhanced Post Generation API")
    print("=" * 60)
    
    for style in styles:
        print(f"\n📝 Testing {style.upper()} style...")
        
        # Update the style for this test
        sample_article["post_style"] = style
        
        try:
            response = requests.post(f"{API_URL}/posts/generate", json=sample_article)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Status: {response.status_code}")
                print(f"Method: {result.get('method', 'unknown')}")
                print(f"Style used: {result.get('style_used', 'unknown')}")
                print(f"Key insights: {len(result.get('key_insights', []))} found")
                
                print("\nGenerated Post:")
                print("-" * 40)
                print(result["post"][:300] + "..." if len(result["post"]) > 300 else result["post"])
                print("-" * 40)
                
                # Check if specific details are included
                post_content = result["post"].lower()
                if "75%" in post_content:
                    print("✅ Article statistic (75%) found in post")
                else:
                    print("❌ Article statistic not found in post")
                
                if "santos" in post_content or "fundamental shift" in post_content:
                    print("✅ Quote/authority referenced")
                else:
                    print("❌ Quote/authority not referenced")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except requests.ConnectionError:
            print("❌ Cannot connect to API. Start server with: uvicorn app.main:app --reload")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    test_enhanced_generation()
    
    print("\n🎯 Test Summary:")
    print("- Each style should produce different content structure")
    print("- Posts should include specific facts from the article")
    print("- Style control should be working properly")
    print("- Generation details should show correct style usage")
    
    print("\n📋 Manual Verification Steps:")
    print("1. Check that consultative style uses frameworks")
    print("2. Verify punchy style has short, bold sentences")
    print("3. Confirm casual style is conversational")
    print("4. Ensure article statistics/quotes are included")
