# RSS-Powered Content Generation Guide

## Overview

The Trivance AI Content Engine now features sophisticated RSS article analysis and content generation capabilities. This guide covers how to use the new RSS-powered features effectively.

## 🚀 Quick Start

### 1. Add RSS Feeds
```bash
# Start the application
uvicorn app.main:app --reload
streamlit run ui/streamlit_app.py
```

Navigate to the **📡 Feeds** tab and add your RSS sources:
- TechCrunch AI: `https://techcrunch.com/tag/artificial-intelligence/feed/`
- MIT Technology Review: `https://www.technologyreview.com/feed/`
- AI News: `https://artificialintelligence-news.com/feed/`

### 2. Generate Content
Navigate to the **✍️ Generate Post** tab:

**Option A: Auto-Select Mode (Recommended)**
1. ✅ Check "Auto-generate from top article"
2. Click "🔍 Fetch Top Article"
3. Review the selected article
4. Click "🚀 Generate Post"

**Option B: Manual Selection**
1. ❌ Uncheck auto mode
2. Select a feed from the dropdown
3. Click "📰 Fetch Articles"
4. Choose an article by title and score
5. Click "🚀 Generate Post"

## 📊 Article Scoring System

### Scoring Criteria

Articles are automatically scored based on relevance to Trivance AI's SMB focus:

**Keywords (2-3 points each)**:
- AI, GPT, ChatGPT, automation
- business, strategy, productivity
- small business, startup, entrepreneur
- workflow, ops, efficiency

**Content Quality Bonuses**:
- +2 points: Articles over 50 words
- +1 point: Articles over 30 words
- +3 points: Keywords in title (weighted higher)

**Content Penalties**:
- -1 point: Academic/research content
- -1 point: Purely technical content

### Score Interpretation

- **15+ points**: Excellent fit for Trivance content
- **10-14 points**: Good relevance to SMB AI strategy
- **5-9 points**: Moderate relevance
- **0-4 points**: Low relevance

## 🛠️ API Usage

### Get Articles from Specific Feed
```bash
curl "http://localhost:8000/feeds/articles?feed_name=TechCrunch%20AI"
```

### Get Top Article Automatically
```bash
curl "http://localhost:8000/feeds/top-article"
```

### Get All Articles with Scores
```bash
curl "http://localhost:8000/feeds/articles/all"
```

## 🎯 Content Generation Options

### Post Styles
- **Consultative (default)**: Balanced, advisory tone
- **Educational**: Teaching-focused content
- **Strategic**: High-level business insights

### Generation Settings
- **Include Hashtags**: Toggle hashtag inclusion
- **Max Article Age**: Filter articles by recency (1-30 days)

## 🔍 Troubleshooting

### Common Issues

**"No articles found"**
- Check RSS feed URLs are valid
- Verify feeds contain recent content
- Some feeds may block automated access

**Low scores for relevant articles**
- Scoring algorithm focuses on SMB AI relevance
- Academic or highly technical content scores lower
- Consider manual selection for edge cases

**API errors**
- Ensure FastAPI server is running
- Check network connectivity for RSS parsing
- Some feeds may have rate limiting

### Debug Mode

Run with verbose output:
```bash
python test_rss.py  # Test RSS parsing
python test_api.py  # Test API endpoints
```

## 📈 Best Practices

### Feed Selection
- Choose feeds with business-focused AI content
- Avoid purely academic or research feeds
- Include variety: news, analysis, practical guides

### Content Generation
- Use auto-select for consistent quality
- Review article previews before generation
- Manually select for specific topics or angles

### Quality Control
- Review generated posts before publishing
- Adjust generation settings based on content type
- Use manual entry for custom content

## 🔮 Future Enhancements

### Planned Features
- **GPT-based scoring**: Use AI to evaluate article relevance
- **Content filtering**: Advanced filters by topic, sentiment
- **Scheduling**: Automatic content generation and posting
- **Analytics**: Track performance of different content sources

### Configuration Options
```python
# In app/services/rss.py - customize scoring
SCORING_KEYWORDS = ["your", "custom", "keywords"]
MIN_ARTICLE_LENGTH = 30  # words
MAX_ARTICLE_AGE = 7      # days
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API endpoint documentation
3. Test with the provided test scripts
4. Verify RSS feed accessibility manually
