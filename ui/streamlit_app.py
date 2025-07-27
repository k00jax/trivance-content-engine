import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Adjust if hosted remotely

st.set_page_config(page_title="Trivance AI Content Engine", layout="wide")
st.title("🧠 Trivance AI – Content Engine Dashboard")

tabs = st.tabs(["📡 Feeds", "✍️ Generate Post", "� Recent Posts", "�📬 Subscribers"])

# --- FEEDS TAB ---
with tabs[0]:
    st.header("📡 Manage RSS Feeds")
    
    # Initialize success flag outside form
    if "feed_added" not in st.session_state:
        st.session_state.feed_added = False
    
    with st.form("add_feed"):
        name = st.text_input("Feed Name")
        url = st.text_input("Feed URL")
        submitted = st.form_submit_button("Add Feed")

        if submitted and name and url:
            res = requests.post(f"{API_URL}/feeds/", json={"name": name, "url": url})
            st.success(res.json()["message"])
            st.session_state.feed_added = True
    
    # Handle form reset after successful submission
    if st.session_state.feed_added:
        st.session_state.feed_added = False
        st.rerun()


    st.subheader("Current Feeds")
    try:
        res = requests.get(f"{API_URL}/feeds/")
        res.raise_for_status()
        feeds = res.json()
    except requests.RequestException as e:
        st.error(f"Error fetching feeds: {e}")
        feeds = []

    if feeds:
        for i, f in enumerate(feeds):
            cols = st.columns([5, 1])
            with cols[0]:
                st.markdown(f"**{f['name']}** → {f['url']}")
            with cols[1]:
                if st.button("🗑 Remove", key=f"remove_{i}"):
                    try:
                        requests.delete(f"{API_URL}/feeds/", params={"name": f["name"]})
                        st.rerun()
                    except requests.RequestException as e:
                        st.error(f"Error removing feed: {e}")
    else:
        st.info("No feeds added yet. Add your first RSS feed above!")


# --- POST GENERATOR TAB ---
with tabs[1]:
    st.header("✍️ Generate AI-Driven Post")
    
    # Auto-select mode toggle
    auto_mode = st.checkbox("🤖 Auto-generate from top article (recommended)", value=True)
    
    # Initialize session state for form data
    if "selected_article" not in st.session_state:
        st.session_state.selected_article = None
    
    if auto_mode:
        st.info("💡 Auto mode will select the highest-scoring article from all your RSS feeds")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 Fetch Top Article", type="primary"):
                try:
                    with st.spinner("Analyzing articles from all feeds..."):
                        res = requests.get(f"{API_URL}/feeds/top-article")
                        res.raise_for_status()
                        st.session_state.selected_article = res.json()
                        st.success("✅ Top article selected!")
                except requests.RequestException as e:
                    st.error(f"Error fetching top article: {e}")
                    st.session_state.selected_article = None
        
        with col2:
            max_age = st.selectbox("Max article age", [1, 3, 7, 14, 30], index=2, format_func=lambda x: f"{x} days")
    
    else:
        st.info("📋 Manual mode: select a feed and article manually")
        
        # Get available feeds
        try:
            feeds_res = requests.get(f"{API_URL}/feeds/")
            feeds_res.raise_for_status()
            feeds = feeds_res.json()
        except requests.RequestException as e:
            st.error(f"Error fetching feeds: {e}")
            feeds = []
        
        if not feeds:
            st.warning("⚠️ No RSS feeds available. Add feeds in the 'Feeds' tab first.")
        else:
            # Feed selection
            feed_names = [f["name"] for f in feeds]
            selected_feed = st.selectbox("📡 Select RSS Feed", feed_names)
            
            if selected_feed:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("📰 Fetch Articles", type="secondary"):
                        try:
                            with st.spinner(f"Fetching articles from {selected_feed}..."):
                                articles_res = requests.get(f"{API_URL}/feeds/articles", params={"feed_name": selected_feed})
                                articles_res.raise_for_status()
                                articles = articles_res.json()
                                st.session_state.available_articles = articles
                                st.success(f"✅ Found {len(articles)} articles")
                        except requests.RequestException as e:
                            st.error(f"Error fetching articles: {e}")
                            st.session_state.available_articles = []
                
                # Article selection
                if "available_articles" in st.session_state and st.session_state.available_articles:
                    articles = st.session_state.available_articles
                    
                    # Format article options with scores
                    article_options = []
                    for i, article in enumerate(articles):
                        score = article.get("score", 0)
                        title = article.get("title", "No title")[:60]
                        article_options.append(f"[Score: {score}] {title}...")
                    
                    selected_article_idx = st.selectbox(
                        "📄 Select Article", 
                        range(len(article_options)),
                        format_func=lambda i: article_options[i]
                    )
                    
                    if selected_article_idx is not None:
                        selected_article = articles[selected_article_idx]
                        st.session_state.selected_article = selected_article
                        
                        # Show article preview
                        with st.expander("👀 Article Preview", expanded=True):
                            st.markdown(f"**Title:** {selected_article.get('title', 'N/A')}")
                            st.markdown(f"**Score:** {selected_article.get('score', 0)} (relevance to SMB AI strategy)")
                            st.markdown(f"**Published:** {selected_article.get('published', 'Unknown')}")
                            st.markdown(f"**Summary:** {selected_article.get('summary', 'No summary')[:300]}...")
                            if selected_article.get('link'):
                                st.markdown(f"**[Read Full Article]({selected_article['link']})**")
    
    # Show selected article and generation form
    if st.session_state.selected_article:
        article = st.session_state.selected_article
        
        st.subheader("📝 Selected Article")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📰 {article.get('title', 'No title')}**")
            st.markdown(f"**🎯 Relevance Score:** {article.get('score', 0)}/10")
            st.markdown(f"**📅 Published:** {article.get('published', 'Unknown')}")
        
        with col2:
            if article.get('link'):
                st.markdown(f"**[🔗 Read Original]({article['link']})**")
            st.markdown(f"**📡 Source:** {article.get('source_feed', 'Unknown')}")
        
        st.markdown("**📄 Summary:**")
        st.text_area("", value=article.get('summary', 'No summary'), height=100, disabled=True)
        
        # Generation options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            include_hashtags = st.checkbox("🏷️ Include hashtags", value=True)
            
            # Map display names to actual style keys
            style_options = {
                "Consultative (strategic, frameworks)": "consultative",
                "Punchy (short, bold claims)": "punchy", 
                "Casual (friendly, conversational)": "casual"
            }
            
            selected_style_display = st.selectbox("✍️ Post Style", 
                list(style_options.keys()),
                help="Different writing styles for various content approaches"
            )
            
            post_style = style_options[selected_style_display]
        
        with col2:
            if st.button("🚀 Generate Post", type="primary", use_container_width=True):
                try:
                    with st.spinner("🧠 Generating Trivance-aligned content..."):
                        # Include post_style in the API request
                        res = requests.post(f"{API_URL}/posts/generate", json={
                            "title": article.get("title", ""),
                            "summary": article.get("summary", ""),
                            "source": article.get("source_feed", "RSS Feed"),
                            "link": article.get("link", ""),
                            "post_style": post_style
                        })
                        res.raise_for_status()
                        result = res.json()
                        
                        st.subheader("💬 Generated LinkedIn Post")
                        
                        generated_post = result["post"]
                        if not include_hashtags and "hashtags" in result:
                            # Remove hashtags if user doesn't want them
                            hashtags = result["hashtags"]
                            generated_post = generated_post.replace(hashtags, "").strip()
                        
                        st.code(generated_post, language="markdown")
                        st.success("✅ Post generated and saved successfully!")
                        
                        # Additional info
                        with st.expander("ℹ️ Generation Details"):
                            generation_details = {
                                "method": result.get("method", "unknown"),
                                "style_used": result.get("style_used", "unknown"),
                                "hashtags": result.get("hashtags", "none"),
                                "article_score": article.get("score", 0)
                            }
                            
                            # Show key insights if available
                            if result.get("key_insights"):
                                generation_details["key_insights"] = result["key_insights"]
                            
                            if result.get("specific_detail"):
                                generation_details["specific_detail_used"] = result["specific_detail"][:100] + "..."
                            
                            st.json(generation_details)
                        
                        # Clear selection for next generation
                        if st.button("🔄 Generate Another Post"):
                            st.session_state.selected_article = None
                            st.rerun()
                            
                except requests.RequestException as e:
                    st.error(f"Error generating post: {e}")
    else:
        if auto_mode:
            st.info("👆 Click 'Fetch Top Article' to automatically select the best article from your feeds")
        else:
            st.info("👆 Select a feed and article above to generate content")
    
    # Manual entry fallback
    with st.expander("📝 Manual Entry (Alternative)", expanded=False):
        st.markdown("**Use this if RSS feeds are not working or you want to input custom content**")
        
        with st.form("manual_gen_post"):
            manual_title = st.text_input("Article Title")
            manual_summary = st.text_area("Summary")
            manual_source = st.text_input("Source")
            manual_link = st.text_input("Link (optional)")
            
            # Add style selection for manual entry too
            manual_style_options = {
                "Consultative (strategic, frameworks)": "consultative",
                "Punchy (short, bold claims)": "punchy", 
                "Casual (friendly, conversational)": "casual"
            }
            
            manual_style_display = st.selectbox("Post Style", 
                list(manual_style_options.keys()),
                help="Writing style for the generated content"
            )
            
            manual_post_style = manual_style_options[manual_style_display]
            manual_generate = st.form_submit_button("Generate from Manual Input")
        
        if manual_generate and manual_title and manual_summary and manual_source:
            try:
                res = requests.post(f"{API_URL}/posts/generate", json={
                    "title": manual_title,
                    "summary": manual_summary,
                    "source": manual_source,
                    "link": manual_link,
                    "post_style": manual_post_style
                })
                res.raise_for_status()
                result = res.json()
                st.subheader("💬 Generated Post (Manual)")
                st.code(result["post"], language="markdown")
                st.success("✅ Post generated from manual input!")
                
                # Show generation details for manual entry too
                with st.expander("ℹ️ Manual Generation Details"):
                    st.json({
                        "method": result.get("method", "unknown"),
                        "style_used": result.get("style_used", "unknown"),
                        "key_insights": result.get("key_insights", []),
                        "specific_detail_used": result.get("specific_detail", "None")[:100] + "..." if result.get("specific_detail") else "None"
                    })
                    
            except requests.RequestException as e:
                st.error(f"Error generating post: {e}")

# --- RECENT POSTS TAB ---
with tabs[2]:
    st.header("📰 Recent Generated Posts")
    
    try:
        res = requests.get(f"{API_URL}/posts/")
        res.raise_for_status()
        posts = res.json()
    except requests.RequestException as e:
        st.error(f"Error fetching posts: {e}")
        posts = []
    
    if posts:
        st.write(f"Total Posts Generated: {len(posts)}")
        
        for i, post in enumerate(posts):
            with st.expander(f"📄 {post.get('title', 'Untitled')} - {post.get('source', 'Unknown Source')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Title:** {post.get('title', 'N/A')}")
                    st.markdown(f"**Source:** {post.get('source', 'N/A')}")
                    if post.get('link'):
                        st.markdown(f"**Link:** [Read Original]({post['link']})")
                    st.markdown(f"**Created:** {post.get('created_at', 'Unknown')}")
                
                with col2:
                    st.markdown("**Summary:**")
                    st.text(post.get('summary', 'No summary available'))
                
                st.markdown("**Generated Content:**")
                st.code(post.get('generated_content', 'No content'), language="markdown")
    else:
        st.info("No posts generated yet. Go to the 'Generate Post' tab to create your first post!")

# --- SUBSCRIBERS TAB ---
with tabs[3]:
    st.header("📬 Subscriber List")

    try:
        res = requests.get(f"{API_URL}/subscribers/")
        res.raise_for_status()
        emails = res.json()
    except requests.RequestException as e:
        st.error(f"Error fetching subscribers: {e}")
        emails = []

    if emails:
        st.write(f"Total Subscribers: {len(emails)}")
        st.table([{"Email": email} for email in emails])
    else:
        st.info("No subscribers yet.")
