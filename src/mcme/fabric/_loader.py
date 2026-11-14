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

import json
import pathlib
import shutil
import tempfile
import typing

import mcme

CACHE_DIR = mcme.CACHE_DIR / "fabric"

class FabricLoader(mcme.ModdedLoader):
    def __init__(self, jarfile, game_version, loader_version, installer_version):
        super().__init__(jarfile=jarfile, game_version=game_version)
        self.__loader_version = str(loader_version)
        self.__installer_version = str(installer_version)

    def export_json(self):
        return {
            "type": "fabric",
            "game_version": self.game_version(),
            "loader_version": self.loader_version(),
            "installer_version": self.installer_version(),
        }

    def cmd(self, instance: mcme.Instance):
        return [ "--nogui" ]

    def install_mod(self, instance: mcme.Instance, url, filename=None) -> pathlib.Path:
        mod_folder = self.__mod_folder(instance)
        if filename is None:
            filename = tempfile.mkstemp(dir=mod_folder)
        else:
            filename = mod_folder / filename
            if not filename.resolve().is_relative_to(mod_folder.resolve()):
                raise ValueError("security error: filename out of bounds")

        mod_folder.mkdir(exist_ok=True)
        r = mcme.get_file(url)
        with open(filename, "wb") as f:
            f.write(r.content)

    def remove_mods(self, instance: mcme.Instance):
        mod_folder = self.__mod_folder(instance)
        if mod_folder.exists():
            shutil.rmtree(mod_folder)

    def loader_version(self) -> str:
        return self.__loader_version

    def installer_version(self) -> str:
        return self.__installer_version

    def __mod_folder(self, instance: mcme.Instance) -> pathlib.Path:
        return instance.directory() / "mods"

    def import_json(info: dict[str, typing.Any]):
        if info["type"] != "fabric":
            raise ValueError("not a fabric loader spec")

        return FabricLoader.get_loader(info.get("game_version"), info.get("loader_version"), info.get("installer_version"))

    def get_versions():
        versions = mcme.get_file("https://meta.fabricmc.net/v2/versions").json()
        return {
            "game": [ x["version"] for x in versions["game"] if x["stable"] ],
            "loader": [ x["version"] for x in versions["loader"] if x["stable"] ],
            "installer": [ x["version"] for x in versions["installer"] if x["stable"] ]
        }

    def get_loader(game_version=None, loader_version=None, installer_version=None):
        if (game_version is None) or (loader_version is None) or (installer_version is None):
            versions = FabricLoader.get_versions()

            if game_version is None:
                game_version = versions["game"][0]
            if loader_version is None:
                loader_version = versions["loader"][0]
            if installer_version is None:
                installer_version = versions["installer"][0]

        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / f"fabric-server-{game_version}-{loader_version}-{installer_version}.jar"
        r = mcme.get_file(f"https://meta.fabricmc.net/v2/versions/loader/{game_version}/{loader_version}/{installer_version}/server/jar")
        with open(cache_file, "wb") as f:
            f.write(r.content)

        return FabricLoader(cache_file, game_version, loader_version, installer_version)
