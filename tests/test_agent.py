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

import pytest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import DISCOUNT_CODES, root_agent


@pytest.fixture(autouse=True)
def reset_discount_codes():
    """Resets the discount codes state before each test."""
    DISCOUNT_CODES["WELCOME50"]["redeemed"] = False
    DISCOUNT_CODES["WELCOME50"]["user_id"] = None
    DISCOUNT_CODES["SUMMER20"]["redeemed"] = False
    DISCOUNT_CODES["SUMMER20"]["user_id"] = None


def run_agent_interaction(prompt: str) -> str:
    """Runs a single interaction with the agent and returns the final concatenated response text."""
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="test_user", app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    message = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])

    events = list(
        runner.run(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
        )
    )

    response_texts = []
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_texts.append(part.text)
    return " ".join(response_texts)


def test_agent_redeem_discount_success() -> None:
    """Verifies that a registered user can successfully redeem a valid code."""
    response = run_agent_interaction("Please redeem WELCOME50 for user_01")
    assert "success" in response.lower() or "redeem" in response.lower()
    assert "50%" in response


def test_agent_redeem_discount_unregistered_user() -> None:
    """Verifies that the agent refuses to redeem a code for an unregistered user ID."""
    response = run_agent_interaction(
        "Please redeem WELCOME50 for unregistered_user_123"
    )
    assert (
        "not registered" in response.lower()
        or "required" in response.lower()
        or "cannot" in response.lower()
    )


def test_agent_redeem_discount_duplicate() -> None:
    """Verifies that a code cannot be redeemed twice."""
    # First redemption should succeed
    response1 = run_agent_interaction("Please redeem WELCOME50 for user_01")
    assert "50%" in response1

    # Second redemption should fail
    response2 = run_agent_interaction("Please redeem WELCOME50 for user_02")
    assert "already" in response2.lower() or "fail" in response2.lower()


def test_agent_redeem_discount_invalid_code() -> None:
    """Verifies that the agent rejects invalid codes."""
    response = run_agent_interaction("Please redeem INVALIDCODE99 for user_01")
    assert (
        "invalid" in response.lower()
        or "does not exist" in response.lower()
        or "not valid" in response.lower()
    )
