import os
import re
from typing import Dict, Any, Optional

# Configuration for future GPT integration
USE_GPT = os.getenv("USE_OPENAI_GPT", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Style definitions for different post tones
STYLE_EXAMPLES = {
    "consultative": {
        "description": "Clear, strategic, uses insight and frameworks",
        "sentence_style": "Balanced length, professional",
        "example_phrases": ["strategic insight", "framework for", "execution matters", "smart businesses focus"]
    },
    "punchy": {
        "description": "Short sentences, bold claims, scroll-stopping style",
        "sentence_style": "Short, punchy, direct",
        "example_phrases": ["Here's the truth:", "Stop doing this:", "The real secret:", "Most teams miss this:"]
    },
    "casual": {
        "description": "Friendly, informal, uses analogies and accessible language",
        "sentence_style": "Conversational, uses contractions",
        "example_phrases": ["Think of it this way:", "Here's what's wild:", "You know what I've noticed?", "It's like this:"]
    }
}

def extract_key_insights(summary: str, max_insights: int = 3) -> list:
    """
    Extract key insights, stats, or quotes from the article summary.
    Returns a list of the most important pieces of information.
    """
    if not summary:
        return []
    
    insights = []
    
    # Look for numbers/statistics
    stat_pattern = r'\b\d+(?:\.\d+)?%|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|percent|%)\b'
    stats = re.findall(stat_pattern, summary.lower())
    insights.extend([f"Key stat: {stat}" for stat in stats[:2]])
    
    # Look for quotes (text in quotes)
    quote_pattern = r'"([^"]+)"'
    quotes = re.findall(quote_pattern, summary)
    insights.extend([f"Quote: \"{quote}\"" for quote in quotes[:1]])
    
    # Extract key phrases (sentences with important keywords)
    important_keywords = [
        'shows', 'reveals', 'found', 'discovered', 'study', 'research', 'report',
        'increased', 'decreased', 'improved', 'reduced', 'growth', 'decline',
        'announced', 'launched', 'released', 'introduced'
    ]
    
    sentences = summary.split('.')
    for sentence in sentences[:5]:  # Check first 5 sentences
        sentence = sentence.strip()
        if any(keyword in sentence.lower() for keyword in important_keywords) and len(sentence) > 20:
            insights.append(f"Key finding: {sentence}")
            if len(insights) >= max_insights:
                break
    
    return insights[:max_insights]

def generate_hashtags(title: str, summary: str) -> str:
    """
    Generate 5-7 relevant hashtags based on article title and summary.
    Returns a string of hashtags for LinkedIn posts.
    """
    # Common Trivance AI hashtags
    base_tags = ["#AI", "#TrivanceAI", "#SmallBusiness"]
    
    # Content-based hashtags (simple keyword matching for now)
    content_tags = []
    
    combined_text = f"{title} {summary}".lower()
    
    # Map keywords to hashtags
    keyword_hashtag_map = {
        "chatgpt": "#ChatGPT",
        "gpt": "#GPT",
        "openai": "#OpenAI",
        "automation": "#Automation",
        "efficiency": "#Efficiency",
        "productivity": "#Productivity",
        "machine learning": "#MachineLearning",
        "ml": "#MachineLearning",
        "data": "#DataScience",
        "analytics": "#Analytics",
        "startup": "#Startup",
        "entrepreneur": "#Entrepreneur",
        "business": "#Business",
        "strategy": "#Strategy",
        "innovation": "#Innovation",
        "technology": "#Tech",
        "operations": "#Operations",
        "workflow": "#Workflow",
        "process": "#ProcessImprovement",
        "executive": "#Leadership",
        "ceo": "#Leadership",
        "growth": "#Growth",
        "scale": "#Scaling"
    }
    
    for keyword, hashtag in keyword_hashtag_map.items():
        if keyword in combined_text and hashtag not in content_tags:
            content_tags.append(hashtag)
    
    # Combine base tags with content tags, limit to 7 total
    all_tags = base_tags + content_tags[:4]  # Max 4 content tags + 3 base tags = 7
    
    return " ".join(all_tags)

def generate_with_openai(article, post_style: str = "consultative") -> Dict[str, Any]:
    """
    Generate content using OpenAI GPT API with proper style control.
    """
    try:
        import openai
        
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        openai.api_key = OPENAI_API_KEY
        
        # Get style information
        style_info = STYLE_EXAMPLES.get(post_style, STYLE_EXAMPLES["consultative"])
        key_insights = extract_key_insights(article.summary)
        
        prompt = f"""
You are a strategic content writer at Trivance AI — a consultancy that helps small and mid-sized businesses adopt AI through logic, language, and systems.

Write a ~175-word LinkedIn post based on the article below.

Your post must:
- Hook readers with a sharp, strategic statement
- Include at least **one clear idea, fact, or detail** from the article summary
- Reflect the Trivance perspective: execution > hype
- End with a soft CTA + 5-7 relevant hashtags

Example Trivance Post:
Welcome to Trivance AI — your strategic partner for AI clarity and execution.

We started Trivance with a simple insight:
✦ Most small to mid-sized businesses don't need an AI overhaul.
✦ They need a human guide to cut through the noise, spot real opportunities, and build smart, working solutions.

Whether you're:
● Looking to upskill your team with practical ChatGPT techniques
● Or unsure where to even begin with low-lift AI in your business — we've got you.

Our approach is grounded in ⬩ logic ⬩ language ⬩ systems — not buzzwords or overpromised solutions.
We bring structure and strategy to the table, so you can move fast and confidently.

Tone Style: {post_style}
Style Guidelines: {style_info["description"]}
Sentence Style: {style_info["sentence_style"]}

CRITICAL: Include at least one specific detail from the summary below. Do not generalize — anchor your insight in the actual content.

Article Input:
- Title: {article.title}
- Summary: {article.summary}
- Source: {article.source}
- Link: {article.link}

Key insights to potentially reference: {key_insights}

Return clean, final LinkedIn-ready text (including hashtags at the bottom).
"""
        
        # Use newer OpenAI API format
        try:
            # Try new API first
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a professional content writer for Trivance AI, skilled at creating engaging LinkedIn posts with a {post_style} tone that incorporates specific details from article content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            generated_content = response.choices[0].message.content.strip()
            
        except (ImportError, AttributeError):
            # Fallback to old API format
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a professional content writer for Trivance AI, skilled at creating engaging LinkedIn posts with a {post_style} tone."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            generated_content = response.choices[0].message.content.strip()
        
        hashtags = generate_hashtags(article.title, article.summary)
        
        return {
            "post": generated_content,
            "method": "openai_gpt",
            "hashtags": hashtags,
            "prompt_used": prompt,
            "style_used": post_style,
            "key_insights": key_insights
        }
        
    except ImportError:
        return {
            "error": "OpenAI library not installed. Run: pip install openai",
            "fallback": True
        }
    except Exception as e:
        return {
            "error": f"OpenAI generation failed: {str(e)}",
            "fallback": True
        }

def generate_template_based(article, post_style: str = "consultative") -> Dict[str, Any]:
    """
    Generate content using template-based approach with style control.
    Uses actual article content and applies proper style formatting.
    """
    hashtags = generate_hashtags(article.title, article.summary)
    key_insights = extract_key_insights(article.summary)
    style_info = STYLE_EXAMPLES.get(post_style, STYLE_EXAMPLES["consultative"])
    
    # Extract a specific detail from the summary to include
    specific_detail = ""
    if key_insights:
        specific_detail = key_insights[0].replace("Key stat: ", "").replace("Key finding: ", "").replace("Quote: ", "")
    elif article.summary:
        # Fallback: use first meaningful sentence from summary
        sentences = [s.strip() for s in article.summary.split('.') if len(s.strip()) > 20]
        if sentences:
            specific_detail = sentences[0]
    
    # Style-specific templates
    if post_style == "punchy":
        templates = [
            {
                "hook": "🚨 {title}.",
                "insight": "Here's what everyone's missing: {detail}",
                "body": """The playbook is simple:
• Map your current workflow
• Find the bottlenecks  
• Apply AI precisely where it matters

Stop chasing shiny tools. Start fixing real problems.""",
                "cta": "Ready to cut through the noise?"
            },
            {
                "hook": "💥 {title}.",
                "insight": "The truth? {detail}",
                "body": """Most teams get this backwards:
• They buy AI tools first
• Then figure out what to do with them
• Wonder why results disappoint

Smart approach: Problems first. Tools second.""",
                "cta": "Time to flip the script?"
            }
        ]
    
    elif post_style == "casual":
        templates = [
            {
                "hook": "📰 Just read this: {title}",
                "insight": "Here's what caught my attention: {detail}",
                "body": """You know what I love about this? It's exactly what we see with our clients.

The companies that succeed with AI aren't the ones with the biggest budgets. They're the ones who:
• Start with clear problems
• Test small and learn fast  
• Focus on their team's actual workflows

It's not rocket science, but it works.""",
                "cta": "What's your take on this?"
            },
            {
                "hook": "� Interesting perspective: {title}",
                "insight": "This resonates: {detail}",
                "body": """Think of it this way — AI is like hiring a really smart intern.

You wouldn't just give them access to everything and say "figure it out." You'd:
• Show them your current process
• Give them specific tasks to improve
• Check their work and iterate

Same principle applies to AI tools.""",
                "cta": "Makes sense, right?"
            }
        ]
    
    else:  # consultative (default)
        templates = [
            {
                "hook": "🎯 {title} — here's the strategic insight:",
                "insight": "The key finding: {detail}",
                "body": """This aligns with what we see across SMBs implementing AI successfully.

The pattern is consistent:
✦ They start with process mapping, not tool shopping
✦ They focus on high-impact, low-complexity wins first
✦ They invest in team training alongside technology

At Trivance AI, we call this ⬩ logic ⬩ language ⬩ systems — because sustainable AI adoption requires all three.""",
                "cta": "Ready to build your AI strategy on solid foundations?"
            },
            {
                "hook": "📊 {title} — and the implications are clear:",
                "insight": "Consider this: {detail}",
                "body": """Smart businesses recognize that AI implementation isn't about replacing humans — it's about amplifying human capabilities.

The framework that works:
✦ Identify repetitive tasks that drain team energy
✦ Map existing workflows before adding automation
✦ Choose tools that integrate with current systems

This isn't about transformation. It's about intelligent optimization.""",
                "cta": "What's your next optimization opportunity?"
            }
        ]
    
    # Select template based on title length for variation
    template_index = len(article.title) % len(templates)
    template = templates[template_index]
    
    # Build the post content
    hook = template["hook"].format(title=article.title)
    insight = template["insight"].format(detail=specific_detail[:100] + "..." if len(specific_detail) > 100 else specific_detail)
    
    post_content = f"""{hook}

{insight}

{template["body"]}

{template["cta"]}

Source: {article.source}
{article.link if article.link else ''}

{hashtags}"""
    
    return {
        "post": post_content.strip(),
        "method": "template_based",
        "hashtags": hashtags,
        "template_used": template_index,
        "style_used": post_style,
        "key_insights": key_insights,
        "specific_detail": specific_detail
    }

def generate_commentary(article, post_style: str = "consultative"):
    """
    Generate Trivance AI-aligned LinkedIn content using the article as inspiration.
    
    Args:
        article: Article object with title, summary, source, link
        post_style: Style of the post ("consultative", "punchy", "casual")
    
    Uses OpenAI GPT if configured (USE_OPENAI_GPT=true and OPENAI_API_KEY set),
    otherwise falls back to template-based generation.
    """
    
    # Validate post_style
    if post_style not in STYLE_EXAMPLES:
        post_style = "consultative"
    
    if USE_GPT and OPENAI_API_KEY:
        result = generate_with_openai(article, post_style)
        
        # If GPT generation failed, fall back to template
        if result.get("fallback") or result.get("error"):
            print(f"GPT generation failed: {result.get('error', 'Unknown error')}")
            print("Falling back to template-based generation...")
            return generate_template_based(article, post_style)
        
        return result
    
    else:
        # Use template-based generation
        return generate_template_based(article, post_style)

# Utility function to get available styles
def get_available_styles() -> Dict[str, str]:
    """Return available post styles with descriptions."""
    return {style: info["description"] for style, info in STYLE_EXAMPLES.items()}
