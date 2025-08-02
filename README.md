# tech-professional-coacher

<img width="1247" height="498" alt="image" src="https://github.com/user-attachments/assets/9d121dd5-5fa6-4f80-93ce-ba8be12b00f1" />


## Overview

The Professional Coach Assistant System is designed to support individuals preparing for technology-related careers by automating research, analysis, and guidance tasks. The system is structured as a team of specialized agents, each focusing on a distinct aspect of the job search and interview process, all coordinated by a central supervisor agent.

## System Architecture

### Supervisor Agent

- **Professional CoachAssistant (Supervisor)**
  - Oversees and coordinates the activities of all specialist agents.
  - Ensures seamless workflow and information sharing between specialists.

### Specialist Agents and Tools

1. **Tech Job Researcher (Specialist)**
   - Focus: Researches technology job opportunities.
   - Tools:
     - *LinkedIn Job Positions Scrapper*: Extracts job listings from LinkedIn.
     - *Glassdoor Job Positions Scrapper*: Extracts job listings from Glassdoor.

2. **Personal Profiler Analyzer (Specialist)**
   - Focus: Analyzes candidate profiles and matches with relevant job descriptions.
   - Tool:
     - *Job Description WebScrapper*: Scrapes and analyzes job descriptions from various sources.

3. **Tech Journalist (Specialist)**
   - Focus: Gathers and summarizes news relevant to tech careers and employment trends.
   - Tool:
     - *News WebScrapper*: Collects news articles from tech industry sources.

4. **Resume Strategist for Engineers (Specialist)**
   - Focus: Guides engineers in tailoring their resumes and applying for positions.
   - Tools:
     - *Job Position Scrapper*: Identifies suitable job openings.
     - *Resume File Reader*: Reads and analyzes resume files.
     - *Resume File Writer*: Assists in creating or editing resumes.

5. **Tech Interview Preparer (Specialist)**
   - Focus: Prepares candidates for technical interviews.
   - Tools:
     - *Resume File Reader*: Reads and reviews resume files for interview preparation.
     - *Job Position Scrapper*: Gathers details about interview-relevant job roles.

## Workflow

The supervisor agent delegates tasks to specialist agents based on user needs. Each specialist utilizes dedicated scraping and analysis tools to automate data collection and processing, ensuring that candidates receive up-to-date and relevant information for their job search, resume optimization, and interview preparation.

## Use Cases

- Automated job position research from multiple platforms.
- Personalized profile analysis and job matching.
- Up-to-date news aggregation for career insights.
- Resume review and enhancement guidance for engineers.
- Targeted interview preparation using real job data.

See the above diagram for the flow of responsibilities and tools between the supervisor and specialist agents.

```
