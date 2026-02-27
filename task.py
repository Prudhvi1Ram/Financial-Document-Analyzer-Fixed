from crewai import Task
from agents import (
    verifier,
    financial_analyst,
    investment_advisor,
    risk_assessor
)


verification = Task(
    description=(
        "Using the financial_summary below, determine whether it contains structured financial "
        "information such as revenue, income statements, margins, or cash flow.\n\n"
        "Financial Summary:\n{financial_summary}"
    ),
    expected_output="Confirmation with reasoning.",
    agent=verifier
)


analyze_financial_document = Task(
    description=(
        "Using the financial_summary below, analyze:\n"
        "- Revenue trends\n"
        "- Net income\n"
        "- Operating margins\n"
        "- Cash flow\n"
        "- Growth patterns\n\n"
        "Financial Summary:\n{financial_summary}"
    ),
    expected_output="Structured financial analysis.",
    agent=financial_analyst
)


investment_analysis = Task(
    description=(
        "Using only the financial_summary below, provide:\n"
        "- Strengths\n"
        "- Weaknesses\n"
        "- Short-term outlook\n"
        "- Long-term outlook\n"
        "- Buy/Hold/Sell recommendation\n\n"
        "Financial Summary:\n{financial_summary}"
    ),
    expected_output="Structured investment recommendation.",
    agent=investment_advisor
)


risk_assessment = Task(
    description=(
        "Using only the financial_summary below, evaluate:\n"
        "- Financial risks\n"
        "- Liquidity risks\n"
        "- Revenue volatility\n"
        "- Market risks\n"
        "- Overall risk rating\n\n"
        "Financial Summary:\n{financial_summary}"
    ),
    expected_output="Structured risk assessment.",
    agent=risk_assessor
)