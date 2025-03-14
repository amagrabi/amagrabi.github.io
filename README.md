# Personal Website

## Development Setup

Create and activate a virtual environment (e.g. via [uv](https://docs.astral.sh/uv/getting-started/installation/)):

```bash
uv venv --python 3.12 
source .venv/bin/activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Run:

```bash
python -m app
```

Navigate to `http://localhost:5001`

## Deployment to Heroku

Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

Login:

```bash
heroku login
```

Push to Heroku:

```bash
git push heroku main
```
