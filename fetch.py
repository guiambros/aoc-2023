import base
import os
import sys
import re

cwd = os.getcwd()
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)

year = int(re.search("\d{4}", cwd).group(0))
day = int(re.search("\/day(\d+)", cwd).group(1))
base.fetch_and_save(year, day)
