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

import os
from dap_core import common, dependencies
import glob

class DepsAction():
  name = "deps"
  default_dependencies_file_location = common.dependencies_file_location()

  def __init__(self, dependencies_file_location = ""):
    self.set_dependencies_file_location(dependencies_file_location)
    return
 
  def run(self):
    common.print_info("Running " + self.name + " action")

    self.deps = self.load_dependencies(self.dependencies_file_location)

    for dep in self.deps.dependencies_for("default"):
      dep.install()

    return 0, ""

  def load_dependencies(self, dependencies_file_location):
    dependencies_file_contents = ""
    try:
      with open(dependencies_file_location) as f:
        dependencies_file_contents = f.read()
      f.closed
    except (OSError, IOError) as e:
      common.print_warning("No dependencies file found at " + dependencies_file_location)

    return dependencies.Dependencies(dependencies_file_contents)

  def set_dependencies_file_location(self, dependencies_file_location):
    if dependencies_file_location:
      self.dependencies_file_location = dependencies_file_location
    else:
      self.dependencies_file_location = DepsAction.default_dependencies_file_location


def action():
   return DepsAction()
