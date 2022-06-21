| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_validate_python_dependencies`|Whether or not to validate Python dependencies required for this role's operation are installed.  This will cause the role to fail fast if they are not available.|boolean|`True`|yes|
|`k4k8s_deploy_install_python_dependencies`|Whether or not to install Python dependencies required for this role's operation.|boolean|`False`|yes|
|`k4k8s_deploy_python_package_manager`|The Python package management tool to leverage when `k4k8s_deploy_install_python_dependencies: True`|string|`"pip"`|no|
|`k4k8s_deploy_validate_ansible_collection_dependencies`|Whether or not to validate Ansible Galaxy Collection dependencies required for this role's operation are installed.  This will cause the role to fail fast if they are not available.|boolean|`True`|yes|
|`k4k8s_deploy_install_ansible_collection_dependencies`|Whether or not to install Ansible Galaxy Collections required for this role's operation.|boolean|`False`|yes|
|`k4k8s_deploy_validate_binary_dependencies`|Whether or not to validate binary dependencies required for this role's operation are installed.  This will cause the role to fail fast if they are not available.|boolean|`True`|yes|
|`k4k8s_deploy_install_binary_dependencies`|Whether or not to install binary dependencies required for this role's operation. This will use built-in package managers and package repositories.  In the case of a `k4k8s_deploy_method: "helm"`, the Helm tarball will be downloaded and binary installed to `/usr/local/bin`.|boolean|`False`|yes|


## Advanced variables

The following tables outline variables located in [vars/main.yml](vars/main.yml), [vars/Debian.yml](vars/Debian.yml), [vars/Linux.yml](vars), [vars/RedHat.yml](vars/RedHat.yml), and [vars/Suse.yml](vars/Suse.yml) that may be required for successful operation and customization for environments that may have stringent security requirements.  Chances are, you typically will not need to change any of these settings in most cases.


### Python

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_python_module_deps`|List of Python `pip` or `pipx` package manager packages to install or validate they are installed.|list (array)|`["kubernetes"]`|no|

**[Table of Contents](#table-of-contents)**

---


#### pip configuration

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_pyvenv_path`|Path to a specific Python vitrual environment.|string|`None` (omitted)|no|
|`k4k8s_deploy_pip_executable_path`|Path to your `pip` Python package manager.|string|`"pip3"`|no|
|`k4k8s_deploy_python_umask`|Ensure your `umask` is set appropriately during `pip` package installation operations.|string|`"0022"`|no|

**[Table of Contents](#table-of-contents)**

---


#### pipx configuration

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_pipx_package`|Name of the `pipx` package to install additional Python module packages to.|string|`"ansible-core" # set to function within default GitHub Actions runners`|no|
|`k4k8s_deploy_pipx_executable_path`|Path to your `pipx` Python package manager.|string|`"pipx"`|no|

**[Table of Contents](#table-of-contents)**

---


### Ansible configuration

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_ansible_collection_deps`|List of Ansible Galaxy Collection dependencies required for the role to properly function.  Used when `k4k8s_deploy_validate_ansible_collection_dependencies` or `k4k8s_deploy_install_ansible_collection_dependencies` are set to `True`.|list (array)|`["community.general", "kubernetes.core"]`|no|
|`k4k8s_deploy_ansible_collection_deps_hybrid_certs`|List of Ansible Galaxy Collection dependencies required for the role to properly function.  Used when `k4k8s_deploy_validate_ansible_collection_dependencies` or `k4k8s_deploy_install_ansible_collection_dependencies` are set to `True` and `k4k8s_deploy_create_hybrid_mode_certificate_secrets` is set to `True`.|list (array)|`["community.crypto"]`|no|
|`k4k8s_deploy_ansible_collection_path`|Desired path for installing Ansible Galaxy Collections.  Used when `k4k8s_deploy_install_ansible_collection_dependencies` is set to `True`.|string|None (omitted)|no|
|`k4k8s_deploy_ansible_galaxy_executable_path`|Path to the location of your `ansible-galaxy` executable.|string|`"ansible-galaxy`|no|

**[Table of Contents](#table-of-contents)**

---


### Binaries

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_bin_deps`|List of binary dependencies required for the role to operate properly.  Used when `k4k8s_deploy_validate_binary_dependencies` is set to `True`.|list (array)|`[]`|no|
|`k4k8s_deploy_bin_deps_helm_method`|List of binary dependencies required for the role to operate properly when `k4k8s_deploy_method` is set to `"helm"` and k4k8s_deploy_validate_binary_dependencies` is set to `True`.|list (array)|`["helm"]`|no|
|`k4k8s_deploy_bin_install_proxy_enabled`|Controls use of a web proxy server, and in this role's case, specifically when downloading tarballs when `k4k8s_deploy_install_binary_dependencies` is set to `True`.  See details [here](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/get_url_module.html#parameter-use_proxy).|boolean|`None` (omitted)|no|
|`k4k8s_deploy_install_bin_pkgs`|List of packages to install from a OS' package manager.  This may be different for each OS based target.  Found in [vars/Debian.yml](vars/Debian.yml), [vars/RedHat.yml](vars/RedHat.yml), and [vars/Suse.yml](vars/Suse.yml).|list (array)|`[]`|no|
|`k4k8s_deploy_install_pkg_repos`|List of dictionaries for OS package repository setup when installing packages from a OS' package manager.  Used when `k4k8s_deploy_install_binary_dependencies` is set to `True`.  This may be different for each OS based target.  Check in [vars/Debian.yml](vars/Debian.yml), [vars/RedHat.yml](vars/RedHat.yml), and [vars/Suse.yml](vars/Suse.yml) for examples.|list (array) of dictionaries|`[]`|no|

**[Table of Contents](#table-of-contents)**

---


#### Tarball based binary installation

| Variable name | Description | Variable type | Default value | Required |
| --- | --- | --- | --- | --- |
|`k4k8s_deploy_bin_version_info`|Contains information on how to obtain, install, and validate a tarball binary package in a repeatable manner.  Used when `k4k8s_deploy_install_binary_dependencies` is set to `True`.|dictionary|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.<binary name>`|Name that corresponds to `k4k8s_deploy_install_bin_tarballs[].name`.|dictionary|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.< binary name >.checksum`|Contains checksums based on OS and architecture for the tarball binary package.|dictionary|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.<binary name>.checksum.< OS >`|Contains checksums for a particular OS type and architecture defined by `{{ ansible_system | lower }}`.|dictionary|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.<binary name>.checksum.< OS >.< architecture >`|Contains the checksum for a particular OS types particular architecture defined by `{{ ansible_architecture }}`.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.< binary name >.version`|Version of a tarball binary package to install.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.< binary name >.baseurl`|Base-URL to build a download URL path off of for a particular tarball binary package.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.< binary name >.extension|File extension used to build multiple filenames and URLs with for a particular tarball binary package.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_bin_version_info.< binary name >.destination`|Location to move the extracted binary to from a tarball binary package.|string|`"/usr/local/bin"`|no|
|`k4k8s_deploy_install_bin_tarballs_helm_method`|Same as `k4k8s_deploy_install_bin_tarballs` in structure and used when `k4k8s_deploy_method: "helm"` and `k4k8s_deploy_install_binary_dependencies: True`.|dictionary|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_install_bin_tarballs`|List of dictionaries containing a tarball package `name` which corresponds to the `k4k8s_deploy_bin_version_info.<binary name>`. Used when `k4k8s_deploy_install_binary_dependencies: True`.|list (array) of dictionaries|`[]`|no|
|`k4k8s_deploy_install_bin_tarballs[].name`|Name for a binary to install from a tarball binary package.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_install_bin_tarballs[].extracted_dir`|Expected directory name when a tarball binary package is extracted.  Values in `k4k8s_deploy_bin_version_info` are used to assemble this dynamically.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_install_bin_tarballs[].dl_filename`|Filename to download a tarball binary package to within a temporary directory.  Values from within `k4k8s_deploy_bin_version_info` can be leveraged to assemble this path.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_install_bin_tarballs[].url`|Download URL for a tarball binary package assembled from values found in `k4k8s_deploy_bin_version_info`.|string|see value in [vars/main.yml](vars/main.yml)|no|
|`k4k8s_deploy_install_bin_tarballs_helm_method`|Same as `k4k8s_deploy_install_bin_tarballs` in structure, and used when `k4k8s_deploy_method: "helm"` and `k4k8s_deploy_install_binary_dependencies: True`|list (array) of dictionaries|see value in [vars/main.yml](vars/main.yml)|no|

---


### Collected result variables and other set facts or variables

The following table of variables may be useful for debugging purposes.  You can access them after the `kong.kong.k4k8s-deploy` role has completed its run.  If running the `kong.kong.k4k8s-deploy` role via `ansible.builtin.include_role` you will need to add `public: True` to the module parameters, which allows you to access role variables after they have completed running.

| Variable name | Description |
| --- | --- |
|`__k4k8s_deploy_ansible_galaxy_results__`|The command results from `ansible-galaxy collection list` during the prerequisite validation process|
