import llm
import click
import os
from pathlib import Path
import toml
from importlib import resources

# Update these lines to use just the filename
DEFAULT_FEW_SHOT_PROMPT_FILE = "few_shot_prompt_llm_plugin_all.xml"
MODEL_FEW_SHOT_PROMPT_FILE = "few_shot_prompt_llm_plugin_model.xml"
UTILITY_FEW_SHOT_PROMPT_FILE = "few_shot_prompt_llm_plugin_utility.xml"

def read_few_shot_prompt(file_name):
    try:
        return resources.read_text("llm_plugin_generator", file_name)
    except FileNotFoundError:
        click.echo(f"Warning: Few-shot prompt file not found: {file_name}.")
        return ""


def write_main_python_file(content, output_dir, filename):
    main_file = output_dir / filename
    with main_file.open("w") as f:
        f.write(content)
    click.echo(f"Main Python file written to {main_file}")

def write_readme(content, output_dir):
    readme_file = output_dir / "README.md"
    with readme_file.open("w") as f:
        f.write(content)
    click.echo(f"README file written to {readme_file}")

def write_pyproject_toml(content, output_dir):
    pyproject_file = output_dir / "pyproject.toml"
    with pyproject_file.open("w") as f:
        f.write(content)
    click.echo(f"pyproject.toml file written to {pyproject_file}")

def extract_plugin_name(pyproject_content):
    try:
        pyproject_dict = toml.loads(pyproject_content)
        name = pyproject_dict['project']['name']
        # Convert kebab-case to snake_case
        return name.replace('-', '_')
    except:
        # If parsing fails, return a default name
        return "plugin"

@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("prompt", required=False)
    @click.argument("input_files", nargs=-1, type=click.Path(exists=True))
    @click.option("--output-dir", type=click.Path(), default=".", help="Directory to save generated plugin files")
    @click.option("--type", default="default", type=click.Choice(["default", "model", "utility"]), help="Type of plugin to generate")
    @click.option("--model", "-m", help="Model to use")
    def generate_plugin(prompt, input_files, output_dir, type, model):
        """Generate a new LLM plugin based on examples and a prompt or README file(s)."""
        # Select the appropriate few-shot prompt file based on the type
        if type == "model":
            few_shot_file = MODEL_FEW_SHOT_PROMPT_FILE
        elif type == "utility":
            few_shot_file = UTILITY_FEW_SHOT_PROMPT_FILE
        else:
            few_shot_file = DEFAULT_FEW_SHOT_PROMPT_FILE

        few_shot_prompt = read_few_shot_prompt(few_shot_file)
        
        input_content = ""
        for input_file in input_files:
            with open(input_file, "r") as f:
                input_content += f"""Content from {input_file}:
{f.read()}

"""
        if prompt:
            print(f"Prompt: {prompt}")
            input_content += f"""Additional prompt:
{prompt}
"""

        if not input_content:
            input_content = click.prompt("Enter your plugin description or requirements")
        
        llm_model = llm.get_model(model)
        response = llm_model.prompt(
            f"""Generate a new LLM plugin based on the following few-shot examples and the given input:
Few-shot examples:
{few_shot_prompt}

Input:
{input_content}

Generate the plugin code, including the main plugin file, README.md, and pyproject.toml. 
Ensure the generated plugin follows best practices and is fully functional. 
Provide the content for each file separately, enclosed in XML tags like <plugin_py>, <readme_md>, and <pyproject_toml>."""
        )
        
        generated_plugin = response.text()
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        plugin_py_content = extract_content(generated_plugin, "plugin_py")
        readme_content = extract_content(generated_plugin, "readme_md")
        pyproject_content = extract_content(generated_plugin, "pyproject_toml")
        
        # Extract the plugin name from pyproject.toml
        plugin_name = extract_plugin_name(pyproject_content)
        
        # Use the extracted name for the main Python file
        write_main_python_file(plugin_py_content, output_path, f"{plugin_name}.py")
        write_readme(readme_content, output_path)
        write_pyproject_toml(pyproject_content, output_path)
        
        click.echo("Plugin generation completed.")

def extract_content(text, tag):
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    start = text.find(start_tag) + len(start_tag)
    end = text.find(end_tag)
    return text[start:end].strip()

@llm.hookimpl
def register_models(register):
    pass  # No custom models to register for this plugin

@llm.hookimpl
def register_prompts(register):
    pass  # No custom prompts to register for this plugin
