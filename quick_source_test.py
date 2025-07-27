import sys
sys.path.insert(0, 'app')
from services.generator import generate_commentary
from routes.posts import ArticleInput

# Test empty source
article = ArticleInput(
    title='Test Empty Source',
    summary='Test article with empty source field to verify RSS Feeds fallback is working correctly',
    source='',
    link='https://example.com',
    post_style='punchy'
)

result = generate_commentary(article, post_style='punchy')
print('✅ Post with empty source (should show "RSS Feeds"):')
print('=' * 50)
post_lines = result['post'].split('\n')
for line in post_lines:
    if 'Source:' in line:
        print(f"SOURCE LINE: {line}")
        break
        
print('\nLast 150 characters:')
print(result['post'][-150:])
