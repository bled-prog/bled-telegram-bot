import asyncio
import logging

import sentry_sdk

from app import bot, logger_config
from app.config import settings
from app.libs import chatgpt
from app.libs.chatgpt import OpenAIAPI
from app.libs.wiki_api import WikiAPI


async def main():
    wiki_api = WikiAPI()
    chat_gpt = OpenAIAPI(
        base_url=settings.OPENAI_API_BASE_URL,
        api_key=settings.OPENAI_API_KEY.get_secret_value(),
        completions_settings=chatgpt.types.ChatCompletionsArgs(
            model=settings.OPENAI_API_MODEL,
            context=settings.OPENAI_CHAT_CONTEXT,
        )
    )
    await bot.start(settings.BOT_TOKEN, wiki_api, chat_gpt)


if __name__ == '__main__':
    logger_config.setup(settings.ENVIRONMENT)

    if settings.SENTRY_DSN.get_secret_value():
        logging.info('Sentry init')
        sentry_sdk.init(
            server_name='bled_tg_bot',
            dsn=settings.SENTRY_DSN.get_secret_value(),
            environment=settings.ENVIRONMENT,
            traces_sample_rate=settings.SENTRY_TRACES_RATE,
            profiles_sample_rate=settings.SENTRY_PROFILES_RATE
        )
    asyncio.run(main())
