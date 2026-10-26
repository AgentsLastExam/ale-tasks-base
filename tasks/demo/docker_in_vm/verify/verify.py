from ale_verify import checks, write

nested_container = checks.text_equals(
    "/home/user/output/nested-container.txt",
    "nested-container-ok\n",
)
write({"overall": nested_container["score"], "nested_container": nested_container})
