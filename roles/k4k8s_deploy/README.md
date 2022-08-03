# kong.kong.k4k8s_deploy

[![k4k8s-deploy](https://github.com/Kong/kong-ansible-collection/actions/workflows/k4k8s-deploy-ci.yml/badge.svg)](https://github.com/Kong/kong-ansible-collection/actions/workflows/k4k8s-deploy-ci.yml)

<p align="center">
  <img src="https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2018/08/kong-combination-mark-color-256px.png" /></div>
</p>


## Description

An Ansible role to deploy Kong for Kubernetes, Kong for Kubernetes Enterprise, Kong for Kubernetes with Kong Enterprise, and Kong Kubernetes Ingress Controller to Kubernetes or Red Hat OpenShift clusters.  Product specific documentation can be found within the Kong Kubernetes Ingress Controller documentation pages [here](https://docs.konghq.com/kubernetes-ingress-controller/).

The Ansible role can currently perform a Helm based or Kubernetes YAML manifest based installation, along with full automation of Kong required secrets for production grade installations.  The role can also take care of installing and verifying the installation of Python module dependencies, Ansible Galaxy Collection dependencies, and binary dependencies if desired (configurable).


## Table of Contents

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=true} -->

<!-- code_chunk_output -->

1. [Description](#description)
2. [Table of Contents](#table-of-contents)
3. [Dependencies](#dependencies)
    1. [Python dependencies](#python-dependencies)
    2. [Ansible collection dependencies](#ansible-collection-dependencies)
    3. [Binary dependencies](#binary-dependencies)
4. [Testing and Supported Platforms](#testing-and-supported-platforms)
5. [Default variables](#default-variables)
    1. [Role behavior variables](#role-behavior-variables)
    2. [Helm deployment method variables](#helm-deployment-method-variables)
    3. [YAML manifest deployment method variables](#yaml-manifest-deployment-method-variables)
    4. [Kong deployment variables](#kong-deployment-variables)
    5. [Kubernetes and Red Hat OpenShift variables](#kubernetes-and-red-hat-openshift-variables)
6. [Advanced variables](#advanced-variables)
    1. [Helm](#helm)
    2. [Collected result variables and other set facts or variables](#collected-result-variables-and-other-set-facts-or-variables)
7. [Playbook usage examples](#playbook-usage-examples)
    1. [Sample Helm values files](#sample-helm-values-files)
8. [License](#license)
9. [Author](#author)

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

1. When using `k4k8s_deploy_method: "helm"` (default value) [Helm3](https://helm.sh/docs/intro/install/) `helm` is required on the target Ansible host (`{{ inventory_hostname }}`) in `$PATH`.
1. When using `k4k8s_deploy_create_hybrid_mode_cp_cert_secret: true` to generate control-plane hybrid-mode shared private-key/certificate pair secrets, [OpenSSL](https://wiki.openssl.org/index.php/Binaries) `openssl` or `openssl3` (on CentOS8/RedHat8) is required on the target Ansible host (`{{ inventory_hostname }}`) in `$PATH`.


**[Table of Contents](#table-of-contents)**

---


## Testing and Supported Platforms

This Ansible role was validated to function using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html) and [this](../../.github/workflows/k4k8s-deploy-ci.yml) GitHub Actions workflow.

The testing targets the latest version of Kubernetes available from [`microk8s`](https://microk8s.io/) a fully compliant and lightweight Kubernetes distribution and Red Hat OpenShift using the [`microshift-aio:latest`](https://microshift.io/) container image.

The testing matrix is validated against the following `ansible-test` containers as target hosts and launched from the default `ansible-test` container:

|Test Container|Python Version|
|---|---|
|default|3.10|
|centos8|3.6|
|ubuntu1804|3.6|
|ubuntu2004|3.8|
|opensuse15|3.6|

**[Table of Contents](#table-of-contents)**

---


## Default variables

The following tables outline variables available in [defaults/main.yml](defaults/main.yml) and are used to control the behavior of the `kong.kong.k4k8s-deploy` Ansible role.  They are presented based on how they affect the overall operation of the role's automation.


### Role behavior variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_method`|The method used to deploy Kong for Kubernetes, Kong for Kubernetes Enterprise, Kong for Kubernetes with Kong Enterprise, and Kong Kubernetes Ingress Controller to Kubernetes or Red Hat OpenShift clusters.  Options available in `kong.kong.k4k8s-deploy release 0.0.1` are `helm` or `yaml_manifest`.|string|`"helm"`|yes|

**[Table of Contents](#table-of-contents)**

---


### Helm deployment method variables

The following variables apply only when `k4k8s_deploy_method: "helm"` is set (default).

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_helm_chart_values_files`|Array/list of Helm values files to apply to the [Kong Helm charts](https://github.com/Kong/charts).  If combining with `k4k8s_deploy_helm_chart_values`, these will be applied first and can be overridden by values in your `k4k8s_deploy_helm_chart_values`. The order of your list is the order the values will be applied in, much like providing the `-f` option multiple times with Helm.|list (array)|`[]`|no|
|`k4k8s_deploy_helm_chart_values_remote`|Whether or not the `k4k8s_deploy_helm_chart_values_files` should be read from the `{{ inventory_hostname }}` or Ansible control node. Set to `true` when the Helm values files are on the `{{ inventory_hostname }}`.|boolean|`false`|no|
|`k4k8s_deploy_helm_chart_values`|Dictionary of Helm values to apply to the [Kong Helm charts](https://github.com/Kong/charts).  Can be used with `k4k8s_deploy_helm_chart_values_files`, or alone. If combining with `k4k8s_deploy_helm_chart_values_files` these values will be applied last and can override values in your `k4k8s_deploy_helm_chart_values_files` via **recursive dictionary merges** and any lists are replaced with the new value. This is a great way to override a single value or a few.  See Ansible's [combine filter documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-hashes-dictionaries) for more clarity on this merge methodology.|dictionary|`{}`|no|

**[Table of Contents](#table-of-contents)**

---


### YAML manifest deployment method variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_yaml_manifest_paths`|Array/list of your Kong YAML manifests for Kubernetes or Red Hat OpenShift.  The order they are listed out is the order in which they will be applied to your cluster. If `k4k8s_deploy_yaml_manifest_paths_remote` is set to `True`, then these must be fully-qualified paths, otherwise relative pathing from the playbook location should work.|list (array)|[]|no|
|`k4k8s_deploy_yaml_manifest_paths_remote`|Whether or not your YAML manifests listed in `k4k8s_deploy_yaml_manifest_paths` are on the Ansible control node or on the `{{ inventory_hostname }}`.|boolean|False|no|

**[Table of Contents](#table-of-contents)**

---


### Kong deployment variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_create_enterprise_license_secret`|Whether or not to create the Kong Enterprise license secret.  This uses the `k4k8s_deploy_enterprise_license_json_string` variable, along with `k4k8s_deploy_enterprise_license_secret_key` and `k4k8s_deploy_enterprise_license_secret_name` to generate the Kubernetes or Red Hat OpenShift secret object.|boolean|`False`|yes|
|`k4k8s_deploy_enterprise_license_secret_name`|The name of the Kubernetes or Red Hat OpenShift Kong Enterprise license secret object to be created. This is should match how you have your Helm values or YAML manifests configured.|string|"kong-enterprise-license"|no|
|`k4k8s_deploy_enterprise_license_secret_key`|The name of the key within the Kubernetes or Red Hat OpenShift secret object. This is should match how you have your Helm values or YAML manifests configured.|string|`"license"`|no|
|`k4k8s_deploy_enterprise_license_json_string`|The contents of your Kong Enterprise license.json file.  **NOTE:** It is *highly recommended* to store this value within an ansible-vault and pass it to your playbook, or by using some other secure mechanism.|string|`''`|no|
|`k4k8s_deploy_create_enterprise_superuser_password_secret`|Whether or not to create an initial Kong Superuser (Admin user) Kubernetes or Red Hat OpenShift secret for use with basic-auth.|boolean|`False`|yes|
|`k4k8s_deploy_enterprise_superuser_password_secret_name`|The name of the initial Kong Superuser (Admin user) Kubernetes or Red Hat OpenShift secret to be created. This is should match how you have your Helm values or YAML manifests configured.|string|`"kong-enterprise-superuser-password"`|no|
|`k4k8s_deploy_enterprise_superuser_password`|The password that will be used to generate the initial Kong Enterprise superuser password.|string|`"cloudnative"` This should be changed.|no|
|`k4k8s_deploy_create_hybrid_mode_cp_cert_secret`|Whether or not to create a SSL certificate secret for Kubernetes or Red Hat OpenShift for a Kong Enterprise Hybrid-mode (separated control plane and data plane) configuration to secure communications.  You may want to use an external method that meets your security standards prior to running this role to handle this in a production grade deployment.  This is mutually exclusive with `k4k8s_deploy_create_hybrid_mode_dp_cert_secret`, and uses `k4k8s_deploy_hybrid_mode_cert_secret_name`, `k4k8s_deploy_hybrid_mode_cert_cert_key`, `k4k8s_deploy_hybrid_mode_cert_key_key`, `k4k8s_deploy_hybrid_mode_cert_expiration`, and `k4k8s_deploy_hybrid_mode_cert_common_name` to create the secret. This is a [shared mode](https://docs.konghq.com/gateway/latest/plan-and-deploy/hybrid-mode/hybrid-mode-setup/#generate-a-certificatekey-pair)  certificate/key pair.|boolean|`False`|yes|
|`k4k8s_deploy_hybrid_mode_cert_secret_name`|The name of the Kong Enterprise Hybrid-mode certificate/key pair secret to create on a Kubernetes or Red Hat OpenShift cluster.|string|`"kong-cluster-cert"`|no|
|`k4k8s_deploy_hybrid_mode_cert_cert_key`|The name of the key within the `k4k8s_deploy_hybrid_mode_cert_secret_name` secret used to store the x509 certificate.|string|`"cert"`|no|
|`k4k8s_deploy_hybrid_mode_cert_key_key`|The name of the key within the `k4k8s_deploy_hybrid_mode_cert_secret_name` secret used to store the openssl private key.|string|`"key"`|no|
|`k4k8s_deploy_hybrid_mode_cert_expiration`|Number of days for the self-signed hybrid-mode Kong Enterprise certificate to expire in.|integer|`1095`|no|
|`k4k8s_deploy_hybrid_mode_cert_common_name`|Common name (CN) to use in the self-signed hybrid-mode Kong Enterprise certificate.|string|`kong_clustering`|no|
|`k4k8s_deploy_create_hybrid_mode_dp_cert_secret`|Whether or not to create the hybrid-mode certificate when deploying a Kong Enterprise dataplane.  This is mutually exclusive with `k4k8s_deploy_create_hybrid_mode_cp_cert_secret`.  This uses `k4k8s_deploy_hybrid_mode_cert_secret_name`, `k4k8s_deploy_hybrid_mode_cert_cert_key`, and `k4k8s_deploy_hybrid_mode_cert_key_key` to create the secret. Additionally, you will need to set the `k4k8s_deploy_hybrid_mode_certificate_harvest_context` and/or `k4k8s_deploy_hybrid_mode_certificate_harvest_kubeconfig` to retrieve/harvest the secret from a control-plane cluster.|boolean|`False`|no|
|`k4k8s_deploy_hybrid_mode_certificate_harvest_context`|The kubernetes or Red Hat OpenShift kubeconfig context to use to 'harvest' the `k4k8s_deploy_hybrid_mode_cert_secret_name` secret from the Kong Enterprise control-plane when creating the data-plane's secret.|string|`None` (unset)|no|
|`k4k8s_deploy_hybrid_mode_certificate_harvest_kubeconfig`|The kubernetes or Red Hat OpenShift kubeconfig to use to 'harvest' the `k4k8s_deploy_hybrid_mode_cert_secret_name` secret from the Kong Enterprise control-plane when creating the data-plane's secret.|string|`None`|no|
|`k4k8s_deploy_hybrid_mode_cert_harvest_namespace`|The Kubernetes or Red Hat OpenShift namespace to harvest the hybrid-mode secret from.|string|`"kong"`|no|
|`k4k8s_deploy_create_postgres_password_secret`|Whether or not to create a secret containing your Kong Enterprise control plane database postgresql password. | boolean|`False`|no|
|`k4k8s_deploy_postgres_password_secret_name`|The name of the postresql password secret to create|string|`"kong"`|no|
|`k4k8s_deploy_postgres_admin_password_secret_key`|The name of the admin password key within the Kubernetes or Red Hat OpenShift `k4k8s_deploy_postgres_password_secret_name` secret object. This key should match your Helm values or YAML manifests configured secret reference.|string|`"postgres-password"`|no|
|`k4k8s_deploy_postgres_user_password_secret_key`|The name of the user password postrgres key within the Kubernetes or Red Hat OpenShift `k4k8s_deploy_postgres_password_secret_name` secret object. This should match your Helm values or YAML manifests configured secret reference.|string|`"password"`|no|
|`k4k8s_deploy_postgres_admin_password`|The password for your Kong Enterprise postgresql database administrator user.|string|"kong"|no|
|`k4k8s_deploy_postgres_user_password`|The password for your Kong Enterprise postgresql database user.|string|"kong"|no|
|`k4k8s_deploy_create_admin_gui_sessions_conf_secret`|Whether or not to create a [admin GUI sessions](https://docs.konghq.com/gateway/latest/configure/auth/kong-manager/sessions/) configuration.  This uses the `k4k8s_deploy_sessions_conf_secret_name`, `k4k8s_deploy_admin_gui_sessions_conf_key`, and `k4k8s_deploy_admin_gui_sessions_settings` variables to construct the secret and configuration.|boolean|`False`|no|
|`k4k8s_deploy_sessions_conf_secret_name`|The name of the Kubernetes or Red Hat OpenShift admin GUI sessions configuration secret to create.|string|`"admin_gui_session_conf"`|no|
|`k4k8s_deploy_admin_gui_sessions_conf_key`|The name of the key within the Kubernetes or Red Hat OpenShift `k4k8s_deploy_admin_gui_sessions_conf_secret_name` secret object. This is should match how you have your Helm values or YAML manifests configured.|||||
|`k4k8s_deploy_admin_gui_sessions_settings`|Dictionary containing the [admin GUI sessions](https://docs.konghq.com/gateway/latest/configure/auth/kong-manager/sessions/) configuration options to be applied.|dictionary|see values in [defaults/main.yml](defaults/main.yml)|no|
|`k4k8s_deploy_admin_gui_sessions_settings.cookie_domain`|Use when serving the Kong Manager on a separate subdomain.  Set a subdomain such as an example `".xyz.com"` and set `cookie_samesite` to `"off"`.|string|`None` (unset)|no|
|`k4k8s_deploy_admin_gui_sessions_settings.cookie_lifetime`|The duration (in seconds) that the session will remain open.|integer|`3600`|no|
|`k4k8s_deploy_admin_gui_sessions_settings.cookie_name`|The name of the cookie.|string|"please-change-me"|yes|
|`k4k8s_deploy_admin_gui_sessions_settings.cookie_renew`|The duration (in seconds) of a session remaining at which point the Plugin renews the session.|integer|'600'|no|
|`k4k8s_deploy_admin_gui_sessions_settings.cookie_samesite`|If using different domains for the Admin API and Kong Manager, set to `"off"`.|string|`"Strict"`|no|
|`k4k8s_deploy_admin_gui_sessions_settings.cookie_secure`|Set to `true` when using HTTPS instead of HTTP for Kong Manager.|boolean|`false`|no|
|`k4k8s_deploy_admin_gui_sessions_settings.secret`|The secret used in keyed HMAC generation. Although the **Session Plugin's** default is a random string, the secret *must* be manually set for use with Kong Manager since it must be the same across all Kong workers/nodes.|string|`please-change-me`|yes|
|`k4k8s_deploy_admin_gui_sessions_settings.storage`| Where session data is stored. It is `"cookie"` by default, but may be more secure if set to `"kong"` since access to the database would be required.|string|`"cookie"`|no|
|`k4k8s_deploy_create_portal_sessions_conf_secret`|Whether or not to create a [Dev Portal Sessions](https://docs.konghq.com/gateway/latest/developer-portal/configuration/authentication/sessions/) configuration.  This uses the `k4k8s_deploy_sessions_conf_secret_name`, `k4k8s_deploy_portal_sessions_conf_key`, and `k4k8s_deploy_portal_sessions_settings` variables to construct the secret and configuration.|boolean|`False`|no|
|`k4k8s_deploy_portal_sessions_conf_key`|The name of the key within the Kubernetes or Red Hat OpenShift `k4k8s_deploy_portal_sessions_conf_secret_name` secret object. This is should match how you have your Helm values or YAML manifests configured.|||||
|`k4k8s_deploy_portal_sessions_settings`|Dictionary containing the [Dev Portal Sessions](https://docs.konghq.com/gateway/latest/developer-portal/configuration/authentication/sessions/) configuration options to be applied.|dictionary|see values in [defaults/main.yml](defaults/main.yml)|no|
|`k4k8s_deploy_portal_sessions_settings.cookie_domain`|Use when serving the Dev Portal on a separate subdomain.  Set a subdomain such as an example `".xyz.com"` and set `cookie_samesite` to `"off"`.|string|`None` (unset)|no|
|`k4k8s_deploy_portal_sessions_settings.cookie_lifetime`|The duration (in seconds) that the session will remain open.|integer|`3600`|no|
|`k4k8s_deploy_portal_sessions_settings.cookie_name`|The name of the cookie.|string|"please-change-me"|yes|
|`k4k8s_deploy_portal_sessions_settings.cookie_renew`|The duration (in seconds) of a session remaining at which point the Plugin renews the session.|integer|'600'|no|
|`k4k8s_deploy_portal_sessions_settings.cookie_samesite`|If using different domains for the Admin API and Kong Manager, set to `"off"`.|string|`"Strict"`|no|
|`k4k8s_deploy_portal_sessions_settings.cookie_secure`|Set to `true` when using HTTPS instead of HTTP for Kong Manager.|boolean|`false`|no|
|`k4k8s_deploy_portal_sessions_settings.secret`|The secret used in keyed HMAC generation. Although the **Session Plugin's** default is a random string, the secret *must* be manually set for use with Kong Manager since it must be the same across all Kong workers/nodes.|string|`please-change-me`|yes|
|`k4k8s_deploy_portal_sessions_settings.storage`| Where session data is stored. It is `"cookie"` by default, but may be more secure if set to `"kong"` since access to the database would be required.|string|`"cookie"`|no|

**[Table of Contents](#table-of-contents)**


### Kubernetes and Red Hat OpenShift variables

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_namespace`|The Kubernetes `namespace` or Red Hat OpenShift `project` to deploy Kong for Kubernetes, Kong for Kubernetes Enterprise, Kong for Kubernetes with Kong Enterprise, or Kong Kubernetes Ingress Controller to.|string|`"kong"`|yes|
|`k4k8s_kubeconfig`|The path to your Kubernetes (`kubectl`) or Red Hat OpenShift CLI (`oc`) configuration file. This may be useful when working with multiple clusters and Kong deployment types.|string|`None` (unset)|no|
|`k4k8s_cluster_context`|The context to use for operating on a Kubernetes or Red Hat OpenShift cluster.  If not specified, the current context set in your `k4k8s_kubeconfig` will be used.  This may be useful when working with multiple clusters and Kong deployment types.|string|`None` (unset)|no|

**[Table of Contents](#table-of-contents)**

---


## Advanced variables

### Helm

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_helm_atomic`|Equivalent to the `helm` `--atomic` option.|boolean|`False`|no|
|`k4k8s_deploy_helm_binary_path`|Path to the `helm` executable.|string|`"helm"`|no|
|`k4k8s_deploy_helm_chart_ref`|The Helm chart name to use to deploy Kong for Kubernetes, Kong for Kubernetes Enterprise, Kong for Kubernetes with Kong Enterprise, and Kong Kubernetes Ingress Controller to Kubernetes or Red Hat OpenShift clusters.|string|`"kong/kong"`|no|
|`k4k8s_deploy_helm_chart_repo_name`|Name to install the Helm chart repository as.|string|`"kong"`|no|
|`k4k8s_deploy_helm_chart_repo_url`|URL for Kong's helm chart repository.|string|`"https://charts.konghq.com"`|no|
|`k4k8s_deploy_helm_chart_repo_username`|Username for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_deploy_helm_chart_repo_password`|Password for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_deploy_helm_chart_version`|Use if you need a particular Kong Helm Chart version, otherwise the latest chart will be used.|string|`None` (omitted)|no|
|`k4k8s_deploy_helm_disable_hook`|Corresponds to the `helm` `--no-hooks` option.|boolean|`False`|no|
|`k4k8s_deploy_helm_force_reinstall`|Helm option to force reinstall, ignore on new install.|boolean|`False`|no|
|`k4k8s_deploy_helm_release_name`|Name of the helm release.|string|`"kong"`|no|
|`k4k8s_deploy_helm_replace`|Corresponds to the `helm` `--replace` option.|boolean|`False`|no|
|`k4k8s_deploy_helm_update_repo`|Whether or not to update the helm chart repository prior to deployment.  This ensures the latest chart is available.  If a specific chart version is required, set the `k4k8s_deploy_helm_chart_version`|boolean|`True`|no|
|`k4k8s_deploy_helm_wait`|Whether or not to wait for the Helm Chart's objects to be successfully deployed and at desired state.|boolean|`True`|no|

**[Table of Contents](#table-of-contents)**

---


### Collected result variables and other set facts or variables

The following table of variables may be useful for debugging purposes.  You can access them after the `kong.kong.k4k8s-deploy` role has completed its run.  If running the `kong.kong.k4k8s-deploy` role via `ansible.builtin.include_role` you will need to add `public: True` to the module parameters, which allows you to access role variables after they have completed running.

| Variable name | Description |
| --- | --- |
|`__k4k8s_deploy_helm_results__`|The results collected when applying the kong/kong Helm chart|
|`__k4k8s_deploy_helm_release_values__`|The combined values from your helm values files and helm values.  This is what gets applied during Helm chart deployment.  Good way to validate your chart values are being read as you expect them to. |
|`__k4k8s_deploy_admin_gui_session_conf_string__`|The constructed dictionary for your Admin GUI Sessions configuration.|
|`__k4k8s_deploy_portal_session_conf_string__`|The constructed dictionary for your Dev Portal Sessions configuration.|
|`__k4k8s_deploy_openssl_key__['privatekey']`|The generated hybrid-mode control plane openssl shared-mode private key (be careful with this data due to potential security risks).|
|`__k4k8s_deploy_openssl_csr__['csr']`|The generated hybrid-mode control plane certificate signing request (CSR).|
|`__k4k8s_deploy_x509_cert__['certificate']`|The generated hybrid-mode control plane x509 certificate.|
|`__k4k8s_deploy_cp_hybrid_secret__`|When using the `k4k8s_deploy_create_hybrid_mode_dp_cert_secret` setting, the hybrid-mode certificate secret harvested from the Kong Enterprise control-plane cluster.|

**[Table of Contents](#table-of-contents)**

---


## Playbook usage examples

The following example assumes you already have all the necessary kubeconfigs in place on `linuxhost1`.  You could add additional steps to this playbook to fully configure `linuxhost1` so that it is ready to execute the play.


```yaml
---
- name: "Deploy kong enterprise control-plane and data-planes"
  hosts: "linuxhost1"
  vars_files:
    - /path/to/my/ansible_vault
  tasks:
    - name: "Deploy kong enterprise control-plane"
      ansible.builtin.include_role:
        name: "kong.kong.k4k8s_deploy"
        public: True # to be able to validate registered vars later
      vars:
        k4k8s_cluster_context: "kong-cp"
        k4k8s_deploy_helm_chart_values_files:
          - "kong-controlplane-values.yaml"
        k4k8s_deploy_create_enterprise_superuser_password_secret: True
        k4k8s_deploy_create_enterprise_license_secret: True
        k4k8s_deploy_enterprise_license_json_string: "{{ load_me_from_ansible_vault }}"
        k4k8s_deploy_create_postgres_password_secret: True
        k4k8s_deploy_create_hybrid_mode_cp_cert_secret: True
        k4k8s_deploy_create_admin_gui_sessions_conf_secret: True
        k4k8s_deploy_admin_gui_sessions_settings:
          cookie_domain: ".myapp.mydomain.com"
          cookie_name: "oatmeal-raisin"
          secret: "thisisverysecret"
          cookie_samesite: "off" # my kong manager and dev portal will be on different subdomains
        k4k8s_deploy_create_portal_sessions_conf_secret: True
        k4k8s_deploy_portal_sessions_settings:
          cookie_domain: ".dev.mydomain.com"
          cookie_name: "chocolate-chip"
          cookie_samesite: "off" # my kong manager and dev portal will be on different subdomains
          secret: "thisisreallysecret"
    
    - name: "Deploy kong enterprise data-planes"
      ansible.builtin.include_role:
        name: "kong.kong.k4k8s_deploy"
        public: True # to be able to validate registered vars later
      vars:
        k4k8s_cluster_context: "{{ item }}"
        k4k8s_deploy_helm_chart_values_files:
          - "kong-dataplane-values.yaml"
        k4k8s_deploy_create_enterprise_license_secret: True
        k4k8s_deploy_enterprise_license_json_string: "{{ load_me_from_ansible_vault }}"
        k4k8s_deploy_create_hybrid_mode_dp_cert_secret: True
        k4k8s_deploy_hybrid_mode_cert_harvest_cluster_context: "kong-control-plane" # optional if you only have 1 context in the kubeconfig
        k4k8s_deploy_hybrid_mode_cert_harvest_kubeconfig: "~/.kube/kong-control-plane-kubeconfig"
      with_items:
        - "on-premise"
        - "cloud1"
        - "cloud2"
        - "dr-site"
```

**[Table of Contents](#table-of-contents)**

---


### Sample Helm values files

[Here's a few examples](../../tests/integration/targets/test-k4k8s-deploy/files/) of Helm values files that were used in testing this role during development.

**[Table of Contents](#table-of-contents)**

---


## License

[Apache 2.0](../../LICENSE)

---


## Author

[Andrew J. Huffman](https://github.com/ahuffman)

---
**[Table of Contents](#table-of-contents)**