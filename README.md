# Ansible Collection - kong.kong

<p align="center">
  <img src="https://2tjosk2rxzc21medji3nfn1g-wpengine.netdna-ssl.com/wp-content/uploads/2018/08/kong-combination-mark-color-256px.png" /></div>
</p>


## Description

A collection of Ansible assets to automate [Kong's](http://www.konghq.com/) portfolio of products.


## Collection Contents

Click on the name of a collection component within the table below for the full component documentation.

### Modules

|Module name|Description|
|---|---|
|[kong.kong.inso_generate_config](https://github.com/Kong/kong-ansible-collection/tree/main/docs/inso_generate_config.md)|Generate Kong Gateway and Kong Ingress Controller configurations from OpenAPI specifications.|
|[kong.kong.inso_lint_spec](https://github.com/Kong/kong-ansible-collection/tree/main/docs/inso_generate_config.md)|Lint and validate your OpenAPI specifications.|


### Roles

|Role name|Description|
|---|---|
|[kong.kong.k4k8s_cert_manager](https://github.com/Kong/kong-ansible-collection/tree/main/roles/k4k8s_cert_manager)|An Ansible role to deploy [cert-manager](https://cert-manager.io) for the purpose of automated deployment of TLS certificates with Kong Ingress Controller ingresses. This role includes a set of optional `ClusterIssuer` configurations.|
|[kong.kong.k4k8s_deploy](https://github.com/Kong/kong-ansible-collection/tree/main/roles/k4k8s_deploy)|An Ansible role to deploy Kong for Kubernetes, Kong for Kubernetes Enterprise, Kong for Kubernetes with Kong Enterprise, and Kong Ingress Controller to Kubernetes or Red Hat OpenShift clusters using Helm or YAML manifests.|
|[kong.kong.k4k8s_external_dns](https://github.com/Kong/kong-ansible-collection/tree/main/roles/k4k8s_external_dns)|An Ansible role to deploy and configure [external-dns](https://github.com/kubernetes-sigs/external-dns) on a Kubernetes or Red Hat OpenShift cluster for the purpose of automated deployment of DNS records with Kong Ingress Controller ingresses and Kong Gateway Enterprise services.|


## License
[Apache 2.0](LICENSE)


## Author

[Andrew J. Huffman](https://github.com/ahuffman)