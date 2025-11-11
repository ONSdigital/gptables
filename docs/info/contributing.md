# Contributing

When contributing to this repository, please first discuss the change you wish
to make using [GitHub Issues](https://github.com/ONSdigital/gptables/issues). Alternatively,
get in touch with the Analysis Standards and Pipelines Team at the Office for National Statistics
via [email](mailto:ASAP@ons.gov.uk).

## Pull request process

1. Branch from the `dev` branch with a descriptive name, e.g. `feature-xyx`, `bug-xyz`, or by referencing an issue number.
1. Update relevant documentation:
    - Update Markdown (`.md`) files in the `docs/` folder if necessary.
    - Ensure function and class docstrings are clear and complete - documentation is generated from these using `mkdocs` and `mkdocstrings`.
    - Update the `README.md` file if needed.
1. Once you are ready for review please open a pull request to the
   `dev` branch.
    - Please fill in the template as much as possible so the changes are clear to a colleague without
   prior knowledge of the changes.
    - This will be merged by maintainers following their approval.

Thank you for contributing to `gptables`!

## Code style

- We name variables using few nouns in lowercase, e.g. `mapping_names`
  or `increment`.
- We name functions using verbs in lowercase, e.g. `map_variables_to_names` or
  `change_values`.
- We use the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html)
  format for documenting features using docstrings.
- Code formatting and linting are enforced via pre-commit hooks. Please install them by running `pre-commit install` in the root directory of the repository.

## Testing

- We use pytest for testing. All tests must pass.
- Please ensure that you have added tests for any new features or bug fixes, or raised an issue prompting the team to add this.
