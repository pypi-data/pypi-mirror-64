#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
# 
#  This file is part of power-daps.
# 
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, pathlib
from dap_core import common
import glob

class PackageAction():
  name = "package"

  def __init__(self):
    return

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    for dir in self.list_of_package_dirs():
      common.print_verbose("Packaging " + dir)
      os.chdir(dir)
      common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", "dist/dap"]))
      common.stop_if_failed(*common.run_command(['/usr/local/bin/python3', 'setup.py', 'sdist', 'bdist_wheel']))

    return 0, ""
    # return common.run_command([self.pyinstaller(),
    #                    "--noconfirm", "--log-level=WARN",
    #                    common.power_daps_dir() + "dap.spec"])

  def list_of_package_dirs(self):
    return [str(p.parent.absolute()) for p in pathlib.Path(".").glob("**/setup.py")]

  def pyinstaller(self):
    rc, pyinstaller_path = common.run_command(["which", "pyinstaller"])
    return pyinstaller_path.rstrip()

def action():
   return PackageAction()

