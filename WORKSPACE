workspace(
    name = "net_ankiweb_ankisyncserver",
    managed_directories = {"@npm": [
        "ts/node_modules",
    ]},
)
# : load repos which will gave rules  
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
# register repo for ankisyncserver ,rules_python and  net_ankiweb_anki pylib local repo, rules_rust  
load(":repos.bzl", "register_repos")
register_repos()


#: setup rust and python toolchain 
# set deps' dep 
load("@bazel_skylib//lib:versions.bzl", "versions")
versions.check(minimum_bazel_version = "3.7.0")
load("@io_bazel_rules_rust//rust:repositories.bzl", "rust_repositories")
rust_repositories(
        edition = "2018",
        # use_worker = True,
        #version = "1.47.0",
        version = "nightly",
	iso_date = "2020-10-24",
    )

load("@io_bazel_rules_rust//:workspace.bzl", "bazel_version")
bazel_version(name = "io_bazel_rules_rust_bazel_version")
load("@net_ankiweb_anki//:python.bzl", "setup_local_python")
setup_local_python(name = "python")
#native.register_toolchains("@python//:python3_toolchain")
register_toolchains("@python//:python3_toolchain")


#: setup outher 

# bazel_skylib_workspace set and python version set 
# maybe put the workspace later 
# now empty op 
load(":defs.bzl", "setup_deps")
setup_deps()




# self direct deps 
load("@rules_python//python:pip.bzl", "pip_install")
# Create a central repo that knows about the dependencies needed for
# requirements.txt.
pip_install(   # or pip3_import
   name = "my_deps",
   requirements = "//:src/requirements.txt",
   # Error in path: Not a regular file: /workspaces/anki-sync-server/external/src/requirements.txt	    
   #requirements = ":src/requirements.txt",
  # requirements = "//src:requirements.txt",
   python_interpreter_target = "@python//:python",
   timeout = 600,
   #extra_pip_args = ["--no-binary","orjson"],	    

)

# : load dep's dep: pylib deps
# !!!!
# must use file label
#: have rule repo dep and data/deps  
load("@net_ankiweb_anki//:pylib_deps.bzl", "pylib_deps")

pylib_deps()
# now data did not 
# deps as pyre_deps repo 

# should be in the pylib_deps.bzl as a whole 
# ../anki/pylib_deps.bzl
load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")
protobuf_deps()
load("@net_ankiweb_anki//cargo:crates.bzl", "raze_fetch_remote_crates")
raze_fetch_remote_crates()








load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()
