# kong.kong.k4k8s_external_dns

[![k4k8s_external_dns](https://github.com/Kong/kong-ansible-collection/actions/workflows/k4k8s_external_dns-ci.yml/badge.svg)](https://github.com/Kong/kong-ansible-collection/actions/workflows/k4k8s_external_dns-ci.yml)

<p align="center">
  <img src="https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2018/08/kong-combination-mark-color-256px.png" /></div>
</p>

## Description

An Ansible role to deploy [external-dns](https://github.com/kubernetes-sigs/external-dns) on a Kubernetes or Red Hat OpenShift cluster for the purpose of automated deployment of DNS records with Kong Kubernetes Ingress Controller ingresses and Kong Gateway Enterprise services.

***WIP below here***

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
    3. [ExternalDNS global variables](#externaldns-global-variables)
    4. [ExternalDNS provider variables](#externaldns-provider-variables)
6. [Advanced Variables](#advanced-variables)
    1. [Helm](#helm)
    2. [Secrets](#secrets)
        1. [AWS Route53 Secret](#aws-route53-secret)
    3. [Collected result variables and other set facts or variables](#collected-result-variables-and-other-set-facts-or-variables)
7. [Playbook usage examples and how-to guide](#playbook-usage-examples-and-how-to-guide)
    1. [Prerequisites for AWS Route53](#prerequisites-for-aws-route53)
        1. [Deploy external-dns for use with Kong Ingresses with AWS Route53](#deploy-external-dns-for-use-with-kong-ingresses-with-aws-route53)
        2. [Deploy Kong Gateway and external-dns](#deploy-kong-gateway-and-external-dns)
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

This Ansible role was validated to function using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html) and [this](../../.github/workflows/k4k8s_external_dns-ci.yml) GitHub Actions workflow.

The testing targets the latest version of Kubernetes available from [`microk8s`](https://microk8s.io/) a fully compliant and lightweight Kubernetes distribution and Red Hat OpenShift using the [`microshift-aio:latest`](https://microshift.io/) container image.

The testing matrix is validated against the following `ansible-test` containers as target hosts and launched from the default `ansible-test` container:

|Test Container|Python Version|
|---|---|
|default|3.10|
|ubuntu1804|3.6|
|ubuntu2004|3.8|
|opensuse15|3.6|


## Default variables

The following tables outline variables available in [defaults/main.yml](defaults/main.yml) and are used to control the behavior of the `kong.kong.k4k8s_external_dns` Ansible role. They are presented based on how they affect the overall operation of the role's automation.


### Kubernetes and Red Hat OpenShift variables
|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_edns_namespace`|Kubernetes or Red Hat OpenShift namespace to deploy external-dns to.|string|`"external-dns"`|yes|
|`k4k8s_kubeconfig`|Path to kubeconfig to use during Kubernetes and Red Hat OpenShift operations.|string|`None` (unset)|no|
|`k4k8s_cluster_context`|The Kubernetes or Red Hat OpenShift context to use within the specified or default kubeconfig|string|`None` (unset)|no|

**[Table of Contents](#table-of-contents)**

---


### Helm variables
|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_edns_helm_chart_values_files`|List of [Helm values files](https://helm.sh/docs/chart_template_guide/values_files/) that modify the deployment of external-dns. See the available values [here](https://github.com/kubernetes-sigs/external-dns/tree/master/charts/external-dns)|list/array|`[]`|no|
|`k4k8s_edns_helm_chart_values`|Dictionary of Helm values to apply to the external-dns Helm chart.  See the available values [here](https://github.com/kubernetes-sigs/external-dns/tree/master/charts/external-dns). Can be used with `k4k8s_edns_helm_chart_values_files`, or alone. If combining with `k4k8s_edns_helm_chart_values_files` these values will be applied last and can override values in your `k4k8s_edns_helm_chart_values_files` via recursive dictionary merges and any lists are replaced with the new value. This is a great way to override a single value or a few. See Ansible's [combine filter documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-hashes-dictionaries) for more clarity on this merge methodology.|dictionary|`{}`|no|
|`k4k8s_edns_helm_chart_values_remote`|Whether or not the `k4k8s_edns_helm_chart_values_files` should be read from the `{{ inventory_hostname }}` or Ansible control node. Set to `true` when the Helm values files are on the remote `{{ inventory_hostname }}`.|boolean|`false`|yes|

**[Table of Contents](#table-of-contents)**

---


### ExternalDNS global variables

The following variables expose several of the most commonly configured external-dns Helm chart values without requiring knowledge of all possible chart configurations.  These

|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_edns_create_provider_secret`|Whether or not to create the Kubernetes or Red Hat OpenShift secret.  It is recommended to set this to `true` and provide your `k4k8s_edns_aws_access_key_id` and `k4k8s_edns_aws_secret_access_key` (via `ansible-vault`) to fully automate the process.  If you wish to create a provider secret out of band, you can alternatively set the Helm chart value of `env` with your own secretRef settings.|boolean|`false`|yes|
|`k4k8s_edns_provider`|The DNS provider to configure external-dns for.  Currently `aws` (Route53) is the only supported provider with this role.  More providers will be added in the future.|string|`"aws"`|yes|
|k4k8s_edns_domain_filters|Corresponds to the external-dns Helm chart value `domainFilters` and the command line option `--domain-filter`.  List of possible target zones to limit DNS record management by domain suffixes.|list (array)|`[]`|yes|
|k4k8s_edns_sync_policy|Corresponds to the external-dns Helm chart value `policy` and command line option `--policy`.  How DNS records are synchronized between sources and provides.  The available values are `sync` or `upsert-only`.  `sync` will perform both creation and deletion of DNS records, while `upsert-only` will only create DNS records.|string|`"upsert-only"`|yes|
|k4k8s_edns_sync_interval|Corresponds to the external-dns Helm chart value `interval` and command line option `--interval`.  How often to synchronize DNS updates with the DNS provider.|string|`"1m"`|yes|
|k4k8s_edns_txt_owner_id|Adds a `external-dns/owner=` field to TXT records within the DNS provider, which can help with identification of which external-dns instance created a record.|string|`""`|yes|
|k4k8s_edns_txt_prefix|Adds a prefix to the name of each TXT record created within the DNS provider.  Useful for identification of which external-dns instance created a record within a domain.|string|`""`|yes|
|k4k8s_edns_txt_suffix|Adds a suffix to the name of each TXT record created within the DNS provider.  Useful for identification of which external-dns instance created a record within a domain.|string|`""`|yes|

**[Table of Contents](#table-of-contents)**

---


### ExternalDNS provider variables

These variables apply when `k4k8s_edns_create_provider_secret: true`.

|Variable name|Description|Variable type|Default value|Required|
|---|---|---|---|---|
|`k4k8s_edns_aws_access_key_id`|The AWS access key ID that corresponds to the `k4k8s_edns_aws_secret_access_key` for the AWS IAM programmatic account with access to manage your AWS Route53 records.  This should be provided by a secure mechanism such as `ansible-vault`.|
|`k4k8s_edns_aws_secret_access_key`|The AWS secret access key that corresponds to the `k4k8s_edns_aws_access_key_id` for the AWS IAM programmatic account with access to manage your AWS Route53 records.  This should be provided by a secure mechanism such as `ansible-vault`.|

**[Table of Contents](#table-of-contents)**

---


## Advanced Variables

The variables defined in the sections below are available for deeper configuration of the role, and probably will not need to be overridden in most use-cases.


### Helm

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_edns_helm_atomic`|Equivalent to the `helm` `--atomic` option.|boolean|`false`|no|
|`k4k8s_edns_helm_binary_path`|Path to the `helm` executable.|string|`"helm"`|no|
|`k4k8s_edns_helm_chart_ref`|The Helm chart name to use to deploy external-dns to Kubernetes or Red Hat OpenShift clusters.|string|`"external-dns/external-dns"`|no|
|`k4k8s_edns_helm_chart_repo_name`|Name to install the Helm chart repository as.|string|`"external-dns"`|no|
|`k4k8s_edns_helm_chart_repo_url`|URL for external-dns's helm chart repository.|string|`"https://kubernetes-sigs.github.io/external-dns/"`|no|
|`k4k8s_edns_helm_chart_repo_username`|Username for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_edns_helm_chart_repo_password`|Password for helm chart access.|string|`None` (omitted)|no|
|`k4k8s_edns_helm_chart_version`|Use if you need a particular external-dns version, otherwise the latest chart will be used.|string|`None` (unset)|no|
|`k4k8s_edns_helm_disable_hook`|Corresponds to the `helm` `--no-hooks` option.|boolean|`false`|no|
|`k4k8s_edns_helm_force_reinstall`|Helm option to force reinstall, ignore on new install.|boolean|`False`|no|
|`k4k8s_edns_helm_release_name`|Name of the helm release.|string|`"external-dns"`|no|
|`k4k8s_edns_helm_replace`|Corresponds to the `helm` `--replace` option.|boolean|`false`|no|
|`k4k8s_edns_helm_update_repo`|Whether or not to update the helm chart repository prior to deployment.  This ensures the latest chart is available.  If a specific chart version is required, set the `k4k8s_edns_helm_chart_version`|boolean|`true`|no|
|`k4k8s_edns_helm_wait`|Whether or not to wait for the Helm Chart's objects to be successfully deployed and at desired state.|boolean|`true`|no|

**[Table of Contents](#table-of-contents)**

---


### Secrets

The following variables are useful if you would like to modify how the Kubernetes or Red Hat OpenShift external-dns secret is created. You can choose fully ignore these variables and provide your own Helm values for the external-dns Helm chart's `env` value.

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|k4k8s_edns_provider_secret_name|Name of the secret to create in your `k4k8s_edns_namespace` on your Kubernetes or Red Hat OpenShift cluster.|string|`"external-dns"`|no|


#### AWS Route53 Secret
|k4k8s_edns_aws_access_key_id_key|Name of the key where the AWS access key id will be stored within the `k4k8s_edns_provider_secret_name` secret.|string|`"aws_access_key_id"`|no|
|k4k8s_edns_aws_secret_access_key_key|Name of the key where the AWS secret access key will be stored within the `k4k8s_edns_provider_secret_name` secret.|string|`"aws_secret_access_key"`|no|

**[Table of Contents](#table-of-contents)**

---


### Collected result variables and other set facts or variables

The following table of variables may be useful for debugging purposes.  You can access them after the `kong.kong.k4k8s_external_dns` role has completed its run.  If running the `kong.kong.k4k8s_external_dns` role via `ansible.builtin.include_role` you will need to add `public: true` to the module parameters, which allows you to access role variables after they have completed running.

|Variable name|Description|
|---|---|
|`__k4k8s_edns_helm_results__`|The results collected from applying the external-dns Helm chart via the `kubernetes.core.helm` Ansible module|
|`__k4k8s_edns_helm_release_values__`|The combined values from your helm values files and helm values.  This is what gets applied during Helm chart deployment.  Good way to validate your chart values are being read as you expect them to. |

**[Table of Contents](#table-of-contents)**

---


## Playbook usage examples and how-to guide

### Prerequisites for AWS Route53

1. Create an AWS IAM Policy like the example found [here](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md#iam-policy).  You may want to further restrict the policy to specific DNS Zones.

1. Create an AWS IAM programmatic user and attach the IAM Policy for external-dns you created to it.

---
**[Table of Contents](#table-of-contents)**


#### Deploy external-dns for use with Kong Ingresses with AWS Route53

```yaml
---
- name: "Deploy external-dns for Kong with AWS Route53"
  hosts: "localhost"
  vars:
    cluster_name: "my-cluster"
  vars_files:
    - "/path/to/my/ansible/vault.yaml"
  tasks:
    - name: "Ensure external-dns with AWS Route53 is present"
      ansible.builtin.include_role:
        name: "kong.kong.k4k8s_external_dns"
      vars:
        k4k8s_kubeconfig: "/path/to/my/cluster/kubeconfig"
        k4k8s_edns_create_provider_secret: true
        k4k8s_edns_aws_access_key_id: "{{ aws_access_key_id }}"  # from ansible-vault
        k4k8s_edns_aws_secret_access_key: "{{ aws_secret_access_key }}"  # from ansible-vault
        k4k8s_edns_helm_chart_values:
          extraArgs:
            - "--aws-prefer-cname"  # Use CNAME's instead of proprietary ALIAS records
        k4k8s_edns_txt_prefix: "{{ cluster_name }}"
        k4k8s_edns_txt_owner_id: "{{ cluster_name }}"
        k4k8s_edns_sync_interval: "15m"
        k4k8s_edns_sync_policy: "sync"  # create and delete DNS records
        k4k8s_edns_domain_filters:
          - "example.com"
```

Once your external-dns instance has been deployed, you can add an annotation such as `external-dns.alpha.kubernetes.io/hostname: myingress.example.com` to your Kubernetes ingresses and services as needed.  

---
**[Table of Contents](#table-of-contents)**


#### Deploy Kong Gateway and external-dns with AWS Route53

```yaml
- name: "Deploy Kong Gateway and external-dns with AWS Route53"
  hosts: "localhost"
  vars:
    ingress_dns_zone: "example.com"
    cluster_name: "my-cluster"
    k4k8s_kubeconfig: "/path/to/my/cluster/kubeconfig"
  vars_files:
    - "/path/to/my/ansible/vault.yaml"
  tasks:
    - name: "Ensure external-dns with AWS Route53 is present"
      ansible.builtin.include_role:
        name: "kong.kong.k4k8s_external_dns"
      vars:
        k4k8s_edns_create_provider_secret: true
        k4k8s_edns_aws_access_key_id: "{{ aws_access_key_id }}"  # from ansible-vault
        k4k8s_edns_aws_secret_access_key: "{{ aws_secret_access_key }}"  # from ansible-vault
        k4k8s_edns_helm_chart_values:
          extraArgs:
            - "--aws-prefer-cname"  # Use CNAME's instead of proprietary ALIAS records
        k4k8s_edns_txt_prefix: "{{ cluster_name }}"
        k4k8s_edns_txt_owner_id: "{{ cluster_name }}"
        k4k8s_edns_sync_interval: "15m"
        k4k8s_edns_sync_policy: "sync"  # create and delete DNS records
        k4k8s_edns_domain_filters:
          - "{{ ingress_dns_zone }}"

    - name: "Ensure kong control-plane is present and configured"
      ansible.builtin.include_role:
        name: "kong.kong.k4k8s_deploy"
      vars:
        k4k8s_kubeconfig: "/path/to/my/cluster/kubeconfig"
        k4k8s_deploy_create_enterprise_superuser_password_secret: true
        k4k8s_deploy_enterprise_license_json_string: "{{ kong_enterprise_license_from_vault }}"
        k4k8s_deploy_enterprise_superuser_password: "{{ kong_enterprise_admin_pass_from_vault }}"
        k4k8s_deploy_create_postgres_password_secret: true
        k4k8s_deploy_postgres_admin_password: "{{ pgsql_admin_pass_from_vault }}"
        k4k8s_deploy_postgres_user_password: "{{ pgsql_user_pass_from_vault }}"
        k4k8s_deploy_create_hybrid_mode_cp_cert_secret: true
        k4k8s_deploy_create_admin_gui_sessions_conf_secret: true
        k4k8s_deploy_admin_gui_sessions_settings:
          cookie_domain: ".{{ ingress_dns_zone }}"
          cookie_name: "oatmeal-raisin"
          cookie_samesite: "off"
          cookie_secure: true
          secret: "thisisverysecret"
        k4k8s_deploy_create_portal_sessions_conf_secret: true
        k4k8s_deploy_portal_sessions_settings:
          cookie_domain: ".{{ ingress_dns_zone }}"
          cookie_name: "chocolate-chip"
          cookie_samesite: "off"
          cookie_secure: true
          secret: "thisisreallysecret"
        k4k8s_deploy_helm_chart_values_files:
          - "kong-enterprise-values.yaml"
        # the following lets us recycle a common helm values file for multiple kong environments
        k4k8s_deploy_helm_chart_values:
            admin:
              ingress:
                hostname: "admin.{{ ingress_dns_zone }}"
            manager:
              ingress:
                hostname: "manager.{{ ingress_dns_zone }}"
            portal:
              ingress:
                hostname: "portal.{{ ingress_dns_zone }}"
            portalapi:
              ingress:
                hostname: "portalapi.{{ ingress_dns_zone }}"
            proxy:
              annotations:
                external-dns.alpha.kubernetes.io/hostname: "{{ cluster_name }}.{{ ingress_dns_zone }}"
```

In the above scenario you would be deploying an all-in-one Kong Enterprise deployment, with Kong Ingress Controller exposing all of your services on the `my-cluster.example.com` proxy (Kong Gateway).  You could reach the Kong Admin API via `admin.example.com`, the Kong Manager UI via `manager.example.com`, the Kong Developer Portal UI via `portal.example.com`, and the Kong Developer Portal API via `portalapi.example.com`.

Again, much of this is dependent on the contents of your [Helm values files for deploying Kong for Kubernetes](https://github.com/Kong/charts/blob/main/charts/kong/README.md).

---
**[Table of Contents](#table-of-contents)**


## License

[Apache 2.0](https://github.com/Kong/kong-ansible-collection/blob/main/LICENSE)


## Author

[Andrew J. Huffman](https://github.com/ahuffman)

**[Table of Contents](#table-of-contents)**
