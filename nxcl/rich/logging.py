from __future__ import annotations
from typing import Any, Union, Optional, Iterable, List

import os
import logging
from logging import LogRecord

from rich.logging import RichHandler as _RichHandler
from rich.highlighter import Highlighter
from rich.console import Console, ConsoleRenderable
from rich.traceback import Traceback
from rich.containers import Renderables


ModuleType = Any
FormatTimeCallable = Any


__all__ = [
    "RichHandler",
    "RichFileHandler",
]


class RichHandler(_RichHandler):
    def __init__(
        self,
        level: Union[int, str] = logging.NOTSET,
        console: Optional[Console] = None,
        *,
        show_time: bool = False,
        omit_repeated_times: bool = True,
        show_level: bool = False,
        show_path: bool = False,
        enable_link_path: bool = True,
        highlighter: Optional[Highlighter] = None,
        markup: bool = True,
        rich_tracebacks: bool = True,
        tracebacks_width: Optional[int] = None,
        tracebacks_extra_lines: int = 3,
        tracebacks_theme: Optional[str] = None,
        tracebacks_word_wrap: bool = True,
        tracebacks_show_locals: bool = False,
        tracebacks_suppress: Iterable[Union[str, ModuleType]] = (),
        locals_max_length: int = 10,
        locals_max_string: int = 80,
        log_time_format: Union[str, FormatTimeCallable] = "[%x %X]",
        keywords: Optional[List[str]] = None,
    ) -> None:
        super().__init__(
            level=level,
            console=console,
            show_time=show_time,
            omit_repeated_times=omit_repeated_times,
            show_level=show_level,
            show_path=show_path,
            enable_link_path=enable_link_path,
            highlighter=highlighter,
            markup=markup,
            rich_tracebacks=rich_tracebacks,
            tracebacks_width=tracebacks_width,
            tracebacks_extra_lines=tracebacks_extra_lines,
            tracebacks_theme=tracebacks_theme,
            tracebacks_word_wrap=tracebacks_word_wrap,
            tracebacks_show_locals=tracebacks_show_locals,
            tracebacks_suppress=tracebacks_suppress,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            log_time_format=log_time_format,
            keywords=keywords,
        )

    def render(
        self,
        *,
        record: LogRecord,
        traceback: Optional[Traceback],
        message_renderable: ConsoleRenderable,
    ) -> ConsoleRenderable:

        log_renderable = Renderables([message_renderable] if not traceback else [message_renderable, traceback])
        return log_renderable



class RichFileHandler(RichHandler):
    def __init__(
        self,
        filename,
        mode: str = "a",
        encoding = None,
        errors = None,
        level: Union[int, str] = logging.NOTSET,
        *,
        width: int = 200,
        show_time: bool = False,
        omit_repeated_times: bool = False,
        show_level: bool = False,
        show_path: bool = False,
        enable_link_path: bool = True,
        highlighter: Optional[Highlighter] = None,
        markup: bool = True,
        rich_tracebacks: bool = True,
        tracebacks_width: Optional[int] = 120,
        tracebacks_extra_lines: int = 3,
        tracebacks_theme: Optional[str] = None,
        tracebacks_word_wrap: bool = True,
        tracebacks_show_locals: bool = False,
        tracebacks_suppress: Iterable[Union[str, ModuleType]] = (),
        locals_max_length: int = 10,
        locals_max_string: int = 80,
        log_time_format: Union[str, FormatTimeCallable] = "[%x %X]",
        keywords: Optional[List[str]] = None,
    ) -> None:
        filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors

        self.stream = open(self.baseFilename, self.mode, encoding=self.encoding, errors=self.errors)
        self.console = Console(
            file=self.stream,
            width=width,
            markup=markup,
            log_time=show_time,
            log_path=show_path,
            log_time_format=log_time_format,
            highlight=highlighter,
        )

        super().__init__(
            console=self.console,
            level=level,
            show_time=show_time,
            omit_repeated_times=omit_repeated_times,
            show_level=show_level,
            show_path=show_path,
            enable_link_path=enable_link_path,
            highlighter=highlighter,
            markup=markup,
            rich_tracebacks=rich_tracebacks,
            tracebacks_width=tracebacks_width,
            tracebacks_extra_lines=tracebacks_extra_lines,
            tracebacks_theme=tracebacks_theme,
            tracebacks_word_wrap=tracebacks_word_wrap,
            tracebacks_show_locals=tracebacks_show_locals,
            tracebacks_suppress=tracebacks_suppress,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            log_time_format=log_time_format,
            keywords=keywords,
        )

    def close(self):
        self.acquire()
        try:
            try:
                if self.stream:
                    try:
                        self.flush()
                    finally:
                        stream = self.stream
                        self.stream = None
                        if hasattr(stream, "close"):
                            stream.close()
            finally:
                super().close()
        finally:
            self.release()
