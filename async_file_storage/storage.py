import os
from sys import argv
import yaml
from aiohttp import web, ClientSession
import asyncio


class ConfigFileException(Exception):
    pass


def get_config_dict(config_file):
    with open(config_file, 'r') as stream:
        try:
            yaml_dict = yaml.load(stream)
            return yaml_dict
        except yaml.YAMLError as e:
            print(e)


class Storage():
    def __init__(self, directory, save_flag, port, nodes=()):
        self._port = port
        self._dir = directory
        self._save_flag = save_flag
        self._nodes = nodes

    async def handle_success(self, request: web.Request):
        file_name = request.match_info.get('file')
        if os.path.isfile(os.path.join(self._dir, file_name)):
            return web.Response(text="ok")
        else:
            return web.Response(status=404)

    async def download(self, node_id: int, file_name):
        data = await self.fetch("/".join([self._nodes[node_id]['url'], file_name]))
        if self._save_flag and self._nodes[node_id]['save_files']:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.write_file(os.path.join(self._dir, file_name), data))
        return data

    @staticmethod
    def write_file(file_path, data):
        with open(file_path, "w") as file:
            file.write(data)

    @staticmethod
    async def fetch(url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise FileNotFoundError

    async def success_call(self, node_id: int, file_name):
        get = "/".join([self._nodes[node_id]['url'], "success", file_name])
        if await self.fetch(get):
            return node_id

    async def get_success_nodes(self, file_name):
        futures = []
        for node_id in range(len(self._nodes)):
            futures.append(self.success_call(node_id, file_name))
        done, _ = await asyncio.wait(futures)
        success_nodes = []
        for future in done:
            if not future.exception():
                success_nodes.append(future.result())
        return success_nodes

    async def handle_file(self, request: web.Request):
        file_name = request.match_info.get('file')
        file_path = os.path.join(self._dir, file_name)
        try:
            file = open(file_path, 'r')
            loop = asyncio.get_running_loop()
            data = await loop.run_in_executor(None, file.read)
        except FileNotFoundError:
            success_nodes = await self.get_success_nodes(file_name)
            if success_nodes:
                data = await self.download(success_nodes[0], file_name)
                return web.Response(text=data)
            return web.Response(status=404)
        else:
            file.close()
            return web.Response(text=data)

    def process(self):
        app = web.Application()
        app.add_routes([web.get('/{file}', self.handle_file),
                        web.get('/success/{file}', self.handle_success)])
        web.run_app(app)


if __name__ == "__main__":
    config = ''.join(argv[1:])

    if len(argv) != 2:
        raise ConfigFileException("Wrong number of arguments")

    if not os.path.isfile(config):
        raise ConfigFileException("Config file doesn\'t exist")

    if not (config.endswith('.yaml') or config.endswith('.yml')):
        raise ConfigFileException("Wrong file extension")

    config_dict = get_config_dict(config)
    storage = Storage(**config_dict)
    storage.process()
