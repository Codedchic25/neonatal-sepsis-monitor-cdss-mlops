"""Twilio Emergency SMS Notification and Alerting Engine.

Handles high-vigilance clinical alert routing, integrating third-party REST API
payload dispatches with fallback simulation loops to prevent runtime blockages.
"""

import os

from twilio.base.exceptions import TwilioRestException


class NotificationEngine:
    """Enterprise-grade rapid alerting and message orchestration platform for NICU wards."""

    def __init__(self) -> None:
        """Initializes the alerting module, safely extracting cryptographic keys from environment handlers."""
        self.account_sid: str | None = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token: str | None = os.getenv("TWILIO_AUTH_TOKEN")

        # Aliniat cu structura din .env (Caută TWILIO_TWILIO_PHONE, cu fallback pe TWILIO_FROM_NUMBER)
        self.from_number: str | None = os.getenv("TWILIO_TWILIO_PHONE") or os.getenv(
            "TWILIO_FROM_NUMBER"
        )
        self.client = None

        if self.account_sid and self.auth_token:
            try:
                from twilio.rest import Client

                self.client = Client(self.account_sid, self.auth_token)
            except ImportError:
                self.client = None

    def send_critical_sms(
        self,
        to_number: str,
        message_body: str,
        success_template: str,
        sim_template: str,
    ) -> str:
        """Dispatches an emergency SMS alert using pre-translated dictionary strings matching the active locale.

        Args:
            to_number (str): The target recipient clinical mobile number.
            message_body (str): The pre-translated text containing the telemetry risk payload.
            success_template (str): The localized UI success banner template string.
            sim_template (str): The localized UI sandbox simulation message fallback string.

        Returns:
            str: The structural execution status mapped directly to presentation layer layers.
        """
        if self.client and to_number and self.from_number:
            try:
                # Execute direct REST connection handshake with remote Twilio cloud servers
                self.client.messages.create(
                    body=message_body, from_=self.from_number, to=to_number
                )
                return success_template
            except TwilioRestException as e:
                # Intercept API authentication, format, or restriction exceptions gracefully
                return f"⚠️ Twilio REST Exception: {e!s}"
            except Exception as e:  # noqa: BLE001
                # Intercept socket-level failures and dynamic network resolution drops defensively
                return f"⚠️ Notification Network Fault: {e!r}"
        else:
            # Fallback local telemetry loop tracking: prints outputs cleanly to the terminal logs
            print(f"[SMS SIMULATION DISPATCH TO {to_number}]:\n{message_body}")
            return sim_template
