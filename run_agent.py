import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent


async def main() -> None:
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(
        user_id="github-actions",
        app_name="job-finder-agent",
    )
    runner = Runner(
        agent=root_agent,
        app_name="job-finder-agent",
        session_service=session_service,
    )
    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=(
                    "Run the job search now. Read my resume, find matching jobs, "
                    "and send the HTML report by email."
                )
            )
        ],
    )

    async for event in runner.run_async(
        user_id="github-actions",
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())