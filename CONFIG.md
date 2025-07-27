# Trivance AI Content Engine Configuration

## Environment Variables

### OpenAI GPT Integration (Optional)

To enable OpenAI GPT-powered content generation:

1. **Install OpenAI library:**
   ```bash
   pip install openai
   ```

2. **Set environment variables:**
   ```bash
   # Windows (Command Prompt)
   set USE_OPENAI_GPT=true
   set OPENAI_API_KEY=your-api-key-here

   # Windows (PowerShell)
   $env:USE_OPENAI_GPT="true"
   $env:OPENAI_API_KEY="your-api-key-here"

   # Linux/Mac
   export USE_OPENAI_GPT=true
   export OPENAI_API_KEY=your-api-key-here
   ```

3. **Or create a `.env` file:**
   ```
   USE_OPENAI_GPT=true
   OPENAI_API_KEY=your-api-key-here
   ```

### Fallback Behavior

If GPT is not configured or fails:
- The app automatically falls back to template-based generation
- Templates use the same Trivance AI voice and structure
- Multiple template variations provide content variety
- No functionality is lost

### Content Generation Methods

**Template-Based (Default):**
- ✅ No API costs
- ✅ Consistent Trivance voice
- ✅ Fast generation
- ✅ Multiple template variations
- ⚠️ Less dynamic content

**GPT-Powered (Optional):**
- ✅ More dynamic, contextual content
- ✅ Better adaptation to article topics
- ✅ Natural language variation
- ⚠️ Requires API key and costs
- ⚠️ Potential for inconsistent voice

## Hashtag Generation

The system automatically generates relevant hashtags based on:
- Article title and summary keywords
- Trivance AI core hashtags (#AI, #TrivanceAI, #SmallBusiness)
- Industry-specific tags (#ChatGPT, #Automation, #Strategy, etc.)
- Maximum of 7 hashtags per post

## Post Generation Styles

The enhanced content generator now supports three distinct writing styles:

### Available Styles

**Consultative (Default)**
- Clear, strategic tone with frameworks
- Balanced sentence length, professional
- Uses insights and structured approaches
- Best for: Strategic insights, business analysis

**Punchy**
- Short sentences, bold claims
- Scroll-stopping, direct style
- Attention-grabbing hooks
- Best for: Viral content, strong opinions

**Casual** 
- Friendly, conversational tone
- Uses analogies and accessible language
- Informal, uses contractions
- Best for: Relatable content, explanations

### Content Accuracy Features

**Key Insights Extraction**:
- Automatically identifies statistics (85%, $1M, etc.)
- Extracts quotes from article summaries
- Finds key findings and research results
- Ensures specific details are included in posts

**Article Content Integration**:
- Posts now reference actual article data
- Include at least one specific fact or quote
- Avoid generic generalizations
- Anchor insights in real content

### Style Examples

**Consultative Example**:
> "📊 AI adoption grows 40% — here's the strategic insight:
> Consider this: 78% of successful implementations start with process mapping.
> The framework that works: ✦ Map workflows ✦ Identify bottlenecks ✦ Apply AI precisely"

**Punchy Example**:
> "🚨 AI adoption grows 40%.
> Here's what everyone's missing: Most teams buy tools first, ask questions later.
> Stop. Problems first. Tools second."

**Casual Example**:
> "💭 Interesting take: AI adoption grows 40%
> You know what I love about this? It's exactly what we see with our clients.
> Think of AI like hiring a smart intern..."
