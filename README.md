# Personal Website

## Development Setup

Create and activate a virtual environment (e.g. via [uv](https://docs.astral.sh/uv/getting-started/installation/)):

```bash
uv venv --python 3.12 
source .venv/bin/activate
```

Install dependencies:

```bash
uv pip install -e .
uv pip install -e ".[dev]"
```

Run:

```bash
python -m app
```

Navigate to `http://localhost:5001`

## Deployment to Heroku

Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

If dependencies were changed in pyproject.toml, update requirements.txt:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

Login:

```bash
heroku login
```

Push to Heroku:

```bash
git push heroku master
```
