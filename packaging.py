#!/usr/bin/env python
import sys
import os
import tempfile

if len(sys.argv) < 2:
    print('./packaging.py file')
    print('./packaging.py file1 file2 file3 ...')
    sys.exit(1)

# Add header
cfile = """
#include <stdio.h>
#include <stdlib.h>
"""

# Add data
count = 0
for name in sys.argv[1:]:
    print(name)
    f = open(name, "rb")
    data = '\\x' + '\\x'.join(f.read().hex(' ').split())
    cfile += """
    char data_{}[] = "{}";
    char name_{}[] = "{}";
    """.format(count, data, count, name)
    count += 1


# extract
cfile += """
int main() {
    FILE *f;
"""

for i in range(count):
    cfile += """
        f = fopen(name_{}, "wb");
        fwrite(data_{}, sizeof(char), sizeof(data_{}), f);
        fclose(f);
    """.format(i, i, i)

cfile += """
    return 0;
}
"""

# compiling self extractor
ctmp = tempfile.NamedTemporaryFile(suffix = '.c', mode = 'w+')
ctmp.write(cfile)

print(ctmp.name)
print(cfile)

ctmp.flush()
os.system('gcc {} -o ./packaged'.format(ctmp.name))

ctmp.close()
