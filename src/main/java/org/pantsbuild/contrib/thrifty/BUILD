java_library(
    dependencies=[
        'src/main/thrift/org/pantsbuild/contrib/thrifty/client',
    ],
    sources=globs('*.java'),
)

jvm_binary(
    name='bin',
    dependencies=[':thrifty'],
    main='org.pantsbuild.contrib.thrifty.ThriftyExample',
)
