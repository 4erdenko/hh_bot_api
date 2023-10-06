import asyncio
import logging
import sys

import coloredlogs

from api.hh_api_client import HHBotApi
from settings.config import HEADERS, PAYLOAD, PAYLOAD_UP, config

logger = logging.getLogger(__name__)


async def main():
    while True:
        try:
            logger.info(config.LOG_START_MAIN_ROUTINE)
            client = HHBotApi(
                login_url=config.LOGIN_LINK,
                resume_url=config.RESUME_UP_POST_LINK,
                headers=HEADERS,
                payload=PAYLOAD,
                payload_up=PAYLOAD_UP,
            )
            await client.initialize()
            for resume in config.parsed_resume_links:
                await client.update_resume(resume)
            logger.info(config.LOG_MAIN_ROUTINE_SUCCESS)
        except Exception as e:
            logger.error(f'{config.LOG_EXCEPTION}: {e}')
        await asyncio.sleep(config.SLEEP_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log', encoding='utf-8'),
        ],
    )

    coloredlogs.install(
        level='INFO',
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        isatty=True,
        stream=sys.stdout,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
