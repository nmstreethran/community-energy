"""Setting paths to QGIS libraries

It may be necessary to run additional commands to ensure the path to the
QGIS libraries are recognised by the Python interpreter. If
`import qgis.core` gives a `ModuleNotFoundError`, just run the following in
the Python interpreter of the active `qgis` conda environment:

exec(open("set_sys_paths.py").read())
"""

import sys
import os

if sys.platform == "win32":
    pathList = [
        os.path.join(sys.exec_prefix),
        os.path.join(sys.exec_prefix, "DLLs"),
        os.path.join(sys.exec_prefix, "lib"),
        os.path.join(sys.exec_prefix, "lib", "site-packages"),
        os.path.join(sys.exec_prefix, "Library", "bin"),
        os.path.join(sys.exec_prefix, "Library", "python"),
        os.path.join(sys.exec_prefix, "Library", "python", "plugins")
    ]
# else:
#     pathList = [
#         os.path.join(sys.exec_prefix),
#         os.path.join(sys.exec_prefix, "lib", "python3.9"),
#         os.path.join(sys.exec_prefix, "lib", "python3.9", "lib-dynload"),
#         os.path.join(sys.exec_prefix, "lib", "python3.9", "site-packages"),
#         os.path.join(sys.exec_prefix, "share", "qgis", "python"),
#         os.path.join(sys.exec_prefix, "share", "qgis", "python", "plugins")
#     ]

for p in pathList:
    sys.path.append(p)
