#!/usr/bin/env python3
"""Clean up existing posts.json to fix HTML entities"""

import json
import sys
import os
sys.path.append('.')

from app.services.rss import clean_html

def clean_posts_file():
    """Clean HTML entities from existing posts in posts.json"""
    posts_file = "data/posts.json"
    
    if not os.path.exists(posts_file):
        print(f"❌ {posts_file} not found")
        return
    
    # Load existing posts
    try:
        with open(posts_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except Exception as e:
        print(f"❌ Error loading {posts_file}: {e}")
        return
    
    print(f"Found {len(posts)} posts in {posts_file}")
    
    # Clean HTML entities from summaries and generated content
    cleaned_count = 0
    for post in posts:
        original_summary = post.get('summary', '')
        original_content = post.get('generated_content', '')
        
        # Clean the summary
        if original_summary and ('&#38;' in original_summary or '&#8212;' in original_summary):
            post['summary'] = clean_html(original_summary)
            cleaned_count += 1
            print(f"✅ Cleaned summary for: {post.get('title', 'Unknown')[:50]}...")
        
        # Clean the generated content 
        if original_content and ('&#38;' in original_content or '&#8212;' in original_content):
            post['generated_content'] = clean_html(original_content)
            cleaned_count += 1
            print(f"✅ Cleaned content for: {post.get('title', 'Unknown')[:50]}...")
    
    if cleaned_count > 0:
        # Backup original file
        backup_file = f"{posts_file}.backup"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"📄 Backup saved to {backup_file}")
        
        # Save cleaned posts
        with open(posts_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Cleaned {cleaned_count} entries in {posts_file}")
    else:
        print("ℹ️  No HTML entities found to clean")

if __name__ == "__main__":
    print("=" * 60)
    print("CLEANING EXISTING POSTS.JSON")
    print("=" * 60)
    clean_posts_file()
    print("=" * 60)
    print("CLEANUP COMPLETE")
    print("=" * 60)
