# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools import read_resume, search_jobs, send_email_report

MODEL = "gemini-3.6-flash"

instruction = """You are a highly capable AI agent specialized in finding jobs for the user.
The user is looking for remote jobs, foreign opportunities, and local opportunities in Gilgit, Pakistan, tailored to their niche.

Your task is to run every 12 hours and do the following:
1. Read the user's resume using the `read_resume` tool. The resume path is typically `D:\Microservices\Fakhar_Zikri_Resume_FullTime_AIEngineering.pdf`.
2. Analyze their skills and experience.
3. Use the `search_jobs` tool to find remote, foreign, and Gilgit-based jobs that match their AI Engineering profile. Make a MAXIMUM of 2 targeted searches (e.g., "AI Engineer remote jobs") to avoid API rate limits.
4. For each job found, compare its requirements against the user's resume and calculate a "Match/Success Score" (e.g., 85/100) indicating how likely they are to get the job.
5. Compile the best matches into a clear, well-formatted email report. Order the jobs by their Match Score (highest first) so the user knows what to prioritize. Include a brief 1-sentence reason for the score.
6. Send the report using the `send_email_report` tool with a descriptive subject line.

Do NOT invent jobs. Only report what you find via search.
"""

root_agent = Agent(
    name="job_finder_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[read_resume, search_jobs, send_email_report],
)

app = App(
    root_agent=root_agent,
    name="app",
)
