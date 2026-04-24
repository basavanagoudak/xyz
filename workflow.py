from crewai import Crew, Task, Process
from agents import researcher, vision_analyst, coordinator, model_name


def create_reality_check_crew(input_text: str, input_image: str = ""):
    research_task = Task(
        description=(
            f"Investigate the following claim thoroughly:\n\n"
            f"CLAIM: \"{input_text}\"\n\n"
            f"1. Search for direct evidence supporting or denying this claim.\n"
            f"2. Search for expert opinions and scientific consensus.\n"
            f"3. Search for the original source of this claim.\n"
            f"4. Check for any fact-checks already published on this topic.\n"
            f"Record every source URL you find."
        ),
        expected_output=(
            "A detailed research report with: (a) key findings, (b) supporting evidence with URLs, "
            "(c) counter-evidence with URLs, (d) credibility assessment of sources."
        ),
        agent=researcher,
    )

    vision_task = Task(
        description=(
            f"Analyze the following image/media for authenticity:\n\n"
            f"IMAGE URL: {input_image if input_image else 'NONE PROVIDED'}\n\n"
            f"If no image is provided, return 'No image to analyze'.\n"
            f"Otherwise: search for the original context of this image, check for manipulation signs."
        ),
        expected_output=(
            "An image forensics report with: authenticity rating (AUTHENTIC/MANIPULATED/UNKNOWN), "
            "original source if found, and key observations."
        ),
        agent=vision_analyst,
    )

    synthesis_task = Task(
        description=(
            "Based on the research report and image forensics report provided, "
            "produce a final verdict. You MUST respond with ONLY a valid JSON object — "
            "no markdown, no extra text. Format:\n"
            '{"verdict": "...", "label": "TRUE|MOSTLY TRUE|MIXED|MOSTLY FALSE|FALSE|UNVERIFIABLE", '
            '"confidence": 0-100, "sources": ["url1", "url2", ...]}'
        ),
        expected_output='A valid JSON object with keys: verdict, label, confidence, sources.',
        agent=coordinator,
        context=[research_task, vision_task] if input_image else [research_task],
    )

    use_image = bool(input_image and input_image.strip())
    crew = Crew(
        agents=[researcher, vision_analyst, coordinator] if use_image else [researcher, coordinator],
        tasks=[research_task, vision_task, synthesis_task] if use_image else [research_task, synthesis_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew
