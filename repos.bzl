
"""
Dependencies required to build Ankisyncserver.
"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository", "new_git_repository")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
def register_repos():
    "Register required dependency repos."

    # bazel
    ##########

    maybe(
        http_archive,
        name = "bazel_skylib",
        sha256 = "97e70364e9249702246c0e9444bccdc4b847bed1eb03c5a3ece4f83dfe6abc44",
        urls = [
            "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
            "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
        ],
    )
    maybe(
        git_repository,
        name = "toolchains",
	commit = "036eb1bee43572d9d20f3b3d5dedb322bf1f2805",
        remote = "https://github.com/cecini/toolchains.git",
	#shallow_since = "1608361362 +0000"
    )

    maybe(
        git_repository,
        name = "rules_python",
        commit = "3927c9bce90f629eb5ab08bbc99a3d3bda1d95c0",
        remote = "https://github.com/ankitects/rules_python",
        shallow_since = "1604408056 +1000",
    )

    # native.local_repository(
    #     name = "rules_python",
    #     path = "../rules_python",
    # )


    # anki's dep, in anki repo
    # should add maybe  
    native.local_repository(
        #name = "pylib",
	name = "net_ankiweb_anki",
        path = "/workspaces/anki",
	# can under path 
    )
    #maybe(
    #    native.local_repository,
   # 	name = "orjson_repo",
    #    path = "/workspaces/orjson",
    #)
    maybe(
        git_repository,
        name = "orjson_repo",
	commit = "2ed8462dc28fbb3929a11374af205d71b8d82faf",
        remote = "https://github.com/cecini/orjson",
    )

   # git_repository(
   #     name = "orjson",
  #name = "orjson_repo",
#	#commit = "9ce98428a2a11211eab61b5c4290f07007f9dede",
#	#commit = "3fc66b8592a999398c802186d51d2c23c540c08a",
#	#commit = "c64e0ab3b2d65c74f3ddc6d124ebd9409c48379a",
#	#commit = "ab680e3083e5c897ab91c01dc4400653cb086b24",
#	#commit = "db9e4091123ccc1a559540e33066c2d3a6d49705",
#	commit = "725f27efd50616be5bb0874d01827a0c2d1541cc",
#	remote = "https://github.com/cecini/orjson.git",
#        #shallow_since = "1604550071 +1000",
#    )

    # transistive depend
  #  maybe(
  #      native.local_repository,
#	name = "rules_pyo3_repo",
 #       path = "/workspaces/rules_pyo3",
  #  )
   # # ne need, this repo have pure python code  
   # maybe(
   #     git_repository,
   #     name = "io_bazel_rules_rust",
   #     commit = "504cde54248f518d5c98eb9f1e8db3546904ecb2",
   #     remote = "https://github.com/ankitects/rules_rust",
   #     shallow_since = "1606199575 +1000",
   # )
