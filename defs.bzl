
load("@bazel_skylib//lib:versions.bzl", "versions")
#load("@pylib//:python.bzl", "setup_local_python")
load("@net_ankiweb_anki//:python.bzl", "setup_local_python")
load("@rules_python//python:pip.bzl", "pip_install")

#load("@io_bazel_rules_rust//rust:repositories.bzl", "rust_repositories")
#load("@io_bazel_rules_rust//:workspace.bzl", "bazel_version")

# load("@net_ankiweb_anki//:pylib_deps.bzl", "pylib_deps")
load("@net_ankiweb_anki//:pylib_defs.bzl", pylib_setup_deps = "setup_deps")

#load("@orjson_repo//:orjson_deps.bzl", "orjson_deps")
load("@orjson_repo//:orjson_defs.bzl", orjson_setup_deps= "setup_deps")

#load("@rules_pyo3_repo//cargo:crates.bzl", "rules_pyo3_fetch_remote_crates")
#load("@orjson_repo//cargo:crates.bzl", orjson_fetch_remote_crates = "raze_fetch_remote_crates")
#load("@net_ankiweb_anki//cargo:crates.bzl", anki_fetch_remote_crates = "raze_fetch_remote_crates")

load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
ankisync_version = "2.2.0"

# self deps def
def setup_deps():
    # no need access internet 
    #versions.check(minimum_bazel_version = "3.7.0")

    # no rust local repo 
    #rust_repositories(
    #        edition = "2018",
    #        # use_worker = True,
    #        #version = "1.47.0",
    #        version = "nightly",
    #	    iso_date = "2020-10-24",
    #)
    #bazel_version(name = "io_bazel_rules_rust_bazel_version")

    #load("@net_ankiweb_anki//:python.bzl", "setup_local_python")
    # we need setup my dep first ,so need this .
    setup_local_python(name = "python")
    native.register_toolchains("@python//:python3_toolchain")
    #register_toolchains("@python//:python3_toolchain")


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
    
    # from anki repo 
    # protobuf_deps()

    # protobuf dep should put in the pylib_deps 
#    pylib_deps()

   # orjson_deps()
    # should load orjson_defs??
    orjson_setup_deps()
    #rules_pyo3_fetch_remote_crates()

    #orjson_fetch_remote_crates()


    pylib_setup_deps()
    
    # should in the pylib defs pylib_setup_deps()
    #anki_fetch_remote_crates()

    bazel_skylib_workspace()

    #pass 
    # use anki's defs, do myself's 
    # protobuf_deps()

    #bazel_skylib_workspace()

    #versions.check(minimum_bazel_version = "3.7.0")
    # use external repo 
    #setup_local_python(name = "python")

    #native.register_toolchains("@python//:python3_toolchain")

   # pip_install(   # or pip3_import
   #     name = "py_deps",
   #     requirements = "@net_ankiweb_anki//pip:requirements.txt",
   #     python_interpreter_target = "@python//:python",
   #     timeout = 600,
   #     # doc
        # 

   # )
#: setup rust and python toolchain 
# set deps' dep 



#: setup outher 

# bazel_skylib_workspace set and python version set 
# maybe put the workspace later 
# now empty op 




# self direct deps 
# Create a central repo that knows about the dependencies needed for
# requirements.txt.


# : load dep's dep: pylib deps

# should be in the pylib_deps.bzl as a whole 
# ../anki/pylib_deps.bzl


# !!!!
# must use file label
#: have rule repo dep and data/deps  

# now data did not 
# deps as pyre_deps repo 


# from above orjson import 
# the ankisync repo no need pyo3, so just belong the orjson repo.




# smallvec orjson vs anki feature diff 
# https://docs.rs/smallvec/1.4.2/smallvec/
# How isolate depend for different repo 
# how command depend for defferent repo 
# default ,if exist ,later will not import agian?
