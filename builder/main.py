"""
    Build script for Parallax Propeller
"""

from os.path import join
from SCons.Script import ARGUMENTS, AlwaysBuild, Builder, Default, DefaultEnvironment


def BeforeUpload(target, source, env):
    upload_options = {}
    if "BOARD" in env:
        upload_options = env.BoardConfig().get("upload", {})

    # extra upload flags
    if "extra_flags" in upload_options:
        env.Append(UPLOADERFLAGS=upload_options.get("extra_flags"))

    env.AutodetectUploadPort()
    env.Append(UPLOADERFLAGS=["-p", '"$UPLOAD_PORT"'])

    if int(ARGUMENTS.get("PIOVERBOSE", 0)):
        env.Prepend(UPLOADERFLAGS=["-v"])

env = DefaultEnvironment()

env.Replace(
    AR="propeller-elf-ar",
    AS="propeller-elf-gcc",
    CC="propeller-elf-gcc",
    CXX="propeller-elf-g++",
    OBJCOPY="propeller-elf-objcopy",
    RANLIB="propeller-elf-ranlib",
    SIZETOOL="propeller-elf-size",

    #SIZEPROGREGEXP=r"^(?:\.text|\.data)\s+(\d+).*",
    #SIZEDATAREGEXP=r"^(?:\.data|\.bss)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -A -d $SOURCES',

    PROGSUFFIX=".elf"
)

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

if not env.get("PIOFRAMEWORK"):
    env.SConscript("frameworks/_bare.py", exports="env")

# The source code of "platformio-build-tool" is here
# https://github.com/platformio/platformio-core/blob/develop/platformio/builder/tools/platformio.py

#
# Target: Build executable and linkable firmware
#
target_elf = env.BuildProgram()
target_buildprog = env.Alias("buildprog", target_elf, target_elf)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload firmware
#

env.Replace(
	UPLOADER="propeller-load",
	UPLOADERFLAGS=[
		"-b", "c3",
		"-r",
        ],
	UPLOADCMD='$UPLOADER $UPLOADERFLAGS $SOURCES'
    )

upload_actions = [
	env.VerboseAction(BeforeUpload, "Looking for upload port..."),
	env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
	]

AlwaysBuild(env.Alias(["upload"], target_elf, upload_actions))

#
# Setup default targets
#

Default([target_buildprog, target_size])
