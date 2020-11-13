
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
load("@bazel_skylib//lib:versions.bzl", "versions")
#load("@pylib//:python.bzl", "setup_local_python")
load("@net_ankiweb_anki//:python.bzl", "setup_local_python")
load("@rules_python//python:pip.bzl", "pip_install")

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")
ankisync_version = "2.2.0"

# self deps def
def setup_deps():
    #pass 
    protobuf_deps()
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
