"""
Test content vault functionality
"""
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.content_vault import content_vault

print("📁 Content Vault Test")
print("=" * 40)

# Test storing a sample post
sample_metadata = {
    "method": "template_test",
    "style_used": "trivance_default", 
    "platform": "LinkedIn",
    "generation_time": 0.5,
    "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
}

sample_post = """🔍 AI Automation Boosts Small Business Efficiency by 40%

Here's a specific takeaway: 40%

At Trivance AI, we believe in ⬩ logic ⬩ language ⬩ systems — because smart AI adoption is structured, not scattered.

Want a strategy that sticks?

Source: TechCrunch
https://example.com/article

#AI #TrivanceAI #SmallBusiness #Automation #Efficiency"""

try:
    content_vault.store_successful_post(
        "Test Article: AI Automation Success",
        sample_post,
        sample_metadata
    )
    
    print("\n📊 Vault Stats:")
    stats = content_vault.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n📝 Recent Posts:")
    recent = content_vault.get_recent_successes(2)
    for i, post in enumerate(recent, 1):
        print(f"  {i}. {post['article_title']} ({post['character_count']} chars)")
        
except Exception as e:
    print(f"❌ Vault test failed: {e}")
    import traceback
    traceback.print_exc()
