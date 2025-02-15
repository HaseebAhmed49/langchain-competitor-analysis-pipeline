from fastapi import FastAPI
from pydantic import BaseModel
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

app = FastAPI()
openai_api_key = os.getenv("OPENAI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/everything"


class CompetitorRequest(BaseModel):
    competitor: str


@app.post("/analyze/")
async def analyze_competitor(request: CompetitorRequest):
    competitor = request.competitor

    # Step 1: Fetch Articles from NewsAPI
    response = requests.get(NEWS_API_URL, params={
        "q": competitor,
        "language": "en",
        "apiKey": news_api_key
    })

    articles = response.json().get("articles", [])

    if not articles:
        return {"summary": "No relevant articles found"}

    # Extract content from top 5 articles
    raw_text = "\n".join([article["title"] + " - " + article["description"] for article in articles[:5] if article["description"]])

    # Step 2: Clean & Process Text
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(raw_text)

    # Step 3: Sentiment Analysis & Summarization
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4")

    template = "Summarize the key insights from this text: {text}"
    prompt = PromptTemplate(template=template, input_variables=["text"])
    summary_chain = LLMChain(llm=llm, prompt=prompt)

    summaries = [summary_chain.run(chunk) for chunk in chunks[:3]]
    final_summary = "\n".join(summaries)

    return {"competitor": competitor, "summary": final_summary}