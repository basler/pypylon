import re

# extract the relevant type information from the generated modules
# run

type_def_re = re.compile("(#define SWIGTYPE_p_.*)")
method_def_re = re.compile("(\s*\{\s*\(char\s*\*\)\".*)")

results = []

for f in ("../generated/genicam_wrap.cpp", "../generated/pylon_wrap.cpp"):
    for l in open(f).readlines():
        l = l.rstrip("\n")
        m = type_def_re.match(l)
        if m:
            results.append(l)
        m = method_def_re.match(l)
        if m:
            results.append(l)

results.sort()

with open("reference_types.txt", "w") as fp:
    for r in results:
        fp.write(r)
        fp.write("\n")
