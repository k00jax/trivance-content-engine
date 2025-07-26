import os
from typing import Dict, Any

# Configuration for future GPT integration
USE_GPT = os.getenv("USE_OPENAI_GPT", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_hashtags(title, summary):
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
        "process": "#ProcessImprovement"
    }
    
    for keyword, hashtag in keyword_hashtag_map.items():
        if keyword in combined_text and hashtag not in content_tags:
            content_tags.append(hashtag)
    
    # Combine base tags with content tags, limit to 7 total
    all_tags = base_tags + content_tags[:4]  # Max 4 content tags + 3 base tags = 7
    
    return " ".join(all_tags)

def generate_with_openai(article) -> Dict[str, Any]:
    """
    Generate content using OpenAI GPT API.
    Requires OPENAI_API_KEY environment variable.
    """
    try:
        import openai
        
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        openai.api_key = OPENAI_API_KEY
        
        prompt = f"""
You are a content writer for Trivance AI — a consultancy that helps small and mid-sized businesses adopt AI using logic, language, and systems. 

Generate a ~175-word LinkedIn post using this article as inspiration — but do **not** repeat its summary. Instead, draw insights from it and layer in Trivance's perspective.

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

Now, write a new post in the same tone using:

- Title: {article.title}
- Summary: {article.summary}
- Source: {article.source}
- Link: {article.link}

Structure:
- Bold, engaging first sentence (insight or hook)
- A strategic insight or takeaway (1–2 sentences)
- Optional nod to SMBs or operational clarity
- Soft call-to-action or invitation
- 5–7 relevant hashtags

Tone:
- Clear, consultative, no buzzwords
- Sharp, not salesy
- Grounded in execution

Return clean, final LinkedIn-ready text (including hashtags at the bottom).
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional content writer for Trivance AI, skilled at creating engaging LinkedIn posts with a consultative, no-nonsense tone."},
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
            "prompt_used": prompt
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

def generate_template_based(article) -> Dict[str, Any]:
    """
    Generate content using template-based approach.
    Fallback method when GPT is not available or configured.
    """
    hashtags = generate_hashtags(article.title, article.summary)
    
    # Template variations for more dynamic content
    templates = [
        {
            "hook": "🎯 {title} — but here's what most teams miss:",
            "insight": "The real opportunity isn't in the latest AI breakthrough. It's in identifying where your current processes break down and applying the right AI tool to fix them.",
            "body": """Most small to mid-sized businesses don't need an AI transformation. They need:
✦ Clear frameworks for where AI actually helps
✦ Practical training that sticks with their team
✦ Systems that work without constant maintenance"""
        },
        {
            "hook": "💡 {title} — and it reveals something important:",
            "insight": "Every AI success story starts with the same foundation: understanding your current workflow before adding any automation.",
            "body": """At Trivance AI, we see this pattern repeatedly:
✦ Companies rush to implement AI without mapping their processes
✦ Teams get overwhelmed by tools that don't fit their workflow
✦ Results fall short because the foundation wasn't solid"""
        },
        {
            "hook": "⚡ {title} — here's the strategic takeaway:",
            "insight": "The best AI implementations aren't about replacing humans. They're about amplifying what your team already does well.",
            "body": """Smart businesses focus on:
✦ Identifying repetitive tasks that drain energy
✦ Training teams on practical AI applications
✦ Building systems that scale without complexity"""
        }
    ]
    
    # Simple rotation based on title length (pseudo-random)
    template_index = len(article.title) % len(templates)
    template = templates[template_index]
    
    post_content = f"""{template["hook"].format(title=article.title)}

{template["insight"]}

{template["body"]}

At Trivance AI, we focus on ⬩ logic ⬩ language ⬩ systems — helping you cut through the noise and build solutions that actually work.

Ready to move beyond the hype and into execution?

Source: {article.source}
{article.link if article.link else ''}

{hashtags}"""
    
    return {
        "post": post_content.strip(),
        "method": "template_based",
        "hashtags": hashtags,
        "template_used": template_index
    }

def generate_commentary(article):
    """
    Generate Trivance AI-aligned LinkedIn content using the article as inspiration.
    
    Uses OpenAI GPT if configured (USE_OPENAI_GPT=true and OPENAI_API_KEY set),
    otherwise falls back to template-based generation.
    """
    
    if USE_GPT and OPENAI_API_KEY:
        result = generate_with_openai(article)
        
        # If GPT generation failed, fall back to template
        if result.get("fallback") or result.get("error"):
            print(f"GPT generation failed: {result.get('error', 'Unknown error')}")
            print("Falling back to template-based generation...")
            return generate_template_based(article)
        
        return result
    
    else:
        # Use template-based generation
        return generate_template_based(article)
