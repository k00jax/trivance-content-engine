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

## Post Structure

All generated posts follow this structure:
1. **Hook:** Bold, engaging first sentence with article title
2. **Insight:** Strategic takeaway relevant to SMBs
3. **Framework:** Bulleted list of actionable points
4. **Brand Voice:** Trivance AI positioning statement
5. **CTA:** Soft call-to-action
6. **Attribution:** Source and link
7. **Hashtags:** 5-7 relevant tags
