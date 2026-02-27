import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()

llm = LLM(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=1000  # reduced
)


verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether the provided financial summary contains structured financial data.",
    backstory="Expert in financial compliance and structured financial validation.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2
)


financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze the provided financial summary and extract financial insights.",
    backstory="Expert in corporate financial statements and profitability analysis.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide investment recommendations using the financial summary.",
    backstory="Certified portfolio strategist and valuation specialist.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2
)


risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Evaluate financial and market risks using the financial summary.",
    backstory="Specialist in risk modeling and macroeconomic exposure.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2
)