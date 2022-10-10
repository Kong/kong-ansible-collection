# kong.kong.inso_lint_spec


## Description

The `inso_lint_spec` module lints and validates your OpenAPI specification with the 'inso' CLI.  Lint results will be returned in the module's results.  Inso CLI will exit with a non-zero exit code if linting fails, and the module run will fail.


## Requirements

* [inso](https://docs.insomnia.rest/inso-cli/install)


## Parameters

| Parameter | Description |
| --- | --- |
| binary_path </br><sub><span style="color:purple">path</span></sub> | The path of a ‘inso’ CLI to use. |
| config </br><sub><span style="color:purple">path</span></sub> | Path to ‘inso’ configuration file. |
| identifier </br><sub><span style="color:purple">string</span> / <span style="color:red">required</span></sub> | A specification name, or id, or a file path. |
| src </br><sub><span style="color:purple">path</span></sub> | Sets the ‘inso’ app data source < file | dir > |
| working_dir </br><sub><span style="color:purple">path</span></sub> | Sets the ‘inso’ working directory |


## Examples

```yaml
# Lint an OpenAPI specification
- name: "Lint OpenAPI specification"
  kong.kong.inso_lint_spec:
    identifier: "/path/to/my/oapi_spec.json"

# Lint OpenAPI specification and register results
- name: "Lint OpenAPI specification and register results"
  kong.kong.inso_lint_spec:
    identifier: "/path/to/my/oapi_spec.json"
  register: "openapi_lint_results"

- name: "View the OpenAPI linting results"
  ansible.builtin.debug:
    var: "openapi_lint_results"
```

## Return Values

| Key | Description |
| --- | --- |
|changed</br><sub><span style="color:purple">boolean</span></sub>|Whether the module made a change to the system, this will always return 'False'.</br>**Returned:** always|
|cmd</br><sub><span style="color:purple">list</span> / <span style="color:purple">elements=string</span></span></sub>|The ‘inso’ CLI command and arguments that were run.</br>**Returned:** always</br>**Sample:** <span style="color:blue">[“[\”/usr/local/bin/inso\””, ”\"lint\””, ” \”spec\””, ” \”–ci\””, ” \”–printOptions\””, ” \”my identifier\”]”]</span>|
|failed</br><sub><span style="color:purple">boolean</span></sub>|Whether the module failed or not.</br>**Returned:** always|
|log</br><sub><span style="color:purple">complex</span></sub>|Dictionary containing log output from the ‘inso’ CLI run.</br>**Returned:** success|
|log.options</br><sub><span style="color:purple">string</span></sub>|The ‘inso’ CLI stdout log of options the command was run with.</br>**Returned:** success</br>**Sample:** <span style="color:blue">“[log] Loaded options { ci: true, printOptions: true }”</span>|
|log.results</br><sub><span style="color:purple">string</span></sub>|The 'inso' CLI stdout log of the lint operation.  If the lint operation fails, the problems in the OpenAPI specification will be reported.</br>**Returned:** always|
|rc</br><sub><span style="color:purple">integer</span></sub>|Return code of the ‘inso’ CLI run.</br>**Returned:** always|
|stderr</br><sub><span style="color:purple">string</span></sub>|Raw standard error (stderr) output from the ‘inso’ CLI run.</br>**Returned:** always|
|stderr_lines</br><sub><span style="color:purple">list</span></sub>|Standard error output (stderr) from the ‘inso’ CLI run in list format.</br>**Returned:** always|
|stdout</br><sub><span style="color:purple">string</span></sub>|Raw standard output (stdout) from the ‘inso’ CLI run.</br>**Returned:** always|
|stdout_lines</br><sub><span style="color:purple">list</span></sub>|Standard output (stdout) from the ‘inso’ CLI run in list format.</br>**Returned:** always|


## Author

[Andrew J. Huffman](https://github.com/ahuffman)