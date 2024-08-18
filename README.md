## Usage
You can use autodoc to run 
```
repos:
  - repo: https://github.com/Tesla2000/Autodoc-hook
    rev: '0.1.2'
    hooks:
      - id: autodoc
        stages: [push]
        args: [--llm, google/gemma-2-2b-it, --api_keys, OPENAI_API_KEY]
```

