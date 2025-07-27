import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Adjust if hosted remotely

st.set_page_config(page_title="Trivance AI Content Engine", layout="wide")
st.title("🧠 Trivance AI – Content Engine Dashboard")

tabs = st.tabs(["📡 Feeds", "✍️ Generate Post", "📝 Recent Posts", "📬 Subscribers"])

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
    st.header("✍️ AI-Driven Content Generator")
    
    # Initialize session states
    if "article_queue" not in st.session_state:
        st.session_state.article_queue = []
    if "selected_article" not in st.session_state:
        st.session_state.selected_article = None
    if "post_style" not in st.session_state:
        st.session_state.post_style = "Trivance Default"
    if "platform" not in st.session_state:
        st.session_state.platform = "LinkedIn"
    if "generated_post" not in st.session_state:
        st.session_state.generated_post = ""
    if "media_url" not in st.session_state:
        st.session_state.media_url = None
    
    # === STEP 1: Article Fetch + Display Layout ===
    
    # Top section with article fetching and display
    top_col1, top_col2 = st.columns([1, 2])
    
    with top_col1:
        st.subheader("🔍 Article Fetching")
        
        # Fetch controls
        fetch_col1, fetch_col2 = st.columns([2, 1])
        
        with fetch_col1:
            if st.button("📰 FETCH ARTICLE", type="primary", use_container_width=True):
                try:
                    with st.spinner("Fetching top articles from all feeds..."):
                        # Get articles with max age filter
                        max_age = st.session_state.get("max_age", 3)
                        res = requests.get(f"{API_URL}/feeds/top-article", params={"max_age_days": max_age})
                        res.raise_for_status()
                        
                        # Get multiple articles for queue
                        articles_res = requests.get(f"{API_URL}/feeds/articles", params={"max_age_days": max_age})
                        articles_res.raise_for_status()
                        articles = articles_res.json()
                        
                        # Sort by relevance score and store in queue
                        articles_sorted = sorted(articles, key=lambda x: x.get("score", 0), reverse=True)
                        st.session_state.article_queue = articles_sorted[:10]  # Keep top 10
                        
                        if st.session_state.article_queue:
                            st.session_state.selected_article = st.session_state.article_queue[0]
                            st.success(f"✅ Fetched {len(st.session_state.article_queue)} articles!")
                        else:
                            st.warning("No articles found in the specified time range")
                            
                except requests.RequestException as e:
                    st.error(f"Error fetching articles: {e}")
        
        with fetch_col2:
            max_age = st.selectbox(
                "Max Age", 
                [1, 3, 7, 14], 
                index=1, 
                format_func=lambda x: f"{x} days",
                key="max_age"
            )
        
        # Next Article button (show after first fetch)
        if st.session_state.article_queue and len(st.session_state.article_queue) > 1:
            if st.button("⏭️ NEXT ARTICLE", use_container_width=True):
                # Find current article index and move to next
                current_idx = 0
                if st.session_state.selected_article:
                    current_title = st.session_state.selected_article.get("title", "")
                    for i, article in enumerate(st.session_state.article_queue):
                        if article.get("title", "") == current_title:
                            current_idx = i
                            break
                
                # Move to next article (cycle back to start if at end)
                next_idx = (current_idx + 1) % len(st.session_state.article_queue)
                st.session_state.selected_article = st.session_state.article_queue[next_idx]
                st.rerun()
    
    with top_col2:
        if st.session_state.selected_article:
            st.subheader("📄 Selected Article")
            
            article = st.session_state.selected_article
            
            # Article title (bold)
            st.markdown(f"**{article.get('title', 'No title available')}**")
            
            # Metadata row
            meta_col1, meta_col2, meta_col3 = st.columns(3)
            with meta_col1:
                st.metric("Relevance Score", f"{article.get('score', 0):.1f}")
            with meta_col2:
                published_date = article.get('published', 'Unknown')
                st.write(f"📅 **Published:** {published_date}")
            with meta_col3:
                source = article.get('source', 'Unknown Source')
                link = article.get('link', '#')
                st.markdown(f"🔗 **Source:** [{source}]({link})")
            
            # Enhanced Summary (scrollable)
            st.write("**📝 Enhanced Summary:**")
            summary = article.get('summary', 'No summary available')
            
            # Use a container with max height for long summaries
            if len(summary) > 300:
                st.text_area(
                    "",
                    value=summary,
                    height=150,
                    disabled=True,
                    key="article_summary_display"
                )
            else:
                st.write(summary)
                
            # Show enhancement indicator
            if len(summary) > 200:
                st.caption("✨ Enhanced summary using web scraping")
            
        else:
            st.info("🎯 Click 'FETCH ARTICLE' to get started with AI-powered content generation")
    
    st.divider()
    
    # === STEP 2: Bottom Controls – Post Generation Setup ===
    
    bottom_col1, bottom_col2 = st.columns([1, 2])
    
    with bottom_col1:
        st.subheader("🎨 Generation Controls")
        
        # Generate Post button
        generate_disabled = st.session_state.selected_article is None
        if st.button(
            "🚀 GENERATE POST", 
            type="primary", 
            disabled=generate_disabled,
            use_container_width=True
        ):
            if st.session_state.selected_article:
                try:
                    with st.spinner("Generating AI-powered post..."):
                        # Prepare generation parameters with correct field names
                        article = st.session_state.selected_article
                        payload = {
                            "title": article.get("title", ""),
                            "summary": article.get("summary", ""),
                            "source": article.get("source", "RSS Feed"),  # Ensure source is provided
                            "link": article.get("link", ""),  # Use 'link' not 'url'
                            "post_style": st.session_state.post_style,  # Use 'post_style' not 'style'
                            "platform": st.session_state.platform
                        }
                        
                        # Call generation API
                        gen_res = requests.post(f"{API_URL}/posts/generate", json=payload)
                        gen_res.raise_for_status()
                        
                        result = gen_res.json()
                        # Handle the correct response field name
                        generated_content = result.get("post", result.get("content", ""))
                        if generated_content:
                            st.session_state.generated_post = generated_content
                            st.success("✅ Post generated successfully!")
                        else:
                            st.warning("⚠️ Post generated but content is empty")
                            st.json(result)  # Debug: show the actual response
                        
                except requests.RequestException as e:
                    st.error(f"Error generating post: {e}")
        
        # Style selection dropdown
        st.session_state.post_style = st.selectbox(
            "📝 Post Style / Tone",
            ["Trivance Default", "Punchy", "Casual"],
            index=0,
            key="style_selector"
        )
        
        # Platform selection dropdown  
        st.session_state.platform = st.selectbox(
            "📱 Social Platform",
            ["LinkedIn", "Email Newsletter", "X.com"],
            index=0,
            key="platform_selector"
        )
        
        if generate_disabled:
            st.caption("⚠️ Select an article first to enable post generation")
    
    with bottom_col2:
        # === STEP 3: Post Output (Editable + Enhanced Tools) ===
        
        if st.session_state.generated_post:
            st.subheader("📝 Generated Post")
            
            # Editable post content
            edited_post = st.text_area(
                "Generated Post",
                value=st.session_state.generated_post,
                height=200,
                key="post_editor"
            )
            
            # Update session state with edits
            st.session_state.generated_post = edited_post
            
            # Tool buttons
            tool_col1, tool_col2 = st.columns(2)
            
            with tool_col1:
                # Hashtags are now included automatically in the generated post
                st.info("✨ Hashtags are automatically included in generated posts")
            
            with tool_col2:
                if st.button("🖼️ GENERATE MEDIA", use_container_width=True):
                    try:
                        with st.spinner("Generating media with DALL-E..."):
                            # Call media generation
                            media_res = requests.post(
                                f"{API_URL}/posts/media",
                                json={"content": edited_post}
                            )
                            
                            if media_res.status_code == 200:
                                media_data = media_res.json()
                                st.session_state.media_url = media_data.get("url", "")
                                st.success("✅ Media generated!")
                            else:
                                st.warning("Media generation not available yet")
                                
                    except requests.RequestException:
                        st.warning("Media generation service unavailable")
                
                # Fallback upload option
                uploaded_file = st.file_uploader(
                    "📁 Upload Media", 
                    type=['png', 'jpg', 'jpeg', 'gif'],
                    key="media_upload"
                )
                
                if uploaded_file:
                    st.session_state.media_url = f"uploaded_{uploaded_file.name}"
                    st.success("✅ Media uploaded!")
            
            # Display media preview
            if st.session_state.media_url:
                st.write("**🖼️ Media Preview:**")
                if st.session_state.media_url.startswith("http"):
                    st.image(st.session_state.media_url, width=300)
                else:
                    st.info(f"📎 Media attached: {st.session_state.media_url}")
            
            # === STEP 4: PUBLISH Button + Modal Confirmation ===
            
            publish_col1, publish_col2, publish_col3 = st.columns([1, 1, 1])
            
            with publish_col3:
                publish_disabled = not (edited_post and st.session_state.platform)
                
                if st.button(
                    "🚀 PUBLISH POST", 
                    type="primary",
                    disabled=publish_disabled,
                    use_container_width=True
                ):
                    # Show modal confirmation (using expander as modal substitute)
                    st.session_state.show_publish_modal = True
            
            # Modal simulation using expander
            if st.session_state.get("show_publish_modal", False):
                with st.expander("📋 Publish Confirmation", expanded=True):
                    st.write("**Ready to publish your post?**")
                    
                    st.write(f"**Platform:** {st.session_state.platform}")
                    st.write(f"**Content Length:** {len(edited_post)} characters")
                    
                    # Final preview
                    st.text_area("Final Content Preview", value=edited_post, height=100, disabled=True)
                    
                    if st.session_state.media_url:
                        st.write(f"**Media:** {st.session_state.media_url}")
                    
                    confirm_col1, confirm_col2 = st.columns(2)
                    
                    with confirm_col1:
                        if st.button("✅ CONFIRM & POST", type="primary", use_container_width=True):
                            # === STEP 5: Save Post to History ===
                            try:
                                # Save to post history
                                post_data = {
                                    "title": st.session_state.selected_article.get("title", ""),
                                    "source": st.session_state.selected_article.get("source", ""),
                                    "enhanced_summary": st.session_state.selected_article.get("summary", ""),
                                    "generated_post": edited_post,
                                    "platform": st.session_state.platform,
                                    "media": st.session_state.media_url,
                                    "hashtags": [tag.strip('#') for tag in edited_post.split() if tag.startswith('#')],
                                    "timestamp": "2025-07-26T00:00:00Z"  # Would use actual timestamp
                                }
                                
                                # Save to history (API call)
                                save_res = requests.post(f"{API_URL}/posts/save", json=post_data)
                                
                                if save_res.status_code == 200:
                                    st.success("🎉 Post published and saved to history!")
                                    
                                    # Log to terminal for now
                                    st.code(f"""
PUBLISHED POST TO {st.session_state.platform}:
                                    
{edited_post}

Source: {st.session_state.selected_article.get('link', 'N/A')}
Media: {st.session_state.media_url or 'None'}
                                    """)
                                    
                                    # Reset state
                                    st.session_state.show_publish_modal = False
                                    st.session_state.generated_post = ""
                                    st.session_state.media_url = None
                                    
                                else:
                                    st.error("Failed to save post to history")
                                    
                            except Exception as e:
                                st.error(f"Error publishing post: {e}")
                    
                    with confirm_col2:
                        if st.button("❌ Cancel", use_container_width=True):
                            st.session_state.show_publish_modal = False
                            st.rerun()
        
        else:
            st.info("📝 Generated posts will appear here after clicking 'GENERATE POST'")
    
    # Queue status indicator
    if st.session_state.article_queue:
        current_position = 1
        if st.session_state.selected_article:
            current_title = st.session_state.selected_article.get("title", "")
            for i, article in enumerate(st.session_state.article_queue):
                if article.get("title", "") == current_title:
                    current_position = i + 1
                    break
        
        st.caption(f"📊 Article queue: {current_position} of {len(st.session_state.article_queue)} loaded")

# --- RECENT POSTS TAB ---
with tabs[2]:
    st.header("📰 Post History & Analytics")
    
    # Fetch post history
    try:
        history_res = requests.get(f"{API_URL}/posts/history")
        history_res.raise_for_status()
        post_history = history_res.json()
    except requests.RequestException as e:
        st.error(f"Error fetching post history: {e}")
        post_history = []
    
    # Fetch regular posts for fallback
    try:
        posts_res = requests.get(f"{API_URL}/posts/")
        posts_res.raise_for_status()
        regular_posts = posts_res.json()
    except requests.RequestException as e:
        regular_posts = []
    
    # Combine and display
    if post_history:
        st.success(f"📊 Found {len(post_history)} posts in history")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_posts = len(post_history)
            st.metric("Total Posts", total_posts)
        
        with col2:
            platforms = [post.get('platform', 'Unknown') for post in post_history]
            most_used_platform = max(set(platforms), key=platforms.count) if platforms else 'N/A'
            st.metric("Top Platform", most_used_platform)
        
        with col3:
            total_chars = sum(post.get('character_count', 0) for post in post_history)
            avg_chars = total_chars // len(post_history) if post_history else 0
            st.metric("Avg. Length", f"{avg_chars} chars")
        
        with col4:
            total_hashtags = sum(len(post.get('hashtags', [])) for post in post_history)
            st.metric("Total Hashtags", total_hashtags)
        
        st.divider()
        
        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            platform_filter = st.selectbox(
                "Filter by Platform",
                ["All"] + list(set(post.get('platform', 'Unknown') for post in post_history)),
                index=0
            )
        
        with filter_col2:
            show_limit = st.slider("Show Posts", 5, 50, 10)
        
        # Filter posts
        filtered_posts = post_history
        if platform_filter != "All":
            filtered_posts = [post for post in post_history if post.get('platform') == platform_filter]
        
        # Display posts
        for i, post in enumerate(filtered_posts[:show_limit]):
            with st.expander(
                f"📄 {post.get('title', 'Untitled')[:60]}... | {post.get('platform', 'Unknown')} | {post.get('timestamp', '')[:10]}",
                expanded=False
            ):
                # Post metadata
                meta_col1, meta_col2 = st.columns(2)
                
                with meta_col1:
                    st.markdown(f"**📰 Title:** {post.get('title', 'N/A')}")
                    st.markdown(f"**📡 Source:** {post.get('source', 'N/A')}")
                    st.markdown(f"**📱 Platform:** {post.get('platform', 'N/A')}")
                    st.markdown(f"**📅 Published:** {post.get('timestamp', 'N/A')[:19]}")
                
                with meta_col2:
                    st.markdown(f"**📊 Character Count:** {post.get('character_count', 0)}")
                    st.markdown(f"**📝 Word Count:** {post.get('word_count', 0)}")
                    
                    hashtags = post.get('hashtags', [])
                    if hashtags:
                        st.markdown(f"**🏷️ Hashtags:** {', '.join(f'#{tag}' for tag in hashtags[:5])}")
                    
                    if post.get('media'):
                        st.markdown(f"**🖼️ Media:** {post.get('media')}")
                
                # Enhanced Summary
                if post.get('enhanced_summary'):
                    st.markdown("**📋 Original Article Summary:**")
                    st.text_area(
                        "",
                        value=post['enhanced_summary'],
                        height=100,
                        disabled=True,
                        key=f"summary_{i}"
                    )
                
                # Generated Post
                st.markdown("**✍️ Generated Post:**")
                st.text_area(
                    "",
                    value=post.get('generated_post', 'No content'),
                    height=150,
                    disabled=True,
                    key=f"post_{i}"
                )
                
                # Action buttons
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button(f"📋 Copy Post", key=f"copy_{i}"):
                        st.success("Post copied to clipboard! (feature would copy in production)")
                
                with action_col2:
                    if st.button(f"🔄 Regenerate", key=f"regen_{i}"):
                        st.info("Would regenerate this post with current settings")
                
                with action_col3:
                    if st.button(f"📊 Analytics", key=f"analytics_{i}"):
                        st.info("Would show post performance analytics")
    
    elif regular_posts:
        st.info("📝 Showing legacy posts (upgrade to new history format)")
        
        for i, post in enumerate(regular_posts[:10]):
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
        st.info("📝 No posts generated yet. Go to the 'Generate Post' tab to create your first post!")
        
        # Show example of what post history will look like
        with st.expander("🎯 What you'll see here", expanded=True):
            st.markdown("""
            **Your post history will include:**
            - 📊 Analytics dashboard with metrics
            - 📱 Platform-specific post tracking  
            - 🏷️ Hashtag performance
            - 📈 Content length statistics
            - 🔄 One-click regeneration
            - 📋 Copy/export functionality
            
            *Start generating posts to build your content library!*
            """)

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
