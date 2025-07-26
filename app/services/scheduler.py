from apscheduler.schedulers.background import BackgroundScheduler
from app.services.generator import generate_commentary

scheduler = BackgroundScheduler()

# Mock article for scheduled job
demo_article = {
    "title": "OpenAI’s New Model Shifts the Landscape Again",
    "summary": "OpenAI released GPT-4o with real-time voice and web vision. This has implications for CX and internal tooling.",
    "source": "TechCrunch",
    "link": "https://techcrunch.com/fake-link"
}

def scheduled_post_job():
    print("Generating scheduled post...")
    post = generate_commentary(demo_article)
    print(post["post"])  # Replace with push to Notion/email/post endpoint

def start_scheduler():
    scheduler.add_job(scheduled_post_job, "interval", days=7)
    scheduler.start()
