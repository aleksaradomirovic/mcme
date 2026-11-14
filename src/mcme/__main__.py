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

import argparse
import pathlib
import json

import mcme

if __name__ == "__main__":
    parser = argparse.ArgumentParser("mcme")

    parser.add_argument("DIRECTORY", nargs="?", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--config", help="specify mcme.json config file (defaults to DIRECTORY/mcme.json)", type=pathlib.Path, required=False)

    args = parser.parse_args()

    directory = args.DIRECTORY
    config_file = args.config if args.config is not None else directory / "mcme.json"

    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    config_loader = config.get("loader", { "type": "fabric" })
    match config_loader["type"]:
        case "fabric":
            import mcme.fabric
            loader = mcme.fabric.FabricLoader.import_json(config_loader)
        case _:
            raise ValueError("unknown loader type")

    directory.mkdir(parents=True, exist_ok=True)
    instance = mcme.Instance(directory, loader)

    if isinstance(loader, mcme.ModdedLoader):
        loader.remove_mods(instance)

    config_mods = config.get("mods", [])
    for mod in config_mods:
        match mod["source"]:
            case "modrinth":
                import mcme.modrinth
                mcme.modrinth.ModrinthSource().install(mod["id"], instance)
            case _:
                raise ValueError("unknown mod source")

    runtime = mcme.Runtime("java")
    runtime.exec(instance)
