#
# Default flags for bare-metal programming (without any framework layers)
# https://code.google.com/archive/p/propgcc/wikis/PropGccTightMemory.wiki
#

from SCons.Script import Import

Import("env")

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=[
    ],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-Wall",  # show warnings
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",  # place each data item in its own section
        "-mfcache"  # enable cache
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions"
    ],

    LINKFLAGS=[
        "-Os"
    ],

    LIBS=[
    ]
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])
