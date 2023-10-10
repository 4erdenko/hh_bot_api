import logging
from typing import Any, Dict

import httpx

from external_services.anti_captcha import get_captcha_solution
from settings.config import config

logger = logging.getLogger(__name__)


class HHBotApi:
    def __init__(
        self,
        login_url: str,
        resume_url: str,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        payload_up: Dict[str, Any],
    ) -> None:
        self.LOGIN_URL: str = login_url
        self.RESUME_URL: str = resume_url
        self.HEADERS: Dict[str, str] = headers
        self.PAYLOAD: Dict[str, Any] = payload
        self.PAYLOAD_UP: Dict[str, Any] = payload_up
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            headers=self.HEADERS
        )
        logger.info(config.LOG_INITIALIZING)

    async def initialize(self) -> None:
        try:
            logger.info(config.LOG_PRE_LOGIN)
            await self._pre_login()
            logger.info(config.LOG_LOGIN)
            await self._login()
        except Exception as e:
            logger.info(f'{config.LOG_EXCEPTION}: {e}')

    async def _pre_login(self) -> None:
        try:
            response: httpx.Response = await self.client.get(self.LOGIN_URL)
            _xsrf_value: str = response.cookies['_xsrf']
            self.client.headers.update({'X-XSRFToken': _xsrf_value})
            self.HEADERS['X-XSRFToken'] = _xsrf_value
            logger.info(config.LOG_PRE_LOGIN_SUCCESS)
        except Exception as e:
            logger.info(f'{config.LOG_EXCEPTION}: {e}')

    async def _login(self) -> None:
        try:
            response: httpx.Response = await self.client.post(
                self.LOGIN_URL, headers=self.HEADERS, data=self.PAYLOAD
            )
            user_hhid = response.json().get('hhid')
            is_bot = response.json().get('hhcaptcha').get('isBot')
            if is_bot:
                logger.warning(config.LOG_CAPTCHA)
                await self._captcha_handler(response)
                await self._login()
            else:
                if user_hhid:
                    logger.info(config.LOG_LOGIN_SUCCESS)
                else:
                    logger.error(config.LOG_LOGIN_ERROR)
        except Exception as e:
            logger.info(f'{config.LOG_EXCEPTION}: {e}')

    async def _captcha_handler(self, response):
        state = response.json().get('hhcaptcha').get('captchaState')
        key, image_url = await self._get_captcha()
        captcha_text = await get_captcha_solution(image_url)
        self.PAYLOAD.update(
            {
                'captchaText': captcha_text,
                'captchaState': state,
                'captchaKey': key,
            }
        )

    async def _get_captcha(self):
        get_key = await self.client.post(config.CAPTCHA_LINK)

        key = get_key.json().get('key')
        image = f'{config.CAPTCHA_IMAGE_LINK}{key}'
        return key, image

    async def update_resume(self, resume_id: str) -> None:
        try:
            logger.info(config.LOG_RESUME_UPDATE.format(resume_id))
            self.PAYLOAD_UP['resume'] = resume_id
            response: httpx.Response = await self.client.post(
                self.RESUME_URL, data=self.PAYLOAD_UP, headers=self.HEADERS
            )

            if response.status_code == httpx.codes.FORBIDDEN:
                logger.error(config.LOG_HTTP_EXCEPTION)
                raise config.LOG_HTTP_EXCEPTION
            elif (
                response.status_code == httpx.codes.FOUND
                or response.status_code == httpx.codes.CONFLICT
            ):
                logger.info(config.LOG_ALREADY_UPDATED)
            else:
                logger.info(config.LOG_RESUME_UPDATE_SUCCESS)
        except Exception as e:
            logger.info(f'{config.LOG_EXCEPTION}: {e}')
