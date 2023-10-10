from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = '.env'

    LOGIN: str = Field(
        ...,
    )
    PASSWORD: str = Field(
        ...,
    )
    USER_AGENT: str = Field(
        ...,
    )
    ANTICAPTCHA_API_KEY: str = Field(
        ...,
    )
    LOGIN_LINK: str = 'https://hh.ru/account/login?backurl=%2F'
    RESUME_UP_POST_LINK: str = 'https://hh.ru/applicant/resumes/touch'
    CAPTCHA_LINK: str = 'https://hh.ru/captcha?lang=EN'
    CAPTCHA_IMAGE_LINK: str = 'https://hh.ru/captcha/picture?key='
    RESUME_LINKS: str = Field(
        ...,
    )

    @property
    def parsed_resume_links(self):
        return self.RESUME_LINKS.split(',')

    LOG_INITIALIZING: str = 'Initializing HHBotApi.'
    LOG_PRE_LOGIN: str = 'Performing pre-login steps.'
    LOG_LOGIN: str = 'Performing login.'
    LOG_LOGIN_ERROR: str = 'Login failed!'
    LOG_CAPTCHA: str = 'Got captcha!'
    LOG_RESUME_UPDATE: str = 'Updating resume with ID: {}'
    LOG_PRE_LOGIN_SUCCESS: str = 'Successfully acquired X-XSRFToken.'
    LOG_LOGIN_SUCCESS: str = 'Successfully logged in.'
    LOG_RESUME_UPDATE_SUCCESS: str = 'Successfully updated resume.'
    LOG_EXCEPTION: str = 'An exception has occurred.'
    LOG_START_MAIN_ROUTINE: str = 'Starting main routine.'
    LOG_MAIN_ROUTINE_SUCCESS: str = 'Main routine completed successfully.'
    LOG_HTTP_EXCEPTION: str = 'Credentials error!'
    LOG_ALREADY_UPDATED: str = 'Already updated'

    FOUR_HOURS: int = 4 * 3600
    TEN_MINUTES: int = 10 * 60
    SLEEP_TIME: int = FOUR_HOURS + TEN_MINUTES


config = Config()
PAYLOAD: dict = {
    '_xsrf': '',
    'backUrl': 'https://hh.ru/',
    'failUrl': '/account/login?backurl=%2F',
    'accountType': 'APPLICANT',
    'remember': 'yes',
    'username': config.LOGIN,
    'password': config.PASSWORD,
    'isBot': 'false',
    'captchaText': '',
}
PAYLOAD_UP: dict = {
    'undirectable': 'true',
    'resume': '',
}
HEADERS: dict = {
    'User-Agent': config.USER_AGENT,
    'Accept': 'application/json',
    'X-XSRFToken': '',
}
