import io

import httpx
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from tenacity import retry, stop_after_attempt, wait_fixed

from settings.config import config


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
async def get_captcha_solution(captcha_url):
    async with httpx.AsyncClient() as client:
        response = await client.get(captcha_url)
        captcha_image = response.content

    captcha_image_io = io.BytesIO(captcha_image)

    client = AnticaptchaClient(config.ANTICAPTCHA_API_KEY)
    task = ImageToTextTask(captcha_image_io)
    job = client.createTask(task)
    job.join()
    return job.get_captcha_text()


if __name__ == '__main__':
    import asyncio

    captcha_url = 'https://hh.ru/captcha/picture?key='
    result = asyncio.run(get_captcha_solution(captcha_url))
    print(f'Captcha solution: {result}')
