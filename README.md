## Usage
Hook requires [docker container](https://hub.docker.com/r/fratajczak/autodoc/tags) to run.
If not present the attempt to download will be performed. Repository of a docker container is accessible with [repository](https://github.com/Tesla2000/Autodoc).

### Local
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
By default, models from ~/.cache/huggingface/hub are used. Location can be 
changed be specifying huggingface_home parameter. 
If the model isn't downloaded yet hook will attempt to download the model.
For some models exporting HUGGINGFACE_API_TOKEN may be required.
```shell
export HUGGINGFACE_API_TOKEN=...
```

### Remote
Or remote once provided OPENAI_API_KEY in 
```shell
export OPENAI_API_KEY=...
```
```
repos:
  - repo: https://github.com/Tesla2000/Autodoc-hook
    rev: '0.1.2'
    hooks:
      - id: autodoc
        stages: [push]
        args: [--llm, gpt-4o-mini, --api_keys=OPENAI_API_KEY]
```
