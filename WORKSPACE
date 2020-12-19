workspace(
    name = "net_ankiweb_ankisyncserver",
    managed_directories = {"@npm": [
        "ts/node_modules",
    ]},
)
# register repo for ankisyncserver ,rules_python and  net_ankiweb_anki pylib local repo, rules_rust  
load(":repos.bzl", "register_repos")
register_repos()

load("@net_ankiweb_anki//:pylib_deps.bzl", "pylib_deps")
pylib_deps()

load("@orjson_repo//:orjson_deps.bzl", "orjson_deps")
orjson_deps()


load(":defs.bzl", "setup_deps")
setup_deps()


load(":late_deps.bzl", "setup_late_deps")
setup_late_deps()


