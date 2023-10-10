# HH Bot API

HH Bot API is a tool designed for automating actions on the HeadHunter platform. With its help, you can automatically update resumes, bypass captchas, and perform other related tasks.

## Features

- **Automatic Resume Update**: Automate the process of updating your resume on the platform.
- **Captcha Bypass**: Uses the [AntiCaptcha](https://anti-captcha.com/) service to bypass captchas encountered during the process.
- **Configurable**: Easily set up and integrate with your existing systems.

## Getting Started

### Prerequisites

- Docker

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/4erdenko/hh_bot_api.git
   ```

2. Navigate to the cloned directory:
   ```bash
   cd hh_bot_api
   ```

3. Create a `.env` file based on the provided [example](https://github.com/4erdenko/hh_bot_api/blob/master/.env_example). Ensure you fill in the necessary fields such as `LOGIN`, `PASSWORD`, `USER_AGENT`, `ANTICAPTCHA_API_KEY`, and `RESUME_LINKS`.

### Usage

- Using Docker directly:
  ```bash
  docker run -d --env-file .env 4erdenko/hh_bot_api:latest
  ```

- Using Docker Compose:
  ```bash
  docker compose up -d
  ```

## Configuration

- All project settings can be found in the [config.py](https://github.com/4erdenko/hh_bot_api/blob/master/settings/config.py) file.
- For captcha handling, you'll need an API key from the AntiCaptcha service.

## CI/CD

The project includes a [GitHub Actions workflow](https://github.com/4erdenko/hh_bot_api/blob/master/.github/workflows/main.yml) for automatic code checks, Docker image builds, and deployment.
