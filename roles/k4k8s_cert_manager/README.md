# kong.kong.k4k8s_cert_manager

<p align="center">
  <img src="https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2018/08/kong-combination-mark-color-256px.png" /></div>
</p>

## Description

An Ansible role to deploy [cert-manager](https://cert-manager.io) on a Kubernetes or Red Hat OpenShift cluster for the purpose of automated deployment of TLS certificates with Kong for Kubernetes ingresses.  The role can optionally deploy a cert-manager `ClusterIssuer` for the [ACME protocol](https://tools.ietf.org/html/rfc8555) via [Let's Encrypt](https://letsencrypt.org/how-it-works/) using either a http solver or DNS solver.



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
    1. [Kubernetes and Red Hat OpenShift variables](#kubernetes-and-red-hat-openshift-variables)
    2. [Helm variables](#helm-variables)
    3. [Cert-manager ClusterIssuer global variables](#cert-manager-clusterissuer-global-variables)
        1. [DNS Solver - AWS Route53 integration variables](#dns-solver-aws-route53-integration-variables)
6. [Advanced Variables](#advanced-variables)
    1. [Helm](#helm)
    2. [Cert-manager deployment and configuration](#cert-manager-deployment-and-configuration)
7. [Playbook usage examples and how-to guide](#playbook-usage-examples-and-how-to-guide)
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

1. [Helm3](https://helm.sh/docs/intro/install/) `helm` is required on the target Ansible host (`{{ inventory_hostname }}`) in `$PATH`.


**[Table of Contents](#table-of-contents)**

---


## Testing and Supported Platforms

WIP


## Default variables

The following tables outline variables available in [defaults/main.yml](defaults/main.yml) and are used to control the behavior of the `kong.kong.k4k8s_cert_manager` Ansible role. They are presented based on how they affect the overall operation of the role's automation.


### Kubernetes and Red Hat OpenShift variables
|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_cm_namespace`|Kubernetes or Red Hat OpenShift namespace to deploy cert-manager to.|string|`"cert-manager"`|yes|
|`k4k8s_kubeconfig`|Path to kubeconfig to use during Kubernetes and Red Hat OpenShift operations.|string|`None` (unset)|no|
|`k4k8s_cluster_context`|The Kubernetes or Red Hat OpenShift context to use within the specified or default kubeconfig|string|`None` (unset)|no|

**[Table of Contents](#table-of-contents)**

---


### Helm variables
|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_cm_helm_chart_values_files`|List of [Helm values files](https://helm.sh/docs/chart_template_guide/values_files/) that modify the deployment of cert-manager. See the available values [here](https://artifacthub.io/packages/helm/cert-manager/cert-manager)|list/array|`[]`|no|
|`k4k8s_cm_helm_chart_values`|Dictionary of Helm values to apply to the cert-manager Helm charts.  See the available values [here](https://artifacthub.io/packages/helm/cert-manager/cert-manager). Can be used with `k4k8s_cm_helm_chart_values_files`, or alone. If combining with `k4k8s_cm_helm_chart_values_files` these values will be applied last and can override values in your `k4k8s_cm_helm_chart_values_files` via recursive dictionary merges and any lists are replaced with the new value. This is a great way to override a single value or a few. See Ansible's [combine filter documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-hashes-dictionaries) for more clarity on this merge methodology.|dictionary|`{}`|no|
|`k4k8s_cm_helm_chart_values_remote`|Whether or not the `k4k8s_cm_helm_chart_values_files` should be read from the `{{ inventory_hostname }}` or Ansible control node. Set to `true` when the Helm values files are on the remote `{{ inventory_hostname }}`.|boolean|`false`|yes|

**[Table of Contents](#table-of-contents)**

---


### Cert-manager ClusterIssuer global variables

These variables apply when `k4k8s_cm_create_cluster_issuer: true`.

|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_cm_create_cluster_issuer`|Whether or not to deploy a cert-manager `ClusterIssuer`. The current `ClusterIssuer` configurations available with this Kong for Kubernetes integration leverage the [ACME protocol](https://tools.ietf.org/html/rfc8555) via [Let's Encrypt](https://letsencrypt.org/how-it-works/). To learn more about the concept of `Issuer` and `ClusterIssuer` resources, see the cert-manager [Issuer Configuration](https://cert-manager.io/docs/configuration/) documentation.|boolean|`false`|yes|
|`k4k8s_cm_solver`|Cert-manager must resolve requests for new ACME TLS certificate requests with a "solver".  The certificate issuer checks the solver to validate a domain belongs to the requester.  This role currently supports a pre-defined http-based solver that will function with Kong's products, as well as a DNS based solver configuration for AWS Route53.  Use the setting value of `"http_acme"` for the http solver ClusterIssuer configuration.  Use the value of `dns_route53_acme` for the AWS Route53 DNS solver ClusterIssuer configuration.|string|`"http"`|no|
|`k4k8s_cm_acme_acct_email_address`|An email address is required when requesting certificates via [Let's Encrypt](https://letsencrypt.org/how-it-works/).  Please specify a preferred email address.|string|`""`|no|

**[Table of Contents](#table-of-contents)**

---


#### DNS Solver - AWS Route53 integration variables

These variables apply when `k4k8s_cm_create_cluster_issuer: true` and `k4k8s_cm_solver: "dns_route53"` are set.  Currently this integration is configured to use a programatic AWS IAM user and role with appropriate [Route53 permissions](https://cert-manager.io/docs/configuration/acme/dns01/route53/#set-up-an-iam-role).  While more providers may be added in the future, if you have an immediate need, please file a new [issue](https://github.com/Kong/kong-ansible-collection/issues).  Pull requests are also welcome, if you would like to add in additional functionality.

|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_cm_route53_access_key_id`|Your AWS programatic IAM user access key ID for use with cert-manager.|string|`""`|no|
|`k4k8s_cm_route53_secret_access_key`|Your AWS programatic IAM user secret access key for use with cert-manager.  This will be stored in a Kubernetes or Red Hat OpenShift secret.|string|`""`|no|
|`k4k8s_cm_route53_region`|It is required to specify an AWS region which is used when authenticating to AWS via cert-manager for modifying temporary Route53 records.|string|`""`|no|
|`k4k8s_cm_route53_dns_zones`|List of AWS Route53 DNS hosted zones.  See [DNS Zones](https://cert-manager.io/docs/configuration/acme/#dns-zones) in the cert-manager documentation for more details.|list/array|`[]`|no|

**[Table of Contents](#table-of-contents)**

---


## Advanced Variables

The variables defined in the sections below are available for deeper configuration of the role, and probably will not need to be overridden in most use-cases.


### Helm

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_cm_helm_atomic`|Equivalent to the `helm` `--atomic` option.|boolean|`false`|no|
|`k4k8s_cm_helm_binary_path`|Path to the `helm` executable.|string|`"helm"`|no|
|`k4k8s_cm_helm_chart_ref`|The Helm chart name to use to deploy cert-manager to Kubernetes or Red Hat OpenShift clusters.|string|`"jetstack/cert-manager"`|no|
|`k4k8s_cm_helm_chart_repo_name`|Name to install the Helm chart repository as.|string|`"jetstack"`|no|
|`k4k8s_cm_helm_chart_repo_url`|URL for cert-manager's helm chart repository.|string|`"https://charts.jetstack.io"`|no|
|`k4k8s_cm_helm_chart_repo_username`|Username for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_cm_helm_chart_repo_password`|Password for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_cm_helm_chart_version`|Use if you need a particular Kong Helm Chart version, otherwise the latest chart will be used.|string|`"v1.8.2"`|no|
|`k4k8s_cm_helm_disable_hook`|Corresponds to the `helm` `--no-hooks` option.|boolean|`false`|no|
|`k4k8s_cm_helm_force_reinstall`|Helm option to force reinstall, ignore on new install.|boolean|`False`|no|
|`k4k8s_cm_helm_release_name`|Name of the helm release.|string|`"cert-manager"`|no|
|`k4k8s_cm_helm_replace`|Corresponds to the `helm` `--replace` option.|boolean|`false`|no|
|`k4k8s_cm_helm_update_repo`|Whether or not to update the helm chart repository prior to deployment.  This ensures the latest chart is available.  If a specific chart version is required, set the `k4k8s_cm_helm_chart_version`|boolean|`true`|no|
|`k4k8s_cm_helm_wait`|Whether or not to wait for the Helm Chart's objects to be successfully deployed and at desired state.|boolean|`true`|no|

**[Table of Contents](#table-of-contents)**

---


### Cert-manager deployment and configuration

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_cm_crd_install_url`|URL to install the cert-manager CRDs for Kubernetes or Red Hat OpenShift from.|string|`"https://github.com/cert-manager/cert-manager/releases/download/{{ k4k8s_cm_helm_chart_version }}/cert-manager.crds.yaml"`|no|
|`k4k8s_cm_crd_names`|Used to perform an idempotency check to verify if the cert-manager CRDs have already been installed on the cluster.|list/array|see [vars/main.yml](https://github.com/Kong/kong-ansible-collection/blob/main/roles/k4k8s_cert_manager/vars/main.yml)|no|
|`k4k8s_cm_acme_server`|The ACME protocol Let's Encrypt server to use when requesting TLS certificates.|string|`"https://acme-v02.api.letsencrypt.org/directory"`|no|
|`k4k8s_cm_cluster_issuer_name`|Name of the `ClusterIssuer` Kubernetes or Red Hat OpenShift resource to create|string|`"letsencrypt-prod"`|no|
|`k4k8s_cm_route53_secret_name`|Name of the Kubernetes or Red Hat OpenShift secret to store the AWS Route53 `k4k8s_cm_route53_secret_access_key` in.|string|`"aws-route53-secret-access-key"`|no|
|`k4k8s_cm_route53_secret_access_key_key`|Name of the dictionary key within the `k4k8s_cm_route53_secret_name` secret to store the `k4k8s_cm_route53_secret_access_key` data in.|string|`"aws-secret-access-key"`|no|

**[Table of Contents](#table-of-contents)**

---


## Playbook usage examples and how-to guide

```yaml
---
- name: "Ensure cert-manager is deployed for Kong"
  hosts: "localhost"
  vars_files:
    - /path/to/my/ansible_vault.yml
  tasks:
    - name: "Ensure cert-manager is deployed with no ClusterIssuer"
      ansible.builtin.include_role:
        name: "kong.kong.k4k8s_cert_manager"
```

**[Table of Contents](#table-of-contents)**

---


## License

[Apache 2.0](https://github.com/Kong/kong-ansible-collection/blob/main/LICENSE)


## Author

[Andrew J. Huffman](https://github.com/ahuffman)

**[Table of Contents](#table-of-contents)**

---
