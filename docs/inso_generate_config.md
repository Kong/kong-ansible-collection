# kong.kong.inso_generate_config


## Description

Generates a configuration from an API specification by using openapi-2-kong.

The command works similarly to generating a declarative configuration file or Kubernetes manifest from within Insomnia.


## Requirements

* [inso](https://docs.insomnia.rest/inso-cli/install)


## Parameters

| Parameter | Description |
| --- | --- |
| binary_path </br><sub><span style="color:purple">path</span></sub> | The path of a ‘inso’ CLI to use. |
| config </br><sub><span style="color:purple">path</span></sub> | Path to ‘inso’ configuration file. |
| format </br><sub><span style="color:purple">string</span></sub> | Output format. This option only applies to type `declarative`, and will be ignored for type `kubernetes`.</br>**Choices:**</br>- **<span style="color:blue">"yaml" ← (default)</span>**</br>- "json" |
| identifier </br><sub><span style="color:purple">string</span> / <span style="color:red">required</span></sub> | A specification name, or id, or a file path. |
| output </br><sub><span style="color:purple">path</span></sub> | Save the generated config to a file |
| src </br><sub><span style="color:purple">path</span></sub> | Sets the ‘inso’ app data source < file | dir > |
| tags </br><sub><span style="color:purple">list</span> / <span style="color:purple">elements=string</span></sub> | List of tags to apply to each entity |
| type </br><sub><span style="color:purple">string</span></sub> | Type of configuration to generate.</br>**Choices:**</br>- **<span style="color:blue">"declarative" ← (default)</span>**</br>- "kubernetes"|
| working_dir </br><sub><span style="color:purple">path</span></sub> | Sets the ‘inso’ working directory |


## Examples

```yaml
# Generate a KIC config
- name: "Generate Kong Ingress Controller config"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
    type: "kubernetes"
    output: "/tmp/kic.yaml"
    tags:
      - dev
      - v2alpha1

# Generate a decK config in yaml format
- name: "Generate Kong Gateway declarative config | yaml"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
    output: "/tmp/deck.yaml"

# Generate a decK config in json format
- name: "Generate Kong Gateway declarative config | json"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
    output: "/tmp/deck.json"
    format: "json"

# Generate a decK config with no output file, store the result, and copy it to the Ansible control node
- name: "Generate Kong Gateway declarative | no output"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
  register: "deck_config"

- name: "Copy the config to localhost"
  ansible.builtin.copy:
    content: "{{ deck_config.output.configuration }}"
    dest: "/tmp/deck.yaml"
  delegate_to: "localhost"

# Generate a decK config with no output file, store the result, and view the result
- name: "Generate Kong Gateway declarative | no output"
  kong.kong.inso_generate_config:
    identifier: "/path/to/my/oapi_spec.json"
  register: "deck_config_out"

- name: "View the result of inso_generate_config"
  ansible.builtin.debug:
    var: "deck_config_out"

- name: "Set the configuration to a variable for further manipulation"
  ansible.builtin.set_fact:
    deck_config: "deck_config_out.output.configuration | from_yaml"
```

## Return Values

| Key | Description |
| --- | --- |
|changed</br><sub><span style="color:purple">boolean</span></sub>|Whether the module made a change to the system</br>**Returned:** always|
|cmd</br><sub><span style="color:purple">list</span> / <span style="color:purple">elements=string</span></span></sub>|The ‘inso’ CLI command and arguments that were run.</br>**Returned:** always</br>**Sample:** <span style="color:blue">[“[\”/usr/local/bin/inso\””, ” \”generate\””, ” \”config\””, ” \”–ci\””, ” \”–printOptions\””, ” \”my identifier\”]”]</span>|
|failed</br><sub><span style="color:purple">boolean</span></sub>|Whether the module failed or not.</br>**Returned:** always|
|log</br><sub><span style="color:purple">complex</span></sub>|Dictionary containing log output from the ‘inso’ CLI run.</br>**Returned:** success|
|log.options</br><sub><span style="color:purple">string</span></sub>|The ‘inso’ CLI stdout log of options the command was run with.</br>**Returned:** success</br>**Sample:** <span style="color:blue">“[log] Loaded options { type: ‘declarative’, format: ‘yaml’, ci: true, printOptions: true }”</span>|
|log.output_path</br><sub><span style="color:purple">string</span></sub>|The ‘inso’ CLI stdout log of the path the generated Configuration was output to. If the ‘output’ parameter was not specificed, or run with check-mode, this will be marked as “stdout”.</br>**Returned:** success</br>**Sample:** <span style="color:blue">“[log] Configuration generated to \”/tmp/ansible_deck_output.yaml\””</span>|
|output</br><sub><span style="color:purple">complex</span></sub>|When the ‘output’ parameter is not specified, or run in check-mode, this will be populated with the raw configuration string from stdout as well as a list formatted version. The stored configuration data could then be used without writing to disk.</br>**Returned:** success|
|output.configuration</br><sub><span style="color:purple">string</span></sub>|Raw configuration string from stdout generated by the ‘inso’ CLI. This will only be returned if the module was run without the ‘output’ parameter or if the module was run in check-mode.</br>**Returned:** success|
|output.configuration_lines</br><sub><span style="color:purple">list</span></sub>|Configuration from stdout generated by the ‘inso’ CLI. This will only be returned if the module was run without the ‘output’ parameter or if the module was run in check-mode.</br>**Returned:** success|
|rc</br><sub><span style="color:purple">integer</span></sub>|Return code of the ‘inso’ CLI run.</br>**Returned:** always|
|stderr</br><sub><span style="color:purple">string</span></sub>|Raw standard error (stderr) output from the ‘inso’ CLI run.</br>**Returned:** always|
|stderr_lines</br><sub><span style="color:purple">list</span></sub>|Standard error output (stderr) from the ‘inso’ CLI run in list format.</br>**Returned:** always|
|stdout</br><sub><span style="color:purple">string</span></sub>|Raw standard output (stdout) from the ‘inso’ CLI run.</br>**Returned:** always|
|stdout_lines</br><sub><span style="color:purple">list</span></sub>|Standard output (stdout) from the ‘inso’ CLI run in list format.</br>**Returned:** always|


## Author

[Andrew J. Huffman](https://github.com/ahuffman)