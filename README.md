What is this?: This is  a Python HTTPX Project aimed to test API Endpoints using "DummyJSON" site as base.

OBJECTIVE: Engineering goals include Client Model structure, Test reliability, separation of concerns, single responsibility approach and best practices. 

BASE: The project contains configuration modules, YAML config files, JSON credential files, pytest fixtures and more.

IMPORTANT NOTE: This project implements pre-commit checks.
Steps if proceeding to pull this  code:
- Create a Python Virtual Environment on your machine for the project (Keep it separated from the system core python environment)
- Activate the Virtual  Environment
- Use Pip install to install the provided packages in requirements.txt and requirements-dev.txt.
Example: pip install -r requirements.txt -r requirements-dev.txt
- Use pre-commit install to install the pre-commit flow. This will create a file in your .git/hooks. (One Time Only)
  This is required as these files need to be on your machine to adequately run the pre-commit flow, this is not inherited directly from the repository 

SCHEMA GENERATION (Development Aid): The Pydantic models in models/ are scaffolded with datamodel-code-generator (installed via requirements-dev.txt) and then completed by hand.

Generate from a live endpoint response:
- curl -s "https://dummyjson.com/products?limit=0" -o response.json
- datamodel-codegen --input response.json --input-file-type json --output-model-type pydantic_v2.BaseModel --snake-case-field --use-annotated --target-python-version 3.12 --class-name ProductListResponse --output generated.py

Flag notes:
- --snake-case-field converts camelCase JSON keys into snake_case fields and adds the matching alias.
- --use-annotated emits the Annotated[...] form, matching the style already used in models/.
- --input-file-type json infers everything from sample data. Use openapi or jsonschema instead whenever a spec is available, as those carry constraints that plain JSON does not.

FEED IT THE WIDEST SAMPLE AVAILABLE: limit=0 returns every record rather than one. The generator infers optionality only from what it sees. Given a single product it declares brand as required; given all 194 it correctly declares brand as optional, because 92 products omit the key entirely.

The generated file is a STARTING POINT, never the finished model. It gets field names, nesting and aliases right, which is the tedious and error-prone part. It cannot infer meaning, and sample JSON carries no constraints, so every field arrives as a bare type. Add the following by hand afterwards:
- Literal[...] for closed value sets, such as category and availability_status
- datetime rather than str for timestamps
- HttpUrl, or the project's URL_ANNOTATION, rather than str for links
- Field(...) bounds: gt, ge, le, min_length, max_length

Never overwrite an existing model with generated output. Regenerate into a scratch file and merge the differences, so hand-written validators and constraints are not lost.

STATUS: On Active Development

WHAT'S NEXT? Complete implementation
