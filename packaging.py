#!/usr/bin/env python
import sys
import os
import tempfile

if len(sys.argv) != 2:
    print('./packaging.py file')
    sys.exit(1)

name = sys.argv[1]
f = open(name, "rb")
data = '\\x' + '\\x'.join(f.read().hex(' ').split())

cfile = """
#include <stdio.h>
#include <stdlib.h>

char data[] = "{}";
int len = {};

int main() {{
    FILE *f = fopen("{}", "wb");
    fwrite(data, sizeof(char), sizeof(data), f);
    fclose(f);
    return 0;
}}
""".format(data, len(data), name)

ctmp = tempfile.NamedTemporaryFile(suffix = '.c', mode = 'w+')
ctmp.write(cfile)

print(ctmp.name)


os.system('cat {}'.format(ctmp.name))
os.system('gcc {} -o ./packaged'.format(ctmp.name))

ctmp.close()
