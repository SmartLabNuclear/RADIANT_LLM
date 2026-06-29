# User Skills

This folder contains example user-defined skills for `RADIANT-LLM`.

It is intended for two purposes:
- testing how `RADIANT-LLM` discovers, loads, and uses compatible custom skills
- showing the structure users can follow when creating their own `RADIANT-LLM`-compatible skills

The included examples are intentionally lightweight. They let users explore skill behavior with concrete, reusable examples, including playful cases such as the movie suggestion skill, while still following the skill layout expected by the system.

Current examples include:
- `MovieSuggester/` for trying a simple recommendation-oriented skill
- `DocumentComposer/` for exploring document-generation-oriented skill patterns
- `_template/` as a minimal starting point for building a new skill

If you want to build your own skill, use these folders as reference implementations and adapt the same general structure for your own workflow.

## License

This folder is part of [RADIANT_LLM](../) and is licensed under the [Apache License 2.0](../LICENSE).
