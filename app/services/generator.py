import os
import re
import time
import html
import logging
import threading
from typing import Dict, Any, Optional
import openai
import textwrap



# Import content vault for storing successful generations
try:
    from .content_vault import content_vault
except ImportError:
    content_vault = None

USE_GPT = os.getenv("USE_OPENAI_GPT", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEBUG_GPT_RESPONSE = os.getenv("DEBUG_GPT_RESPONSE", "false").lower() == "true"

STYLE_EXAMPLES = {
    "trivance_default": {
        "description": "Professional, clear, consultative, and educational",
        "sentence_style": "Balanced and strategic, avoids fluff",
        "example_phrases": [
        ],
        "hooks": [
            "📊 {title} — and the implications are clear:",
            "🎯 {title} — but here's what most teams miss:",
            "💡 {title} — and it reveals something important:",
            "⚡ {title} — the timing couldn't be better:"
        ]
    },
    "punchy": {
        "description": "Direct, action-oriented, and energetic",
        "sentence_style": "Short, impactful statements with clear calls to action",
        "example_phrases": [
            "Here's the reality:",
            "Bottom line:",
            "The result?",
            "Time to act.",
            "What's your move?"
        ],
        "hooks": [
            "🚀 {title} — game changer alert!",
            "💥 {title} — this changes everything:",
            "⚡ {title} — action required:",
            "🎯 {title} — opportunity knocking:"
        ]
    },
    "casual": {
        "description": "Conversational, approachable, and relatable",
        "sentence_style": "Natural flow with personal touches and accessible language",
        "example_phrases": [
            "Think about it:",
            "Here's what's interesting:",
            "I've been thinking about this:",
            "Worth considering:",
            "What do you think?"
        ],
        "hooks": [
            "🤔 {title} — got me thinking:",
            "💭 {title} — here's my take:",
            "🗣️ {title} — let's talk about this:",
            "👀 {title} — worth your attention:"
        ]
    }
}

def extract_key_insights(text: str) -> list:
    """Extract high-quality insights from article summary for content generation."""
    if not text:
        return ["No content available for analysis"]

    keywords = [
        'ai', 'business', 'company', 'technology', 'data', 'growth', 'innovation',
        'market', 'automate', 'optimize', 'platform', 'tools', 'reduce', 'efficiency',
        'workflow', 'integration', 'model', 'system', 'assistant', 'productivity'
    ]

    # Clean and split into sentences
    sentences = [s.strip() for s in text.split('. ') if len(s.strip()) > 30]
    insights = []

    for sentence in sentences:
        lower = sentence.lower()
        if any(k in lower for k in keywords) and not sentence.endswith("..."):
            insights.append(f"Key insight: {sentence}")
        if len(insights) >= 3:
            break

    # If weak insights, return fallback
    if not insights:
        short = text[:240].strip().rstrip(".") + "..."
        return [f"Summary: {short}"]

    return insights


def generate_hashtags(text: str) -> str:
    """Generate relevant hashtags based on content."""
    hashtag_map = {
        'ai': '#AI', 'artificial intelligence': '#AI',
        'business': '#Business', 'company': '#Business',
        'technology': '#Technology', 'tech': '#Technology',
        'innovation': '#Innovation', 'growth': '#Growth',
        'leadership': '#Leadership', 'strategy': '#Strategy',
        'automation': '#Automation', 'digital': '#Digital',
        'data': '#Data', 'analytics': '#Analytics'
    }
    
    text_lower = text.lower()
    found_tags = set()
    
    for keyword, hashtag in hashtag_map.items():
        if keyword in text_lower:
            found_tags.add(hashtag)
    
    # Always include Trivance AI tags
    found_tags.update(['#TrivanceAI', '#SmallBusiness'])
    
    return ' '.join(list(found_tags)[:6])

def generate_with_openai(article, post_style="trivance_default", platform="LinkedIn") -> Dict[str, Any]:
    """Generate content using OpenAI GPT with timeout and enhanced error handling."""
    try:
        import openai
        import threading
        
        result = {"success": False, "error": None, "response": None}
        
        def api_call():
            try:
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                style = STYLE_EXAMPLES.get(post_style, STYLE_EXAMPLES["trivance_default"])
                source = article.source.strip() or "RSS Feeds"
                
                # Decode HTML entities before processing
                clean_title = html.unescape(article.title) if article.title else ""
                clean_summary = html.unescape(article.summary) if article.summary else ""
                
                insights = extract_key_insights(clean_summary)
                
                platform_note = {
                    "LinkedIn": "Include hashtags at the end.",
                    "Email": "No hashtags. Use subject line style tone.",
                    "X": "Post must be under 280 characters. Short, bold, and direct."
                }[platform if platform in ["LinkedIn", "Email", "X"] else "LinkedIn"]

                prompt = textwrap.dedent(f"""
                    You are a strategic content writer at Trivance AI — a consultancy that helps small and mid-sized companies apply AI in practical, high-leverage ways.

                    Create an engaging {platform} post about this article using a {post_style} tone.

                    **You MUST avoid** generic phrases like:
                    - “Consider this:”
                    - “Smart businesses recognize”
                    - “Here's what's interesting:”
                    These sound templated and generic. Do not use them.

                    Instead:
                    - Reference specific features, technologies, or business problems from the article
                    - Explain where this tool could fit into a small/mid-sized org (e.g., HR, logistics, IT ops)
                    - Write like you’re speaking to a COO or Director of Ops — smart and time-conscious
                    - Keep the Trivance tone: clear, consultative, and outcome-driven

                    Structure:
                    1. Hook (clear, relevant to the headline)
                    2. Specific insight (e.g. what this enables)
                    3. Strategic framing (why it matters, where it fits)
                    4. Soft CTA or reflection

                    Article Details:
                    Title: {clean_title}
                    Source: {source}
                    Link: {article.link}
                    Summary: {clean_summary}

                    Key insights to optionally reference: {insights}

                    Final Reminder: Write like a strategist, not a marketer.
                """)
                
                logging.info(f"OpenAI API request sent for article: {clean_title[:50]}...")
                import json

                prompt_length = len(prompt)
                logging.info(f"⏱ Prompt length: {prompt_length} characters")
                logging.info(f"⏱ Prompt sample (first 500 chars):\n{prompt[:500]}")

                # Also validate the message object
                message_payload = [
                    {"role": "system", "content": "You are a strategic..."},
                    {"role": "user", "content": prompt}
                ]
                logging.info("Message payload JSON size:", len(json.dumps(message_payload)))

                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a strategic, human-sounding content writer for Trivance AI. You write posts that are specific, business-relevant, and NEVER use clichés like 'consider this' or 'smart businesses recognize.'"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=0.7
                )

                logging.info("OpenAI API response received successfully")
                
                result["success"] = True
                result["response"] = completion
                result["prompt"] = prompt
                result["insights"] = insights
                logging.info(f"OpenAI generation successful - tokens used: {completion.usage.total_tokens}")
                
            except Exception as e:
                error_msg = f"OpenAI API error: {str(e)}"
                logging.error(error_msg)
                result["error"] = error_msg
        
        # Start API call in thread with timeout
        start_time = time.time()
        thread = threading.Thread(target=api_call)
        thread.daemon = True
        thread.start()
        thread.join(timeout=15)  # 15 second timeout
        
        duration = time.time() - start_time
        
        if thread.is_alive():
            logging.error("⏰ OpenAI API call timed out after 15 seconds")
            return {
                "error": "API call timeout (15s)",
                "fallback": True
            }
        
        if not result["success"]:
            error_msg = result.get("error", "Unknown API error")
            logging.error(f"🚨 OpenAI API error: {error_msg}")
            return {
                "error": f"API error: {error_msg}",
                "fallback": True
            }
        
        # Process successful response
        completion = result["response"]
        if not completion or not completion.choices:
            logging.error("❌ OpenAI returned empty response or no choices")
            return {
                "error": "Empty response from OpenAI",
                "fallback": True
            }
        
        text = completion.choices[0].message.content
        if not text or not text.strip():
            logging.error("❌ OpenAI returned empty content")
            return {
                "error": "Empty content in OpenAI response", 
                "fallback": True
            }
        
        text = text.strip()
        
        # Debug mode: Log GPT response
        if DEBUG_GPT_RESPONSE:
            logging.info(f"[DEBUG] GPT Raw Output ({len(text)} chars):\n{text[:200]}{'...' if len(text) > 200 else ''}")
        
        # Check minimum length threshold
        if len(text) < 50:
            logging.error(f"❌ OpenAI response too short: {len(text)} characters")
            return {
                "error": f"Response too short ({len(text)} characters)",
                "fallback": True
            }
        
        logging.info(f"✅ OpenAI generation successful! ({len(text)} characters, {duration:.2f}s)")
        
        # Verify this looks like AI-generated content (not template-like)
        template_indicators = [
            "Consider this:",
            "Smart businesses recognize",
            "The framework that works:",
            "Here's a specific takeaway:",  # Added the problematic phrase
            "Here's what's interesting:",
            "Think about it:",
            "✦ Identify",
            "✦ Map", 
            "✦ Choose"
        ]
        
        if any(indicator in text for indicator in template_indicators):
            logging.warning("⚠️ OpenAI response contains template-like patterns - possible content issue")
            if DEBUG_GPT_RESPONSE:
                logging.info(f"[DEBUG] Suspicious content detected:\n{text}")
        
        # Store generation metadata for debugging
        generation_metadata = {
            "prompt_length": len(result.get("prompt", "")),
            "response_length": len(text),
            "generation_time": duration,
            "has_template_patterns": any(indicator in text for indicator in template_indicators)
        }
        
        if DEBUG_GPT_RESPONSE:
            logging.info(f"[DEBUG] Generation metadata: {generation_metadata}")
        
        # Add hashtags for LinkedIn
        if platform == "LinkedIn":
            text += f"\n\n{generate_hashtags(article.title + ' ' + article.summary)}"

        # Store in content vault
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
            "prompt_used": result["prompt"],
            "style_used": post_style,
            "platform": platform,
            "key_insights": result["insights"]
        }
        
    except ImportError as e:
        logging.error(f"📦 OpenAI library not available: {e}")
        return {
            "error": f"OpenAI library not available: {e}",
            "fallback": True
        }
    except Exception as e:
        logging.error(f"🚨 OpenAI generation failed: {str(e)}")
        return {
            "error": f"OpenAI generation failed: {str(e)}",
            "fallback": True
        }

def generate_template_based(article, post_style="trivance_default", platform="LinkedIn") -> Dict[str, Any]:
    import random

    # Decode HTML entities
    clean_title = html.unescape(article.title or "")
    clean_summary = html.unescape(article.summary or "")
    source = article.source.strip() or "RSS Feeds"
    insights = extract_key_insights(clean_summary)

    # Synthesize 2–3 insights
    selected_insights = insights[:3]
    insight_text = " ".join(i.replace("Key insight:", "").strip() for i in selected_insights)

    # Style selection
    style = STYLE_EXAMPLES.get(post_style, STYLE_EXAMPLES["trivance_default"])
    hook_template = random.choice(style["hooks"])
    hook = hook_template.format(title=clean_title)
    phrase = random.choice(style["example_phrases"])

    # Strategic framing
    framing_options = [
        "The takeaway for small teams? Prioritize high-leverage tools with low friction.",
        "For leaders navigating AI, it's about choosing tools that reduce complexity — not add to it.",
        "Execution matters more than exploration. Especially in environments where time is tight.",
        "This underscores why clarity beats hype — and where practical automation creates momentum.",
        "In the AI race, it’s not who’s first — it’s who’s actually effective."
    ]
    framing = random.choice(framing_options)

    # Construct post
    post = f"""{hook}

{phrase} {insight_text}

{framing}

Source: {source}
{article.link}"""

    # Add hashtags for social platforms only
    if platform in ["LinkedIn", "X"]:
        post += f"\n\n{generate_hashtags(clean_title + ' ' + clean_summary)}"

    return {
        "post": post.strip(),
        "method": "template_improved",
        "style_used": post_style,
        "platform": platform,
        "key_insights": selected_insights
    }


def generate_commentary(article, post_style="trivance_default", platform="LinkedIn"):
    logging.info(f"🔄 Starting content generation for: {article.title[:50]}...")
    logging.info(f"   Style: {post_style}, Platform: {platform}, USE_GPT: {USE_GPT}")
    
    if USE_GPT and OPENAI_API_KEY:
        logging.info("🤖 Attempting OpenAI generation...")
        result = generate_with_openai(article, post_style, platform)
        
        # Check if we actually got an OpenAI response
        if result.get("method") == "openai_gpt" and not result.get("error"):
            logging.info("✅ OpenAI generation completed successfully!")
            if DEBUG_GPT_RESPONSE:
                content_preview = result.get("post", "")[:100] + "..." if len(result.get("post", "")) > 100 else result.get("post", "")
                logging.info(f"[DEBUG] Final content preview: {content_preview}")
            return result
        else:
            error_msg = result.get('error', 'Unknown OpenAI failure')
            logging.error(f"❌ OpenAI failed: {error_msg}")
            logging.warning("🔄 Falling back to template generation...")
            
            # Add fallback metadata for tracking
            fallback_result = generate_template_based(article, post_style, platform)
            fallback_result["fallback_reason"] = error_msg
            fallback_result["attempted_method"] = "openai_gpt"
            return fallback_result
    else:
        if not USE_GPT:
            logging.info("📋 OpenAI disabled - using template generation")
        elif not OPENAI_API_KEY:
            logging.warning("🔑 No OpenAI API key - using template generation")
        else:
            logging.info("📋 Using template generation")
        return generate_template_based(article, post_style, platform)

def get_available_styles() -> Dict[str, str]:
    return {k: v["description"] for k, v in STYLE_EXAMPLES.items()}
