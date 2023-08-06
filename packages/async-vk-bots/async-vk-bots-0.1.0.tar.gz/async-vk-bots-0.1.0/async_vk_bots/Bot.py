import asyncio
import re
import json
from aiohttp import web
from api.API import API
from api.LongPoll import LongPoll


class Bot:
    bot = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if not cls.bot:
            cls.bot = super(Bot, cls).__new__(cls)
        return cls.bot

    def __init__(self, group_id, version="5.103", event_loop=None):
        self._token = ""
        self._v = version
        self._group_id = group_id
        self._commands = dict()
        self._scenarios = []
        self._confirm = ""
        if event_loop is None:
            event_loop = asyncio.get_event_loop()
        self._loop = event_loop
        self._listeners = dict()
        self._command_not_found = None
        self._listener_not_found = None
        self.api = None

    def add_command(self, regexp, func):
        self._commands[regexp] = func

    def add_scenario(self, scenario):
        if scenario not in self._scenarios:
            self._scenarios.append(scenario)

    def on(self, event: str):
        def decorator(func):
            async def wrapper(data):
                await func(data)
            self._listeners[event] = wrapper
            return wrapper
        return decorator

    async def __handler(self, request):
        try:
            if request["type"] == "confirmation":
                return self._confirm
            elif request["type"] == "message_new":
                msg = request["object"]
                for scenario in self._scenarios:
                    if await scenario.check_for_entry_point(request):
                        return "ok"
                try:
                    async def reply(message, **kwargs):
                        await self.api.send(peer_id=msg["message"]["peer_id"], message=message, **kwargs)
                    command = list(filter(lambda x: x is not None,
                                          map(lambda x: x if re.fullmatch(x, msg["message"]["text"]) else None,
                                              self._commands)))[0]
                    await self._commands[command](msg, re.findall(command, msg["message"]["text"]), reply)
                except IndexError:
                    if hasattr(self._command_not_found, "__call__"):
                        await self._command_not_found(msg)
            else:
                if request["type"] in self._listeners:
                    await self._listeners[request["type"]](request["object"])
                elif hasattr(self._listener_not_found, "__call__"):
                    await self._listener_not_found(request)
            return "ok"
        except KeyError:
            return "not vk"

    def get_web_hook(self, token, confirm_str):
        self._confirm = confirm_str
        self._token = token
        return self.__web_hook

    async def __web_hook(self, request):
        try:
            try:
                json_data = await request.json()
                return web.Response(text=await self.__handler(json_data))
            except json.JSONDecodeError:
                return web.Response(text="Not json")
        except BaseException as e:
            print(e)
            return web.Response(text="error", content_type="text/plain", status=500)

    async def __run(self, token):
        self._token = token
        self.api = API(self._token, self._v, self._loop)
        longpoll = LongPoll(self.api, self._group_id)
        async for event in longpoll.listen():
            await self.__handler(event)

    def run(self, token):
        print("Started")
        self._loop.run_until_complete(self.__run(token))


