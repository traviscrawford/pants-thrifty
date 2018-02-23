java_library(
    dependencies=[
        'src/main/thrift:thrifty',
    ],
    sources=globs('*.java'),
)

jvm_binary(
    name='bin',
    dependencies=[':thrifty'],
    main='org.pantsbuild.contrib.thrifty.ThriftyDistance',
)
