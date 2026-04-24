from crewai import Crew, Task, Process
from agents import researcher, vision_analyst, coordinator, model_name

def create_reality_check_crew(input_text, input_image):
    # Define Tasks
    research_task = Task(
        description=f"Research the following claim and provide a detailed report with evidence: '{input_text}'",
        expected_output="A comprehensive report summarizing findings, sources, and a preliminary truthfulness assessment.",
        agent=researcher
    )

    vision_task = Task(
        description=f"Analyze the image provided (if any) for signs of manipulation or context: '{input_image}'",
        expected_output="An image forensic report detailing any anomalies, metadata issues, or deepfake probabilities.",
        agent=vision_analyst
    )

    synthesis_task = Task(
        description="Synthesize the research and vision reports to provide a final verdict on the claim. Return a JSON-like structure with 'verdict' and 'confidence'.",
        expected_output="A final verdict summary and a confidence score between 0-100.",
        agent=coordinator,
        context=[research_task, vision_task] if input_image else [research_task]
    )

    # Define Crew
    crew = Crew(
        agents=[researcher, vision_analyst, coordinator] if input_image else [researcher, coordinator],
        tasks=[research_task, vision_task, synthesis_task] if input_image else [research_task, synthesis_task],
        process=Process.hierarchical,
        manager_llm=model_name,
        verbose=True
    )
    
    return crew
