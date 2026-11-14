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

import mcme
import mcme.fabric

class ModrinthSource(mcme.ModSource):
    def install(self, id, instance: mcme.Instance):
        version = ModrinthSource.__best_version(id, instance.loader())
        for dep in version["dependencies"]:
            pass # TODO

        for file in version["files"]:
            instance.loader().install_mod(instance, file["url"], filename=file.get("filename"))

    def __best_version(id, loader: mcme.Loader):
        loader_id = ModrinthSource.__loader_id(loader)
        game_version = loader.game_version()

        versions = mcme.get_file(f"https://api.modrinth.com/v2/project/{id}/version").json()
        return [ x for x in versions if (x["version_type"] == "release") and (x["status"] == "listed") and (game_version in x["game_versions"]) and (loader_id in x["loaders"]) ][0]

    def __loader_id(loader: mcme.Loader) -> str:
        if isinstance(loader, mcme.fabric.FabricLoader):
            return "fabric"
        else:
            raise ValueError("unrecognized loader type")
