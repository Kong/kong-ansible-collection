# kong.kong.common.k4k8s_helm

<p align="center">
  <img src="https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2018/08/kong-combination-mark-color-256px.png" /></div>
</p>


## Description

An Ansible role to install Helm chart repositories and Helm charts via roles within the `kong.kong` Ansible collection.  This is not intended to be directly included in a playbook since it's a library for the Kong collection, but if you'd like to, you can reference it by `kong.kong.common.k4k8s_helm`.  If referencing the role from within a collection role, it can be referenced as `common/k4k8s_helm`.


## Table of Contents


<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=truee} -->

<!-- code_chunk_output -->

1. [Description](#description)
2. [Table of Contents](#table-of-contents)
3. [Dependencies](#dependencies)
    1. [Python dependencies](#python-dependencies)
    2. [Ansible collection dependencies](#ansible-collection-dependencies)
    3. [Binary dependencies](#binary-dependencies)
4. [Default variables](#default-variables)
    1. [Role behavior variables](#role-behavior-variables)
    2. [Kubernetes and Red Hat Open Shift variables](#kubernetes-and-red-hat-open-shift-variables)
    3. [Helm deployment method variables](#helm-deployment-method-variables)
5. [Advanced variables](#advanced-variables)
    1. [Helm](#helm)
    2. [Collected result variables](#collected-result-variables)
6. [Role usage examples](#role-usage-examples)
7. [License](#license)
8. [Author](#author)

<!-- /code_chunk_output -->


## Dependencies


### Python dependencies

See [requirements.txt](requirements.txt)

Pre-install Python module dependencies with:

```bash
pip3 install -r requirements.txt
```


### Ansible collection dependencies

See [galaxy-requirements.yml](galaxy-requirements.yml)

Pre-install Ansible Galaxy Collection requirements with:

```bash
ansible-galaxy install -r galaxy-requirements.yml
```


### Binary dependencies

1. [Helm3](https://helm.sh/docs/intro/install/) `helm` is required on the target Ansible host (`{{ inventory_hostname }}`) in `$PATH`.

---
**[Table of Contents](#table-of-contents)**


## Default variables

The following tables outline variables available in [defaults/main.yml](defaults/main.yml) and are used to control the behavior of the `common/k4k8s_helm` Ansible role.  They are presented based on how they affect the overall operation of the role's automation.


### Role behavior variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_helm_component_name`|Used for templating several Ansible task names to denote the Helm chart component we are installing during a kong.kong Ansible role playbook run.|string|`""`|no|


### Kubernetes and Red Hat Open Shift variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_helm_release_namespace`|The Kubernetes `namespace` or Red Hat OpenShift `project` to deploy a Helm chart to|string|`""`|yes|
|`k4k8s_kubeconfig`|The path to your Kubernetes (`kubectl`) or Red Hat OpenShift CLI (`oc`) configuration file. This may be useful when working with multiple clusters.|string|`None` (unset)|no|
|`k4k8s_cluster_context`|The context to use for operating on a Kubernetes or Red Hat OpenShift cluster.  If not specified, the current context set in your `k4k8s_kubeconfig` will be used.  This may be useful when working with multiple clusters.|string|`None` (unset)|no|


### Helm values variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_helm_chart_values_files`|Array/list of Helm values files to apply to the Helm chart.  If combining with `k4k8s_helm_chart_values`, these will be applied first and can be overridden by values in your `k4k8s_helm_chart_values`. The order of your list is the order the values will be applied in, much like providing the `-f` option multiple times with Helm.|list (array)|`[]`|no|
|`k4k8s_helm_chart_values_remote`|Whether or not the `k4k8s_helm_chart_values_files` should be read from the `{{ inventory_hostname }}` or Ansible control node. Set to `true` when the Helm values files are on the `{{ inventory_hostname }}`.|boolean|`false`|no|
|`k4k8s_helm_chart_values`|Dictionary of Helm values to apply to the Helm chart.  Can be used with `k4k8s_helm_chart_values_files`, or alone. If combining with `k4k8s_helm_chart_values_files` these values will be applied last and can override values in your `k4k8s_helm_chart_values_files` via **recursive dictionary merges** and any lists are replaced with the new value. This is a great way to override a single value or a few.  See Ansible's [combine filter documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-hashes-dictionaries) for more clarity on this merge methodology.|dictionary|`{}`|no|

**[Table of Contents](#table-of-contents)**

---


## Advanced variables


### Helm

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_helm_atomic`|Equivalent to the `helm` `--atomic` option.|boolean|`False`|no|
|`k4k8s_helm_binary_path`|Path to the `helm` executable.|string|`"helm"`|no|
|`k4k8s_helm_chart_ref`|The Helm chart name to use to deploy to Kubernetes or Red Hat OpenShift clusters.|string|`""`|yes|
|`k4k8s_helm_chart_repo_name`|Name to install the Helm chart repository as.|string|`""`|yes|
|`k4k8s_helm_chart_repo_url`|URL for the helm chart repository.|string|`""`|yes|
|`k4k8s_helm_chart_repo_username`|Username for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_helm_chart_repo_password`|Password for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_helm_chart_version`|Use if you need a particular Helm Chart version, otherwise the latest chart available will be used.|string|`None` (omitted)|no|
|`k4k8s_helm_disable_hook`|Corresponds to the `helm` `--no-hooks` option.|boolean|`False`|no|
|`k4k8s_helm_force_reinstall`|Helm option to force reinstall, ignore on new install.|boolean|`False`|no|
|`k4k8s_helm_release_name`|Name of the helm release.|string|`""`|yes|
|`k4k8s_helm_replace`|Corresponds to the `helm` `--replace` option.|boolean|`False`|no|
|`k4k8s_helm_update_repo`|Whether or not to update the helm chart repository prior to deployment.  This ensures the latest chart is available.  If a specific chart version is required, set the `k4k8s_helm_chart_version`|boolean|`True`|no|
|`k4k8s_helm_wait`|Whether or not to wait for the Helm Chart's objects to be successfully deployed and at desired state.|boolean|`True`|no|

**[Table of Contents](#table-of-contents)**

---


### Collected result variables

The following variables are useful when debugging.

| Variable name | Description |
| --- | --- |
|`__k4k8s_helm_results__`|The results collected when applying the Helm chart|
|`__k4k8s_helm_release_values__`|The combined values from your helm values files and helm values.  This is what gets applied during Helm chart deployment.  Good way to validate your chart values are being read as you expect them to. |

**[Table of Contents](#table-of-contents)**

---


## Role usage examples

```yaml
...
# called from within a collection role's tasks
- name: "Ensure kong for kubernetes is present | helm"
  ansible.builtin.include_role:
    name: "common/k4k8s_helm"
    public: true
  vars:
    k4k8s_helm_atomic: "{{ k4k8s_deploy_helm_atomic }}"
    k4k8s_helm_binary_path: "{{ k4k8s_deploy_helm_binary_path }}"
    k4k8s_helm_chart_values: "{{ k4k8s_deploy_helm_chart_values }}"
    k4k8s_helm_chart_values_files: "{{ k4k8s_deploy_helm_chart_values_files }}"
    k4k8s_helm_chart_values_remote: "{{ k4k8s_deploy_helm_chart_values_remote }}"
    k4k8s_helm_chart_version: "{{ k4k8s_deploy_helm_chart_version | default(None) }}"
    k4k8s_helm_chart_ref: "{{ k4k8s_deploy_helm_chart_ref }}"
    k4k8s_helm_chart_repo_name: "{{ k4k8s_deploy_helm_chart_repo_name }}"
    k4k8s_helm_chart_repo_password: "{{ k4k8s_deploy_helm_chart_repo_password | default(None) }}"
    k4k8s_helm_chart_repo_url: "{{ k4k8s_deploy_helm_chart_repo_url }}"
    k4k8s_helm_chart_repo_username: "{{ k4k8s_deploy_helm_chart_repo_username | default(None) }}"
    k4k8s_helm_component_name: "kong for kubernetes"
    k4k8s_helm_disable_hook: "{{ k4k8s_deploy_helm_disable_hook }}"
    k4k8s_helm_force_reinstall: "{{ k4k8s_deploy_helm_force_reinstall }}"
    k4k8s_helm_release_name: "{{ k4k8s_deploy_helm_release_name }}"
    k4k8s_helm_release_namespace: "{{ k4k8s_deploy_namespace }}"
    k4k8s_helm_replace: "{{ k4k8s_deploy_helm_replace }}"
    k4k8s_helm_update_repo: "{{ k4k8s_deploy_helm_update_repo }}"
    k4k8s_helm_wait: "{{ k4k8s_deploy_helm_wait }}"

- name: "Set collected helm run facts"
  ansible.builtin.set_fact:
    __k4k8s_deploy_helm_results__: "{{ __k4k8s_helm_results__ }}"
    __k4k8s_deploy_helm_release_values__: "{{ __k4k8s_helm_release_values__ }}"

...
```

**[Table of Contents](#table-of-contents)**

---


## License

[Apache 2.0](../../../LICENSE)

---


## Author

[Andrew J. Huffman](https://github.com/ahuffman)

---
**[Table of Contents](#table-of-contents)**
