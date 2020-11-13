
"""
Dependencies required to build Ankisyncserver.
"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository", "new_git_repository")

def register_repos():
    "Register required dependency repos."

    # bazel
    ##########

    http_archive(
        name = "bazel_skylib",
        sha256 = "97e70364e9249702246c0e9444bccdc4b847bed1eb03c5a3ece4f83dfe6abc44",
        urls = [
            "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
            "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
        ],
    )

    git_repository(
        name = "rules_python",
        commit = "3927c9bce90f629eb5ab08bbc99a3d3bda1d95c0",
        remote = "https://github.com/ankitects/rules_python",
        shallow_since = "1604408056 +1000",
    )

    git_repository(
        name = "io_bazel_rules_rust",
        commit = "a364ded42d9788144cd26b6e98d6b4038753bfa9",
        remote = "https://github.com/ankitects/rules_rust",
        shallow_since = "1604550071 +1000",
    )
    http_archive(
        name = "com_google_protobuf",
        sha256 = "465fd9367992a9b9c4fba34a549773735da200903678b81b25f367982e8df376",
        strip_prefix = "protobuf-3.13.0",
        urls = [
            "https://github.com/protocolbuffers/protobuf/releases/download/v3.13.0/protobuf-all-3.13.0.tar.gz",
        ],
    )
    native.local_repository(
        #name = "pylib",
	name = "net_ankiweb_anki",
        path = "/workspaces/anki",
	# can under path 
    )

