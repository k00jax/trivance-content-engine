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
        name = st.text_input("Feed Name")
        url = st.text_input("Feed URL")
        submitted = st.form_submit_button("Add Feed")
        if submitted and name and url:
            res = requests.post(f"{API_URL}/feeds/", json={"name": name, "url": url})
            st.success(res.json()["message"])

    st.subheader("Current Feeds")
    res = requests.get(f"{API_URL}/feeds/")
    feeds = res.json()
    for f in feeds:
        st.markdown(f"- **{f['name']}** → {f['url']}")

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
