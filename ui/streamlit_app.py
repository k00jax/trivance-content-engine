import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Adjust if hosted remotely

st.set_page_config(page_title="Trivance AI Content Engine", layout="wide")
st.title("🧠 Trivance AI – Content Engine Dashboard")

tabs = st.tabs(["📡 Feeds", "✍️ Generate Post", "📬 Subscribers"])

# --- FEEDS TAB ---
with tabs[0]:
    st.header("📡 Manage RSS Feeds")
    
    with st.form("add_feed"):
        if "feed_name" not in st.session_state:
            st.session_state.feed_name = ""
        if "feed_url" not in st.session_state:
            st.session_state.feed_url = ""

        name = st.text_input("Feed Name", key="feed_name")
        url = st.text_input("Feed URL", key="feed_url")
        submitted = st.form_submit_button("Add Feed")

        if submitted and name and url:
            res = requests.post(f"{API_URL}/feeds/", json={"name": name, "url": url})
            st.success(res.json()["message"])
            st.session_state.feed_name = ""
            st.session_state.feed_url = ""
            st.experimental_rerun()


    st.subheader("Current Feeds")
    res = requests.get(f"{API_URL}/feeds/")
    feeds = res.json()

    for i, f in enumerate(feeds):
        cols = st.columns([5, 1])
        with cols[0]:
            st.markdown(f"**{f['name']}** → {f['url']}")
        with cols[1]:
            if st.button("🗑 Remove", key=f"remove_{i}"):
                requests.delete(f"{API_URL}/feeds/", params={"name": f["name"]})
                st.experimental_rerun()


# --- POST GENERATOR TAB ---
with tabs[1]:
    st.header("✍️ Generate AI-Driven Post")

    with st.form("gen_post"):
        title = st.text_input("Article Title")
        summary = st.text_area("Summary")
        source = st.text_input("Source")
        link = st.text_input("Link")
        generate = st.form_submit_button("Generate Post")
    
    if generate and title and summary and source:
        res = requests.post(f"{API_URL}/posts/generate", json={
            "title": title,
            "summary": summary,
            "source": source,
            "link": link
        })
        st.subheader("💬 Draft Output")
        st.code(res.json()["post"], language="markdown")

# --- SUBSCRIBERS TAB ---
with tabs[2]:
    st.header("📬 Subscriber List")

    res = requests.get(f"{API_URL}/subscribers/")
    emails = res.json()

    if emails:
        st.write(f"Total Subscribers: {len(emails)}")
        st.table([{"Email": email} for email in emails])
    else:
        st.info("No subscribers yet.")
