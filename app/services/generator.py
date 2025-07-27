import os
import re
import time
from typing import Dict, Any, Optional

# Import content vault for storing successful generations
try:
    from .content_vault import content_vault
except ImportError:
    content_vault = None

USE_GPT = os.getenv("USE_OPENAI_GPT", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

STYLE_EXAMPLES = {
    "trivance_default": {
        "description": "Professional, clear, consultative, and educational",
        "sentence_style": "Balanced and strategic, avoids fluff",
        "example_phrases": [
            "Strategic insight",
            "Execution > hype",
            "Mapped workflows",
            "Smart systems",
            "Clear frameworks"
        ]
    },
    "punchy": {
        "description": "Short, bold, scroll-stopping",
        "sentence_style": "One-liners, hooks, shock and clarity",
        "example_phrases": ["Here's the truth:", "Stop doing this:", "What most miss:"]
    },
    "casual": {
        "description": "Friendly, analogy-driven, accessible",
        "sentence_style": "Conversational, uses metaphors",
        "example_phrases": ["Think of it this way:", "It's like this:", "You know what I've noticed?"]
    }
}

def extract_key_insights(summary: str, max_insights: int = 3) -> list:
    if not summary:
        return []
    
    insights = []
    stat_pattern = r'\b\d+(?:\.\d+)?%|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|percent|%)\b'
    quotes = re.findall(r'"([^"]+)"', summary)
    stats = re.findall(stat_pattern, summary.lower())
    insights += [f"Stat: {stat}" for stat in stats[:2]]
    insights += [f"Quote: {quote}" for quote in quotes[:1]]

    important_keywords = [
        'reveals', 'found', 'discovered', 'study', 'research', 'announced',
        'launched', 'released', 'introduced', 'accelerated', 'resistance', 'compliance'
    ]
    for sentence in summary.split('.')[:6]:
        if any(k in sentence.lower() for k in important_keywords):
            insights.append(f"Finding: {sentence.strip()}")
        if len(insights) >= max_insights:
            break

    return insights[:max_insights]

def generate_hashtags(text: str) -> str:
    base_tags = ["#AI", "#TrivanceAI", "#SmallBusiness"]
    topics = {
        "chatgpt": "#ChatGPT", "gpt": "#GPT", "automation": "#Automation",
        "startup": "#Startup", "efficiency": "#Efficiency", "scale": "#Scaling",
        "leadership": "#Leadership", "compliance": "#AIGovernance"
    }
    text = text.lower()
    dynamic = [h for k, h in topics.items() if k in text]
    return " ".join(list(dict.fromkeys(base_tags + dynamic))[:7])

def generate_with_openai(article, post_style="trivance_default", platform="LinkedIn") -> Dict[str, Any]:
    try:
        import openai

        if not OPENAI_API_KEY:
            return {
                "error": "Missing OPENAI_API_KEY",
                "fallback": True
            }

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        style = STYLE_EXAMPLES.get(post_style, STYLE_EXAMPLES["trivance_default"])
        source = article.source.strip() or "RSS Feeds"
        insights = extract_key_insights(article.summary)
        
        platform_note = {
            "LinkedIn": "Include hashtags at the end.",
            "Email": "No hashtags. Use subject line style tone.",
            "X": "Post must be under 280 characters. Short, bold, and direct."
        }[platform if platform in ["LinkedIn", "Email", "X"] else "LinkedIn"]

        prompt = f"""
You are a strategic content writer at Trivance AI. Create a post for {platform} using a {post_style} tone.

Your goal:
- Reference at least one specific detail from the summary
- Reflect Trivance AI's logic-language-systems mindset
- Follow this structure: Hook, Insight, Framing, Soft CTA
- {platform_note}

Article:
Title: {article.title}
Source: {source}
Link: {article.link}
Summary: {article.summary}

Insights you may use: {insights}
"""
        # Log request start time
        start_time = time.time()
        print(f"🚀 Starting OpenAI API call at {time.strftime('%H:%M:%S')}")
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use faster, cheaper model
            messages=[
                {"role": "system", "content": "You're a strategic copywriter for Trivance AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,  # Reduced tokens
            temperature=0.7,
            timeout=60  # 60 second timeout
        )
        
        # Log completion time and duration
        end_time = time.time()
        duration = end_time - start_time
        print(f"🏁 OpenAI API call completed in {duration:.2f}s")
        
        # Flag as potential hang if >30s
        if duration > 30:
            print(f"⚠️ API call took longer than expected ({duration:.2f}s > 30s)")
        
        # Validate response
        if not completion or not completion.choices:
            print("⚠️  Empty response from OpenAI")
            return {
                "error": "Empty response from OpenAI",
                "fallback": True
            }
        
        text = completion.choices[0].message.content
        if not text or not text.strip():
            print("⚠️  Empty content in OpenAI response")
            return {
                "error": "Empty content in OpenAI response", 
                "fallback": True
            }
        
        text = text.strip()
        
        # Enhanced success criteria check
        if len(text) > 50:  # Minimum viable post length
            print(f"✅ OpenAI generation successful! ({len(text)} characters)")
        else:
            print(f"⚠️ OpenAI response may be incomplete ({len(text)} characters)")
            return {
                "error": f"Response too short ({len(text)} characters)",
                "fallback": True
            }
        
        # Log token usage if available
        if hasattr(completion, 'usage') and completion.usage:
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens
            print(f"📊 Token usage: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total")
        else:
            print("📊 Token usage information not available")
        if platform == "LinkedIn":
            text += f"\n\n{generate_hashtags(article.title + ' ' + article.summary)}"

        # Store successful generation in content vault
        if content_vault:
            vault_metadata = {
                "method": "openai_gpt",
                "style_used": post_style,
                "platform": platform,
                "generation_time": duration,
                "token_usage": {
                    "prompt_tokens": getattr(completion.usage, 'prompt_tokens', 0) if hasattr(completion, 'usage') else 0,
                    "completion_tokens": getattr(completion.usage, 'completion_tokens', 0) if hasattr(completion, 'usage') else 0,
                    "total_tokens": getattr(completion.usage, 'total_tokens', 0) if hasattr(completion, 'usage') else 0
                }
            }
            content_vault.store_successful_post(article.title, text, vault_metadata)

        return {
            "post": text,
            "method": "openai_gpt",
            "prompt_used": prompt,
            "style_used": post_style,
            "platform": platform,
            "key_insights": insights
        }
        
    except ImportError as e:
        print(f"📦 OpenAI library not available: {e}")
        return {
            "error": f"OpenAI library not available: {e}",
            "fallback": True
        }
    except Exception as e:
        print(f"🚨 OpenAI generation failed: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        return {
            "error": f"OpenAI generation failed: {str(e)}",
            "fallback": True
        }

def generate_template_based(article, post_style="trivance_default", platform="LinkedIn") -> Dict[str, Any]:
    insights = extract_key_insights(article.summary)
    detail = insights[0].split(":", 1)[-1].strip() if insights else article.summary[:160]
    hashtags = generate_hashtags(article.title + " " + article.summary) if platform == "LinkedIn" else ""
    source = article.source.strip() or "RSS Feeds"

    hook = f"🔍 {article.title}"
    body = f"""Here's a specific takeaway: {detail}

At Trivance AI, we believe in ⬩ logic ⬩ language ⬩ systems — because smart AI adoption is structured, not scattered.

Want a strategy that sticks?

Source: {source}
{article.link}

{hashtags}"""

    return {
        "post": f"{hook}\n\n{body.strip()}",
        "method": "template",
        "platform": platform,
        "hashtags_included": bool(hashtags),
        "style_used": post_style,
        "key_insights": insights
    }

def generate_commentary(article, post_style="trivance_default", platform="LinkedIn"):
    print(f"🔧 generate_commentary called with USE_GPT={USE_GPT}, API_KEY={'set' if OPENAI_API_KEY else 'missing'}")
    
    if USE_GPT and OPENAI_API_KEY:
        print("🤖 Attempting OpenAI generation...")
        result = generate_with_openai(article, post_style, platform)
        
        # Enhanced fallback logic - only fallback on actual failures
        if result.get("error") or result.get("fallback"):
            error_msg = result.get('error', 'Unknown error')
            print(f"🔄 OpenAI failed, using template fallback: {error_msg}")
            
            # Log the specific failure reason for monitoring
            failure_type = "timeout" if "timeout" in error_msg.lower() else "api_error"
            print(f"📊 Failure type: {failure_type}")
            
            return generate_template_based(article, post_style, platform)
        
        # Success case - log and return
        print("✅ OpenAI generation completed successfully!")
        return result
    else:
        print("📋 Using template generation (OpenAI disabled)")
        return generate_template_based(article, post_style, platform)

def get_available_styles() -> Dict[str, str]:
    return {k: v["description"] for k, v in STYLE_EXAMPLES.items()}
