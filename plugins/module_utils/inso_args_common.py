COMMON_ARG_SPEC = {
    "binary_path": {"type": "path", "required": False},
    "config": {"type": "path", "required": False},
    "working_dir": {"type": "path", "required": False},
    "src": {"type": "path", "required": False}
}

def build_base_cmd(module):
    cmd = []
    # get inso binary path
    if not module.params["binary_path"]:
        cmd.append(module.get_bin_path(
            "inso",
            required=True)
        )
    else:
        cmd.append(module.get_bin_path(
            module.params["binary_path"],
            required=True)
        )

    # --config
    if module.params["config"]:
        cmd.append("--config")
        cmd.append(module.params["config"])

    # --src
    if module.params["src"]:
        cmd.append("--src")
        cmd.append(module.params["src"])

    # --workingDir
    if module.params["working_dir"]:
        cmd.append("--workingDir")
        cmd.append(module.params["working_dir"])

    return cmd