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
from shutil import which
from dap_core import common


class UnitTestAction:
  name = "unit_test"

  def __init__(self, source_dir="test", target_dir="target/test", classpath=".:target/production:target/test"):
    self.source_dir = source_dir
    self.target_dir = target_dir
    self.classpath = classpath

  def run(self):
    common.print_info("Running " + self.name + " action")
    cp_string = ""
    if self.classpath != "":
      cp_string = " -cp " + self.classpath + ":" + self.libs_classpath()
    else:
      cp_string = " -cp " + self.libs_classpath()

    common.run_command_in_shell('mkdir -p ' + self.target_dir)

    if not self.list_of_test_classes():
      common.print_verbose("No test classes found. Not running unit tests.")
      return 0, ""

    run_unit_test_command = " ".join([which('java'),
                             cp_string,
                             'org.junit.runner.JUnitCore'] + self.list_of_test_classes())

    exit_code, output = common.run_command_in_shell(run_unit_test_command)
    try:
      output = output.decode()
    except (UnicodeDecodeError, AttributeError):
      pass
    return exit_code, output

  def libs_classpath(self):
    libs = common.run_command_in_shell('find lib/java -type f -name "*.jar" -print')[1]
    return ":".join(libs.splitlines())

  def list_of_test_classes(self):
    test_classes = common.run_command_in_shell('find test -type f -name "*Test.java" -print')[1].splitlines()
    return [ test_class.replace("test/", "").replace(".java", "").replace("/", ".") for test_class in test_classes ]

def action():
  return UnitTestAction()
