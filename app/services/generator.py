def generate_commentary(article):
    return {
        "post": f"""💡 {article.title}

{article.summary}

As more teams embrace AI, smart execution matters. Not just hype — but clarity, automation, and systems thinking.

Source: {article.source}
{article.link}
"""
    }
