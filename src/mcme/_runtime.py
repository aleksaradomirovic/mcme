# Copyright (C) 2026  Aleksa Radomirovic
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import pathlib
import shutil

from ._instance import *

class Runtime:
    def __init__(self, java_exe):
        self.__java_exe = pathlib.Path(java_exe)

    def exec(self, instance: Instance):
        with open(instance.directory() / "eula.txt", "w") as f:
            f.write("eula=true")

        exe = pathlib.Path(shutil.which(self.__java_exe))
        cmd = [ exe, "-jar", instance.loader().jarfile() ] + instance.loader().cmd(instance)
        cwd = instance.directory()

        os.chdir(cwd)
        os.execv(exe, cmd)
