=======================
Kong.Kong Release Notes
=======================

.. contents:: Topics


v1.1.0
======

Release Summary
---------------

| We are adding 2 new integrations to enhance our Kong for Kubernetes deployments.
| 1. cert-manager deployment and configuration support has been added with the new kong.kong.k4k8s_cert_manager role.  
| 2. external-dns deployment and configuration for AWS Route53 has been added with the new kong.kong.k4k8s_external_dns role.

Major Changes
-------------

- Added cert-manager integration role kong.kong.k4k8s_cert_manager
- Added cert-manager integration role kong.kong.k4k8s_cert_manager
- Added external-dns integration role kong.kong.k4k8s_external_dns
- Added external-dns integration role kong.kong.k4k8s_external_dns

Minor Changes
-------------

- Created kong.kong.common.k4k8s_helm collection library role to standardize helm tasks across roles
- Refactored kong.kong.k4k8s_deploy to leverage new kong.kong.common.k4k8s_helm role
- Removed helm tasks that were migrated to the kong.kong.common.k4k8s_helm role
