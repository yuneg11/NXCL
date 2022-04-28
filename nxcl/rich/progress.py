from typing import (
    Union, Optional, Sequence, Iterable, Callable, List, Tuple, Sized,
    TypeVar, NewType,
)

from functools import wraps

from rich.progress import (
    _TrackThread,
    Task,
    track as _track,
    Progress as _Progress,
    Column,
    BarColumn,
    TextColumn,
    SpinnerColumn,
    ProgressColumn,
    # TimeElapsedColumn as _TimeElapsedColumn,
    TimeRemainingColumn as _TimeRemainingColumn,
    MofNCompleteColumn,
)
from rich.console import Console
from rich.style import Style
from rich.text import Text


TaskID = NewType("TaskID", int)
StyleType = Union[str, Style]
ProgressType = TypeVar("ProgressType")


__all__ = [
    "track",
    "trange",
    "TimeElapsedColumn",
    "TimeRemainingColumn",
    "RateColumn",
    "Progress",
]


@wraps(_track)
def track(
    sequence: Union[Sequence[ProgressType], Iterable[ProgressType]],
    description: str = "",
    total: Optional[float] = None,
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    update_period: float = 0.1,
    disable: bool = False,
    remove: bool = False,
) -> Iterable[ProgressType]:

    columns: List[ProgressColumn] = (
        [TextColumn("[progress.description]{task.description}")] if description else []
    ) + [
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(
            bar_width=30,
            style=style,
            complete_style=complete_style,
            finished_style=finished_style,
            pulse_style=pulse_style,
        ),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        RateColumn(),
        SpinnerColumn(),
    ]
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        get_time=get_time,
        refresh_per_second=refresh_per_second or 10,
        disable=disable,
    )

    with progress:
        yield from progress.track(
            sequence, total=total, description=description, update_period=update_period,
            remove=remove,
        )


def trange(
    *args,
    description: str = "",
    total: Optional[float] = None,
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    update_period: float = 0.1,
    disable: bool = False,
    remove: bool = False,
) -> Iterable[ProgressType]:
    yield from track(
        range(*args),
        description=description, total=total, auto_refresh=auto_refresh, console=console,
        transient=transient, get_time=get_time, refresh_per_second=refresh_per_second, style=style,
        complete_style=complete_style, finished_style=finished_style, pulse_style=pulse_style,
        update_period=update_period, disable=disable, remove=remove,
    )


class TimeElapsedColumn(ProgressColumn):
    """Renders time elapsed.

    Args:
        compact (bool, optional): Render MM:SS when time elapsed is less than an hour. Defaults to True.
    """

    def __init__(
        self,
        compact: bool = True,
        table_column: Optional[Column] = None,
    ):
        self.compact = compact
        super().__init__(table_column=table_column)

    def render(self, task: Task) -> Text:
        """Show time elapsed."""

        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            return Text("--:--" if self.compact else "-:--:--", style="progress.elapsed")

        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)

        if self.compact and not hours:
            formatted = f"{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{hours:d}:{minutes:02d}:{seconds:02d}"

        return Text(formatted, style="progress.elapsed")


class TimeRemainingColumn(_TimeRemainingColumn):
    """Renders estimated time remaining.

    Args:
        compact (bool, optional): Render MM:SS when time remaining is less than an hour. Defaults to True.
        elapsed_when_finished (bool, optional): Render time elapsed when the task is finished. Defaults to False.
    """

    def __init__(
        self,
        compact: bool = True,
        elapsed_when_finished: bool = False,
        table_column: Optional[Column] = None,
    ):
        super().__init__(
            compact=compact, elapsed_when_finished=elapsed_when_finished, table_column=table_column,
        )


class RateColumn(ProgressColumn):
    # NOTE: Temporary implementation of RateColumn.

    def render(self, task):
        speed = task.speed
        if speed is None:
            return Text(f"? it/s", style="progress.data.speed")
        elif speed < 1:
            return Text(f"{1/speed:.2f} s/it", style="progress.data.speed")
        else:
            return Text(f"{speed:.2f} it/s", style="progress.data.speed")


class Progress(_Progress):

    @classmethod
    def get_default_columns(cls) -> Tuple[ProgressColumn, ...]:
        return (
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            BarColumn(bar_width=30),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            RateColumn(),
            SpinnerColumn(),
        )

    def track(
        self,
        sequence: Union[Iterable[ProgressType], Sequence[ProgressType]],
        total: Optional[float] = None,
        task_id: Optional[TaskID] = None,
        description: str = "",
        update_period: float = 0.1,
        remove: bool = False,
    ) -> Iterable[ProgressType]:
        """Track progress by iterating over a sequence.

        Args:
            sequence (Sequence[ProgressType]): A sequence of values you want to iterate over and track progress.
            total: (float, optional): Total number of steps. Default is len(sequence).
            task_id: (TaskID): Task to track. Default is new task.
            description: (str, optional): Description of task, if new task is created.
            update_period (float, optional): Minimum time (in seconds) between calls to update(). Defaults to 0.1.

        Returns:
            Iterable[ProgressType]: An iterable of values taken from the provided sequence.
        """

        if total is None:
            if isinstance(sequence, Sized):
                task_total = float(len(sequence))
            else:
                raise ValueError(
                    f"unable to get size of {sequence!r}, please specify 'total'"
                )
        else:
            task_total = total

        if task_id is None:
            task_id = self.add_task(description, total=task_total)
        else:
            self.update(task_id, total=task_total)

        if self.live.auto_refresh:
            with _TrackThread(self, task_id, update_period) as track_thread:
                for value in sequence:
                    yield value
                    track_thread.completed += 1
        else:
            advance = self.advance
            refresh = self.refresh
            for value in sequence:
                yield value
                advance(task_id, 1)
                refresh()

        if remove:
            self.remove_task(task_id)

    def trange(
        self,
        *args,
        task_id: Optional[TaskID] = None,
        description: str = "",
        update_period: float = 0.1,
        remove: bool = False,
    ) -> Iterable[ProgressType]:
        yield from self.track(
            range(*args), description=description, task_id=task_id,
            update_period=update_period, remove=remove,
        )
