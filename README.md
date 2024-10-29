# llm-plugin-generator

[![PyPI](https://img.shields.io/pypi/v/llm-plugin-generator.svg)](https://pypi.org/project/llm-plugin-generator/)
[![Changelog](https://img.shields.io/github/v/release/irthomasthomas/llm-plugin-generator?include_prereleases&label=changelog)](https://github.com/irthomasthomas/llm-plugin-generator/releases)
[![Tests](https://github.com/irthomasthomas/llm-plugin-generator/workflows/Test/badge.svg)](https://github.com/irthomasthomas/llm-plugin-generator/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/irthomasthomas/llm-plugin-generator/blob/main/LICENSE)

LLM plugin to generate few-shot prompts for plugin creation

## Installation

Install this plugin in the same environment as LLM:

```bash
llm install llm-plugin-generator
```

## Usage

To generate a new LLM plugin, use the `generate-plugin` command:

```bash
llm generate-plugin "Description of your plugin"
```

Options:

- `PROMPT`: Description of your plugin (optional)
- `INPUT_FILES`: Path(s) to input README or prompt file(s) (optional, multiple allowed)
- `--output-dir`: Directory to save generated plugin files (default: current directory)
- `--type`: Type of plugin to generate (default, model, or utility)
- `--model`, `-m`: Model to use for generation
- `--reasoning`: Reasoning level for the AI (1-9)

Examples:

1. Basic usage:
```bash
llm generate-plugin "Create a plugin that translates text to emoji" --output-dir ./my-new-plugin --type utility --model gpt-4
```

2. Using input files and specifying reasoning level:
```bash
llm generate-plugin "LLM plugin generator plugin." /home/ShellLM/Projects/claude.sh/llm_plugin_generator/llm_plugin_generator/pyproject.toml /home/ShellLM/Projects/claude.sh/llm_plugin_generator/llm_plugin_generator/llm_plugin_generator.py --output-dir new-plugin-generator --type utility -m claude-3.5-sonnet
```

This will generate a new LLM plugin based on the provided description and/or input files, including the main plugin file, README.md, and pyproject.toml. The files will be saved in the specified output directory.

## Features

- Generates fully functional LLM plugins based on descriptions or input files
- Supports different plugin types: default, model, and utility
- Uses few-shot learning with predefined examples for better generation
- Allows specifying custom output directory
- Compatible with various LLM models
- Generates main plugin file, README.md, and pyproject.toml
- Extracts plugin name from generated pyproject.toml for consistent naming

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-plugin-generator
python -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
pytest
```

## Contributing

Contributions to llm-plugin-generator are welcome! Please refer to the [GitHub repository](https://github.com/irthomasthomas/llm-plugin-generator) for more information on how to contribute.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
