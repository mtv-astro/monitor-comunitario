from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class EvolutionMessage:
    """Message payload expected by the Evolution notification provider."""

    phone: str
    text: str


class EvolutionNotificationProvider:
    """Thin Evolution API adapter.

    The provider is prepared early so the application contract is clear,
    but it should remain disabled while EVOLUTION_ENABLED=false.
    """

    def __init__(self, base_url: str, api_key: str, instance: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.instance = instance

    async def send_text(self, message: EvolutionMessage) -> None:
        """Send a text message through Evolution API.

        The exact endpoint may be adjusted according to the deployed
        Evolution API version. Keep this adapter isolated so changes do
        not leak into the rest of the application.
        """
        if not self.base_url or not self.api_key or not self.instance:
            raise ValueError("Evolution provider is not configured.")

        url = f"{self.base_url}/message/sendText/{self.instance}"
        headers = {"apikey": self.api_key}
        payload = {
            "number": message.phone,
            "text": message.text,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
