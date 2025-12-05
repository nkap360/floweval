"""
AI Proxy Service
=================
Proxy service to handle external AI API requests and avoid CORS issues.
"""

import logging
import os
from typing import List

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])

# Load AI provider base URLs from environment variables
DEEPSEEK_BASE_URL = os.getenv(
    "DEEPSEEK_BASE_URL", "https://api.deepseek.com"
)
CUSTOM_OPENAI_BASE_URL = os.getenv(
    "CUSTOM_OPENAI_BASE_URL", "https://api.openai.com/v1"
)
OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", "https://api.openai.com/v1"
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    provider: str
    model: str
    messages: List[ChatMessage]
    stream: bool = False
    api_key: str


class ChatResponse(BaseModel):
    content: str


@router.post("/chat/completions")
async def chat_completions(request: ChatRequest):
    """
    Proxy endpoint for AI chat completions.
    Handles requests to OpenAI, DeepSeek, and other compatible APIs.
    """
    logger.info(
        "[AI_PROXY] Starting chat completion request | Provider: %s",
        request.provider
    )
    logger.info(
        "[AI_PROXY] Model: %s | Stream: %s | Messages: %d",
        request.model,
        request.stream,
        len(request.messages)
    )
    
    try:
        # Determine base URL based on provider (from environment)
        if request.provider == "deepseek":
            base_url = DEEPSEEK_BASE_URL
        elif request.provider == "custom_openai_endpoint":
            base_url = CUSTOM_OPENAI_BASE_URL
        elif request.provider == "openai":
            base_url = OPENAI_BASE_URL
        else:
            logger.error(
                "[AI_PROXY] Unsupported provider requested: %s",
                request.provider
            )
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported provider: {request.provider}"
            )

        # Prepare headers
        api_key_preview = (
            f"{request.api_key[:10]}..."
            if len(request.api_key) > 10
            else "***"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key_preview}"
        }

        # Prepare request body
        body = {
            "model": request.model,
            "messages": [msg.dict() for msg in request.messages],
            "stream": request.stream
        }

        logger.info(
            "[AI_PROXY] Proxying to %s | URL: %s/chat/completions",
            request.provider,
            base_url
        )
        logger.debug(
            "[AI_PROXY] API Key: %s",
            "present" if request.api_key else "MISSING"
        )
        
        # Update headers with actual API key for request
        headers["Authorization"] = f"Bearer {request.api_key}"

        # If streaming is requested
        if request.stream:
            logger.info("[AI_PROXY] Using streaming mode")

            async def generate_stream():
                try:
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        logger.debug(
                            "[AI_PROXY] Initiating stream to %s",
                            f"{base_url}/chat/completions"
                        )
                        async with client.stream(
                            "POST",
                            f"{base_url}/chat/completions",
                            headers=headers,
                            json=body
                        ) as response:
                            if response.status_code != 200:
                                error_text = await response.aread()
                                logger.error(
                                    "[AI_PROXY] Streaming API error"
                                )
                                logger.error(
                                    "Status: %s | Provider: %s",
                                    response.status_code,
                                    request.provider
                                )
                                logger.error(
                                    "Response: %s",
                                    error_text.decode()
                                )
                                raise HTTPException(
                                    status_code=response.status_code,
                                    detail=f"API error: {error_text.decode()}"
                                )
                            
                            logger.info(
                                "[AI_PROXY] Stream established successfully"
                            )
                            async for chunk in response.aiter_bytes():
                                yield chunk
                except Exception as e:
                    logger.error(
                        "[AI_PROXY] Stream generation error"
                    )
                    logger.error(
                        "Type: %s | Error: %s",
                        type(e).__name__,
                        str(e),
                        exc_info=True
                    )
                    raise

            return StreamingResponse(
                generate_stream(), media_type="text/event-stream"
            )

        # Non-streaming request
        logger.info("[AI_PROXY] Using non-streaming mode")
        async with httpx.AsyncClient(timeout=60.0) as client:
            logger.debug(
                "[AI_PROXY] Sending POST to %s",
                f"{base_url}/chat/completions"
            )
            response = await client.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=body
            )

            if response.status_code != 200:
                error_text = response.text
                logger.error(
                    "[AI_PROXY] Non-streaming API error"
                )
                logger.error(
                    "Status: %s | Provider: %s | Model: %s",
                    response.status_code,
                    request.provider,
                    request.model
                )
                logger.error("Response: %s", error_text)
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API error: {error_text}"
                )

            logger.info("[AI_PROXY] Received successful response")
            data = response.json()
            choices = data.get("choices", [{}])
            content = choices[0].get("message", {}).get("content", "")
            
            logger.info(
                "[AI_PROXY] Extracted content length: %d characters",
                len(content) if content else 0
            )
            
            return ChatResponse(content=content)

    except httpx.TimeoutException as exc:
        logger.error(
            "[AI_PROXY] Request timeout | Provider: %s | Model: %s",
            request.provider,
            request.model,
            exc_info=True
        )
        logger.error("URL: %s", base_url)
        raise HTTPException(
            status_code=504, detail="Request timeout"
        ) from exc
    except httpx.RequestError as exc:
        logger.error(
            "[AI_PROXY] Request error | Provider: %s | Model: %s | Error: %s",
            request.provider,
            request.model,
            str(exc),
            exc_info=True
        )
        raise HTTPException(
            status_code=502, detail=f"Request error: {str(exc)}"
        ) from exc
    except HTTPException:
        # Re-raise HTTP exceptions without wrapping
        raise
    except Exception as exc:
        logger.error(
            "[AI_PROXY] Unexpected error | Provider: %s | Model: %s",
            request.provider,
            request.model,
            exc_info=True
        )
        logger.error(
            "Type: %s | Error: %s",
            type(exc).__name__,
            str(exc)
        )
        raise HTTPException(
            status_code=500,
            detail=(
                f"Internal server error: "
                f"{type(exc).__name__}: {str(exc)}"
            )
        ) from exc
