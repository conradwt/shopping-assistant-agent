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

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


# In-memory store of active discount codes and their status.
# Format: code -> {"discount": str, "redeemed": bool, "user_id": str | None}
DISCOUNT_CODES = {
    "WELCOME50": {"discount": "50% off", "redeemed": False, "user_id": None},
    "SUMMER20": {"discount": "20% off", "redeemed": False, "user_id": None},
}

# In-memory list of registered user IDs.
REGISTERED_USERS = {"user_01", "user_02", "customer_101", "buyer_99", "conradwt"}

# In-memory store of user loyalty points.
LOYALTY_POINTS = {user: 0 for user in REGISTERED_USERS}


def redeem_discount_code(code: str, user_id: str) -> dict:
    """Redeems a single-use discount code for a registered user.

    Args:
        code: The discount code to redeem (e.g., WELCOME50, SUMMER20).
        user_id: The registered user ID.

    Returns:
        A dictionary containing the status and details of the redemption.
    """
    code_upper = code.upper().strip()
    user_id_clean = user_id.strip()

    if user_id_clean not in REGISTERED_USERS:
        return {
            "success": False,
            "message": f"User ID '{user_id}' is not registered. Registration is required to redeem codes.",
        }

    if code_upper not in DISCOUNT_CODES:
        return {"success": False, "message": f"Discount code '{code}' is invalid."}

    promo = DISCOUNT_CODES[code_upper]
    if promo["redeemed"]:
        return {
            "success": False,
            "message": f"Discount code '{code_upper}' has already been redeemed by user '{promo['user_id']}'.",
        }

    # Mark as redeemed
    promo["redeemed"] = True
    promo["user_id"] = user_id_clean

    return {
        "success": True,
        "message": f"Successfully redeemed code '{code_upper}' for user '{user_id_clean}'!",
        "discount": promo["discount"],
    }


def award_loyalty_points(user_id: str, points: int) -> dict:
    """Awards loyalty points to a registered user ID after a successful purchase.

    Args:
        user_id: The registered user ID.
        points: The positive integer number of points to award (maximum 1000 per call).

    Returns:
        A dictionary containing the status and new balance of the user's loyalty points.
    """
    user_id_clean = user_id.strip()

    if user_id_clean not in REGISTERED_USERS:
        return {
            "success": False,
            "message": f"User ID '{user_id}' is not registered. Cannot award loyalty points.",
        }

    if points <= 0:
        return {
            "success": False,
            "message": "Awarded points must be a positive integer greater than zero.",
        }

    if points > 1000:
        return {
            "success": False,
            "message": "Point award exceeds the transaction cap of 1000 points.",
        }

    # Add points
    current_points = LOYALTY_POINTS.get(user_id_clean, 0)
    new_points = current_points + points
    LOYALTY_POINTS[user_id_clean] = new_points

    return {
        "success": True,
        "message": f"Successfully awarded {points} loyalty points to user '{user_id_clean}'!",
        "points_awarded": points,
        "new_balance": new_points,
    }


root_agent = Agent(
    name="shopping_assistant",
    model=Gemini(
        model="gemini-flash-latest",
        api_key="AIzaSyD-mock-key-value-12345",  # type: ignore
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI shopping assistant for a retail store. Help customers with their shopping inquiries, recommend products, assist registered users in redeeming single-use discount codes (like WELCOME50 and SUMMER20) by asking for their user ID and calling the redeem_discount_code tool, and award loyalty points to registered users after a successful purchase by calling the award_loyalty_points tool.",
    tools=[redeem_discount_code, award_loyalty_points],
)

app = App(
    root_agent=root_agent,
    name="app",
)
