# GitHub Codespaces URL Format

## Correct URLs (WITHOUT :3000)
- Home: https://turbo-engine-v69xvg5j7v973x475-3000.app.github.dev/
- My Articles: https://turbo-engine-v69xvg5j7v973x475-3000.app.github.dev/articles/
- Write Article: https://turbo-engine-v69xvg5j7v973x475-3000.app.github.dev/articles/create
- Test Route: https://turbo-engine-v69xvg5j7v973x475-3000.app.github.dev/articles/test

## NEVER use these URLs (WITH :3000)
- ❌ https://turbo-engine-v69xvg5j7v973x475-3000.app.github.dev:3000/articles/
- ❌ https://turbo-engine-v69xvg5j7v973x475-3000.app.github.dev:3000/

## Why?
GitHub Codespaces automatically forwards port 3000 and includes it in the subdomain.
The port number is already in the URL as `-3000` before `.app.github.dev`.

## To start the app:
```bash
python app.py
```

Then use the URLs above WITHOUT :3000