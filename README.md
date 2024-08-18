## Usage
You can use autodoc to run local models
```
repos:
  - repo: https://github.com/Tesla2000/Autodoc-hook
    rev: '0.1.2'
    hooks:
      - id: autodoc
        stages: [push]
        args: [--llm, google/gemma-2-2b-it]
```
Or remote once provided OPENAI_API_KEY in 
```shell
export OPENAI_API_KEY="..."
```
```
repos:
  - repo: https://github.com/Tesla2000/Autodoc-hook
    rev: '0.1.2'
    hooks:
      - id: autodoc
        stages: [push]
        args: [--llm, gpt-4o-mini, --api_keys, OPENAI_API_KEY]
```
