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
"""
You can add your unit tests here.
This is where you test your business logic, including agent functionality,
data processing, and other core components of your application.
"""

from app.agent import (
    DISCOUNT_CODES,
    LOYALTY_POINTS,
    award_loyalty_points,
    redeem_discount_code,
)


def test_redeem_discount_code_success() -> None:
    # Reset status for testing
    DISCOUNT_CODES["WELCOME50"]["redeemed"] = False
    DISCOUNT_CODES["WELCOME50"]["user_id"] = None

    result = redeem_discount_code("WELCOME50", "conradwt")
    assert result["success"] is True
    assert "Successfully redeemed" in result["message"]
    assert result["discount"] == "50% off"

    # Try to redeem again
    result_again = redeem_discount_code("WELCOME50", "conradwt")
    assert result_again["success"] is False
    assert "already been redeemed" in result_again["message"]


def test_redeem_discount_code_invalid_user() -> None:
    result = redeem_discount_code("WELCOME50", "unregistered_user")
    assert result["success"] is False
    assert "not registered" in result["message"]


def test_redeem_discount_code_invalid_code() -> None:
    result = redeem_discount_code("INVALID_CODE", "conradwt")
    assert result["success"] is False
    assert "is invalid" in result["message"]


def test_award_loyalty_points_success() -> None:
    # Reset point status for testing
    LOYALTY_POINTS["conradwt"] = 0

    result = award_loyalty_points("conradwt", 100)
    assert result["success"] is True
    assert "Successfully awarded 100 loyalty points" in result["message"]
    assert result["points_awarded"] == 100
    assert result["new_balance"] == 100

    # Award again
    result2 = award_loyalty_points("conradwt", 250)
    assert result2["success"] is True
    assert result2["new_balance"] == 350


def test_award_loyalty_points_unregistered_user() -> None:
    result = award_loyalty_points("unregistered_user", 100)
    assert result["success"] is False
    assert "not registered" in result["message"]


def test_award_loyalty_points_negative_points() -> None:
    result = award_loyalty_points("conradwt", -10)
    assert result["success"] is False
    assert "positive integer greater than zero" in result["message"]

    result_zero = award_loyalty_points("conradwt", 0)
    assert result_zero["success"] is False
    assert "positive integer greater than zero" in result_zero["message"]


def test_award_loyalty_points_exceeds_cap() -> None:
    result = award_loyalty_points("conradwt", 1001)
    assert result["success"] is False
    assert "exceeds the transaction cap of 1000 points" in result["message"]
