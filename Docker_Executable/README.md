# Docker Executable

Docker Compose templates for running RADIANT-LLM from [zev94/radiant-llm](https://hub.docker.com/r/zev94/radiant-llm) on your machine.

## Quick start

1. Copy [`.env.example`](.env.example) to `.env` and add your API keys.
2. Edit volume paths in [`docker-compose.yml`](docker-compose.yml) to match your machine.
3. From this folder, run:

```bash
docker compose up -d
```

4. Open http://localhost:8060

For full setup options (Grace vLLM tunnels, `visual-parser`, evaluation data), see the main [README.md](../README.md).

## License

This folder is part of [RADIANT_LLM](../) and is licensed under the [Apache License 2.0](../LICENSE).
