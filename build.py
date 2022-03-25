def build(gen, env):
    if env['TGT'] != 'host' or env['BUILD'] != 'coverage':
        return

    env = env.clone()

    env['CPPFLAGS'] += [
        '-DVISIBILITY_HIDDEN=0',
        '-DCOMPILER_RT_HAS_UNAME=1',
        '-DCOMPILER_RT_HAS_FCNTL_LCK=1',
        '-D__linux__=1',
        '-D_GNU_SOURCE=1',
    ]
    env['CPPPATH'] += ['src/libs/llvmprofile/profile']

    # don't produce coverage for the library handling coverage ;)
    env.remove_flag('CFLAGS', '--coverage')
    env.remove_flag('CXXFLAGS', '--coverage')

    # shut off warnings
    env['CFLAGS'] += [
        '-fvisibility=hidden',
        '-Wno-sign-conversion',
        '-Wno-unused-parameter',
    ]

    files = [
        "GCDAProfiling.c",
        "InstrProfiling.c",
        "InstrProfilingBuffer.c",
        "InstrProfilingFile.c",
        "InstrProfilingMerge.c",
        "InstrProfilingMergeFile.c",
        "InstrProfilingNameVar.c",
        "InstrProfilingPlatformDarwin.c",
        "InstrProfilingPlatformFuchsia.c",
        "InstrProfilingPlatformLinux.c",
        "InstrProfilingPlatformOther.c",
        "InstrProfilingPlatformWindows.c",
        "InstrProfilingRuntime.cpp",
        "InstrProfilingUtil.c",
        "InstrProfilingValue.c",
        "InstrProfilingVersionVar.c",
        "InstrProfilingWriter.c",
        # These files were added in LLVM 11.
        "InstrProfilingInternal.c",
        # "InstrProfilingBiasVar.c",
    ]

    lib = env.static_lib(gen, out = 'libllvmprofile', ins = files)
    env.install(gen, env['LIBDIR'], lib)
