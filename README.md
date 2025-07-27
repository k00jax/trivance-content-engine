# Trivance AI Content Engine

An AI-powered content management system for RSS feeds, automated post generation, and subscriber management.

## Features

- 📡 **RSS Feed Management**: Add, remove, and monitor RSS feeds with persistent storage
- ✍️ **AI Post Generation**: Generate intelligent Trivance-aligned LinkedIn content with optional GPT integration
- 🤖 **Smart Article Selection**: Automatic or manual article selection from RSS feeds with relevance scoring
- 📬 **Subscriber Management**: Maintain subscriber lists with local data storage
- 🎯 **Streamlit Dashboard**: User-friendly web interface for all operations
- 💾 **Local Data Persistence**: All data survives server restarts using JSON storage
- 📊 **Article Scoring**: Intelligent relevance scoring for SMB AI strategy content

## RSS-Powered Content Generation

The app now includes sophisticated RSS article analysis and selection:

**Auto-Select Mode (Recommended)**:
- 🎯 Automatically finds the highest-scoring article across all feeds
- 🧠 Uses intelligent scoring based on SMB AI relevance
- ⚡ One-click generation from top content

**Manual Selection Mode**:
- 📋 Browse articles from specific RSS feeds
- 📊 See relevance scores for each article
- 🔍 Preview article content before generation
- 🎪 Full control over content selection

### Article Scoring Algorithm
Articles are scored based on:
- **Keywords**: AI, automation, business, productivity, SMB-related terms
- **Content Quality**: Article length and depth
- **Relevance**: Focus on practical business applications
- **Recency**: Preference for recent content (configurable)

Higher scores indicate better fit for Trivance AI's SMB-focused content strategy.

## Content Generation

The app includes sophisticated content generation with two modes and three styles:

**Template-Based (Default)**:
- Multiple dynamic templates with Trivance AI voice
- Automatic hashtag generation based on content
- No API costs or external dependencies
- Consistent brand messaging

**GPT-Powered (Optional)**:
- OpenAI GPT integration for more dynamic content
- Context-aware post generation
- Natural language variation
- Requires OpenAI API key

### Content Styles
- 🎯 **Consultative**: Strategic, framework-based, professional tone
- ⚡ **Punchy**: Short sentences, bold claims, scroll-stopping style  
- 💬 **Casual**: Friendly, conversational, uses analogies

### Enhanced Features
- 📊 **Content Accuracy**: Posts now include specific facts, stats, and quotes from articles
- 🔍 **Key Insights**: Automatic extraction of important data points
- 🎪 **Style Control**: Three distinct writing styles for different content approaches
- 📈 **SMB Focus**: All content aligned with small business AI strategy

## Data Persistence

The application now includes robust local data persistence:

- **RSS Feeds**: Stored in `data/feeds.json`
- **Subscribers**: Stored in `data/subscribers.json` 
- **Generated Posts**: Stored in `data/posts.json`

All data survives across Streamlit sessions and server restarts. The app automatically creates the data directory and files on first run.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Optional: Enable GPT Integration**:
   ```bash
   pip install openai
   set USE_OPENAI_GPT=true
   set OPENAI_API_KEY=your-api-key-here
   ```

3. **Initialize Sample Data** (optional):
   ```bash
   python init_sample_data.py
   ```

4. **Start the API Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Launch the Streamlit Dashboard**:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

6. **Test RSS Functionality**:
   ```bash
   python test_rss.py
   ```

7. **Test API Endpoints**:
   ```bash
   python test_api.py
   ```

## API Endpoints

### Feeds Management
- `POST /feeds/` - Add RSS feed
- `GET /feeds/` - List all feeds
- `DELETE /feeds/` - Remove feed

### RSS Article Processing
- `GET /feeds/articles?feed_name={name}` - Get articles from specific feed
- `GET /feeds/top-article` - Get highest-scoring article from all feeds
- `GET /feeds/articles/all` - Get all articles from all feeds with scores

### Content Generation
- `POST /posts/generate` - Generate AI post from article data
- `GET /posts/` - Get recent posts
- `GET /posts/all` - Get all posts

### Subscribers
- `GET /subscribers/` - List subscribers
- `POST /subscribers/` - Add subscriber

## Future Database Integration

The codebase is designed for easy migration to external databases (Supabase, SQLite, etc.). See `app/services/persistence.py` for database interface stubs and migration planning.

## Project Structure

```
trivance-content-engine/
├── app/
│   ├── models/          # Data models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic & persistence
│   └── main.py          # FastAPI app
├── data/                # Local JSON storage (gitignored)
├── ui/
│   └── streamlit_app.py # Dashboard interface
├── db/                  # Database schemas
└── tests/               # Test files
```