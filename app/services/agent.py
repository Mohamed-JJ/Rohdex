from openai import OpenAI
from typing import TypeVar, Type, Any
from pydantic import BaseModel
from fastapi import Depends
from app.core import get_logger, get_settings, Settings

logger = get_logger()
T = TypeVar("T", bound=BaseModel)


class OpenAIService:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.OPENAI_APIKEY.get_secret_value(),
            organization=settings.ORG_ID,
        )

    async def get_json_output(
        self, content: str, schema: Type[T], system_prompt: str
    ) -> T:
        """
        Get structured JSON output from OpenAI.

        Args:
            content: The content to process
            schema: The Pydantic model to validate against
            system_prompt: The system prompt to use

        Returns:
            T: The validated response matching the schema
        """
        try:
            logger.info("Sending request to OpenAI")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content},
                ],
                temperature=0.0,
            )

            logger.info("Successfully received response from OpenAI")
            return schema.model_validate_json(response.choices[0].message.content)

        except Exception as e:
            logger.exception("Failed to get response from OpenAI")
            raise


# Dependency
def get_openai_service(settings: Settings = Depends(get_settings)) -> OpenAIService:
    return OpenAIService(settings)
