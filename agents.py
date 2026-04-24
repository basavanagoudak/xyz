import os
from typing import List, Dict, Any
from crewai import Agent
from tools import search_web, analyze_image
from config import config

# Use the model name string directly. CrewAI uses LiteLLM to handle these.
# Ensure the GROQ_API_KEY is in the environment.
os.environ["GROQ_API_KEY"] = config.GROQ_API_KEY or ""
model_name = "groq/llama-3.3-70b-versatile"

# Define Agents
researcher = Agent(
    role='Fact-Checking Researcher',
    goal='Search the web and gather evidence to verify claims.',
    backstory='You are an expert researcher with a keen eye for detail. You specialize in identifying misinformation and finding credible sources to back up or debunk claims.',
    tools=[search_web],
    llm=model_name,
    verbose=True,
    allow_delegation=False
)

vision_analyst = Agent(
    role='Image Forensic Analyst',
    goal='Analyze images to detect manipulation and extract forensic evidence.',
    backstory='You are a specialist in digital forensics. You can spot anomalies in images that indicate tampering, deepfakes, or AI generation.',
    tools=[analyze_image],
    llm=model_name,
    verbose=True,
    allow_delegation=False
)

coordinator = Agent(
    role='Information Integrity Coordinator',
    goal='Synthesize findings from researchers and analysts to provide a final verdict.',
    backstory='You are the final authority on truth. You take reports from your team and weigh the evidence to reach a definitive conclusion with a confidence score.',
    llm=model_name,
    verbose=True,
    allow_delegation=True
)
