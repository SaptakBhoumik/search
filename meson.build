project('searchz', 'cpp', version: '0.1')
add_project_arguments('-std=c++17', language: 'cpp')
cpp_src=[
    'crawler/crawler.cpp'
]
gumbo_dep = dependency('gumbo')
executable(
    'crawler',
    sources: cpp_src, 
    dependencies : gumbo_dep
)