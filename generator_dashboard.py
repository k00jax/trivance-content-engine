"""
Generator Performance Dashboard
"""
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.content_vault import content_vault

def display_dashboard():
    print("🎯 Trivance AI Content Generator Dashboard")
    print("=" * 50)
    
    stats = content_vault.get_stats()
    
    if stats["total_posts"] == 0:
        print("📭 No successful generations recorded yet")
        return
    
    print(f"📊 PERFORMANCE METRICS")
    print(f"   Total successful posts: {stats['total_posts']}")
    print(f"   Average post length: {stats['average_length']} characters")
    print(f"   Latest generation: {stats['latest_post']}")
    
    print(f"\n🤖 GENERATION METHODS")
    for method, count in stats['methods_used'].items():
        percentage = (count / stats['total_posts']) * 100
        print(f"   {method}: {count} posts ({percentage:.1f}%)")
    
    print(f"\n🎨 STYLE DISTRIBUTION") 
    for style, count in stats['styles_used'].items():
        percentage = (count / stats['total_posts']) * 100
        print(f"   {style}: {count} posts ({percentage:.1f}%)")
    
    print(f"\n📝 RECENT SUCCESSES")
    recent_posts = content_vault.get_recent_successes(3)
    for i, post in enumerate(recent_posts, 1):
        timestamp = post['timestamp'][:19].replace('T', ' ')
        print(f"   {i}. {post['article_title']}")
        print(f"      Method: {post['method']} | Style: {post['style_used']} | {post['character_count']} chars")
        print(f"      Generated: {timestamp}")
        if 'token_usage' in post and post['token_usage'].get('total_tokens', 0) > 0:
            tokens = post['token_usage']['total_tokens']
            print(f"      Tokens used: {tokens}")
        print()

if __name__ == "__main__":
    display_dashboard()
