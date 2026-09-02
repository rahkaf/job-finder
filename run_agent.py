import asyncio
import uuid
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

async def main():
    from app.agent import app
    from app.app_utils import services
    from google.adk.runners import Runner
    
    runner = Runner(
        app=app,
        session_service=services.get_session_service(),
        artifact_service=services.get_artifact_service(),
        auto_create_session=True,
    )
    msg = types.Content(role="user", parts=[types.Part.from_text(text="Find remote and Gilgit jobs for me based on my resume and email me the report.")])
    print("Running agent...")
    async for event in runner.run_async(
        user_id="github-action",
        session_id=str(uuid.uuid4()),
        new_message=msg,
    ):
        pass
    print("\nAgent run complete!")

if __name__ == "__main__":
    asyncio.run(main())
