from ..types.methods import Method
from ..types.events import Event
from ..types import objects
from ..utils import logger
from ..utils import sub_string

from . import server
from ._status import LoggerLevel

from vkbottle import User
from vbml import Patcher

import asyncio
import typing
import sys


class Dispatcher:

    def __init__(
            self,
            secret: str,
            token: str,
            user_id: typing.Union[str, int],
            longpoll: bool = False,
            debug: typing.Union[str, bool] = True,
            log_to_path: typing.Union[str, bool] = None,
            *,
            loop: asyncio.AbstractEventLoop = None
    ):
        self.__loop = loop if loop else asyncio.get_event_loop()
        self.__secret: str = secret
        self.__debug: bool = debug
        self.__user_id: int = int(user_id)
        self.__api: User = User(token=token, debug=False)
        self.__patcher: Patcher = Patcher()

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        if longpoll:
            self.__loop.create_task(self.__api.run())

        self.logger = LoggerLevel(debug)
        self.event: Event = Event()

        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<level>[<blue>IrisPY</blue>] {message}</level> <white>[TIME {time:HH:MM:ss}]</white>",
            filter=self.logger,
            level=0
        )
        logger.level("INFO", color="<white>")
        logger.level("ERROR", color="<red>")
        if log_to_path:
            logger.add(
                "log_{time}.log" if log_to_path is True else log_to_path,
                rotation="100 MB",
            )

        logger.debug("Initialized dispatcher with SECRET: <{}> USER_ID: <{}>".format(
            secret, user_id
        ))

    async def process_event(self, event: dict):
        """ Функция, отвечающая за обработку эвента.
        :param event: -> dict
        :return: -> None
        """
        _event = await self.get_event_type(event)
        for handler in self.event.handlers:
            if handler.event_type.value == _event.method:
                try:
                    await handler.notify_handler(_event)
                    logger.info("-> NEW EVENT {} FROM CHAT {}".format(
                        _event.method, _event.object.chat
                    ))
                except Exception as e:
                    logger.exception(f"Error in handler: {e}")

    async def process_self_event(self, event: dict):
        """ Обработка эвентов: "sendSignal", "SendMySignal".
        :return:
        """
        _event = await self.get_event_type(event)
        for handler in self.event.event_handlers:
            if handler.event_type.value == _event.method:
                try:
                    await self.validation(
                        func=handler.handler,
                        event=_event,
                        text=sub_string(_event.message.text),
                        patterns=handler.patterns
                    )
                    logger.info(
                        "-> NEW EVENT {} FROM CHAT {}".format(
                            _event.method, _event.object.chat
                        ))
                except Exception as e:
                    logger.exception(f"Error in handler: {e}")

    async def process_events(self, events: typing.List[dict]):
        for event in events:
            if event["method"] not in ("sendMySignal", "sendSignal"):
                self.__loop.create_task(self.process_event(event))
            else:
                self.__loop.create_task(self.process_self_event(event))

    async def validation(
            self,
            func: typing.Callable,
            event: Method,
            text: str,
            patterns
    ):
        kwargs = {}
        for i in patterns:
            result = self.__patcher.check(text, i)
            if result == {}:
                return await func(event)
            if result:
                kwargs.update(**result)
        logger.debug(f"Validation's result: {kwargs}")
        if kwargs != {}:
            return await func(event, **kwargs)

    @property
    def api(self):
        return self.__api.api

    @property
    def on(self):
        return self.__api.on

    @property
    def loop(self):
        return self.__loop

    @property
    def eee(self):
        return "We love you <3"

    def run_app(self, host: str = "0.0.0.0", port: int = 8080, path: str = "/"):
        """
        :param host: IP адресс, где будет запущен сервер: Пример: "127.0.0.1"
        :param port: Порт, на котором будет запущен сервер: Пример 8000
        :param path: Путь, куда Ирис будет отсылать POST запросы: Пример "/bot"
        :return: -> None
        """
        app = server.get_app(self, self.__secret, self.__user_id)
        logger.info("Handling successfully started. Press Ctrl+C to stop it")
        server.run_app(app, host, port, path)

    @staticmethod
    async def get_event_type(event: dict):
        """ What the bullshit I made...
        :param event: -> dict
        :return: object
        """
        event_type = Method(event["method"])
        ev = None
        if event_type is Method.PING:
            ev = objects.Ping(**event)

        if event_type is Method.BIND_CHAT:
            ev = objects.BindChat(**event)

        if event_type is Method.BAN_EXPIRED:
            ev = objects.BanExpired(**event)

        if event_type is Method.ADD_USER:
            ev = objects.AddUser(**event)

        if event_type is Method.IGNORE_MESSAGES:
            ev = objects.IgnoreMessages(**event)

        if event_type is Method.SUBSCRIBE_SIGNALS:
            ev = objects.SubscribeSignals(**event)

        if event_type is Method.DELETE_MESSAGES:
            ev = objects.DeleteMessages(**event)

        if event_type is Method.DELETE_MESSAGES_FROM_USER:
            ev = objects.DeleteMessagesFromUser(**event)

        if event_type is Method.PRINT_BOOKMARK:
            ev = objects.PrintBookmark(**event)

        if event_type is Method.FORBIDDEN_LINKS:
            ev = objects.ForbiddenLinks(**event)

        if event_type is Method.SEND_SIGNAL:
            ev = objects.SendSignal(**event)

        if event_type is Method.SEND_MY_SIGNAL:
            ev = objects.SendSignal(**event)

        if event_type is Method.HIRE_API:
            ev = objects.HireApi(**event)

        if event_type is Method.BAN_GET_REASON:
            ev = objects.BanGetReason(**event)

        if event_type is Method.TO_GROUP:
            ev = objects.ToGroup(**event)

        return ev
