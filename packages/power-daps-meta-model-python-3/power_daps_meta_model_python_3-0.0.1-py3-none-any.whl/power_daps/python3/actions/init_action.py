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

from dap_core import common
import os, sys, pathlib, shutil

from dap_core.meta_model import MetaModel


class InitAction:
  name = "init"

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    project_dir = '.'
    project_name = os.getcwd().split('/')[-1]

    self.check_that_name_does_not_have_dashes(project_name)
    self.copy_template_files_to(project_dir)
    self.rename_files(project_dir, "PROJECT_NAME", project_name)
    self.rename_files(project_dir, "PROJECT_CAMELIZED_NAME", self.camelize(project_name))
    self.setup_git(project_dir)

    return 0, ""

  def copy_template_files_to(self, destination):
    common.print_verbose("Looking for files to copy in: " + str(pathlib.Path(MetaModel(common.meta_model()).template_for_action(self.name))))
    files_to_copy = [str(p) for p in pathlib.Path(MetaModel(common.meta_model()).template_for_action(self.name)).glob("*")]
    common.print_verbose("Found " + str(len(files_to_copy)) + " files to copy.")
    command_to_run = ['/bin/cp', "-R", *files_to_copy, destination]
    common.run_command(command_to_run)

  def rename_files(self, dir, str_to_find, str_to_replace_with):
    files_to_rename = [str(p) for p in pathlib.Path(dir).glob("*" + str_to_find + "*")]
    common.print_verbose("Renaming " + " ".join(files_to_rename))
    for file_to_rename in files_to_rename:
      rename_command = ['/bin/mv', file_to_rename, file_to_rename.replace(str_to_find, str_to_replace_with)]
      common.run_command(rename_command)

    grep_files_command = [shutil.which('find'), ".", "!", "-name", '*.pyc', "!", "-path", '*target*', "!", "-path", '*/out/*', "!", "-path", '*dist*', "!", "-path", '*.git*', "-type", "f", "-exec", shutil.which("grep"), "-l", "PROJECT_NAME", '{}', ";", "-print"]
    files_to_search_and_replace_within = common.run_command(grep_files_command)[1].splitlines()

    for f in files_to_search_and_replace_within:
      sed_command = self.sed_find_and_replace_command(str_to_find, str_to_replace_with, f)
      common.run_command(sed_command)

  def sed_find_and_replace_command(self, str_to_find, str_to_replace_with, filename):
    sed_command = [shutil.which('sed'), '-i']
    if sys.platform.startswith('darwin'):
      sed_command += [""]
    sed_command += ['-e', "s/" + str_to_find + "/" + str_to_replace_with + "/g", filename]
    return sed_command


  def setup_git(self, dir):
    os.chdir(dir)

    git_init_command = ['/usr/bin/git', 'init']
    common.run_command(git_init_command)

    git_add_command = ['/usr/bin/git', 'add', '.']
    common.run_command(git_add_command)

    git_commit_command = ['/usr/bin/git', 'commit', '-m', 'Initial commit']
    common.run_command(git_commit_command)

    common.print_raw("Initialized new Python 3 application.")

    return 0, ""

  def camelize(self, s):
    return s.replace("_", " ").title().replace(" ", '')

  def check_that_name_does_not_have_dashes(self, name):
    if "-" in name:
      common.exit_with_error_message("Name " + name + " has dashes. Please use underscores as dashes cause problems in the python ecosystem")

def action():
  return InitAction()
