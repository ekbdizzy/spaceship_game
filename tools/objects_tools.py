import os
from tools import read_controls, get_frame_size
from typing import List, Tuple


def get_object_size(frames: List[str]) -> Tuple[int, int]:
    """Return max size of object."""

    if not frames:
        return 0, 0
    object_row_size = max([get_frame_size(frame, rows_only=True) for frame in frames])
    object_column_size = max([get_frame_size(frame, columns_only=True) for frame in frames])
    return object_row_size, object_column_size


def read_animation_frames(path_to_frames: str) -> List[str]:
    """Get all frames for animation from folder 'path_to_frames'."""

    frames = []
    for file_name in os.listdir(path_to_frames):
        with open(os.path.join(path_to_frames, file_name)) as file_data:
            frames.append(file_data.read())
    return frames


def get_axis_position(next_axis_position: int, object_axis_size: int, canvas_axis_size: int):
    """Return value of axis_position between 1 and canvas_axis_size."""

    return min(max(next_axis_position, 1), canvas_axis_size - object_axis_size - 1)


def get_object_position(canvas,
                        current_row: int, current_column: int,
                        frames: List[str],
                        speed=1) -> Tuple[int, int]:
    """Moves object according 'read_controls' actions if object inside canvas."""

    # Шаг 18/21. Не пойму, зачем выносить это выше, если эти значения никому кроме этой функции не нужны.
    # Функция уровнем выше (rocket) не должна задумываться о том, что происходит здесь, а просто получать координаты.
    rocket_rows_direction, rocket_column_direction, _ = read_controls(canvas)

    next_row_position = current_row + rocket_rows_direction * speed
    next_column_position = current_column + rocket_column_direction * speed

    object_row_size, object_column_size = get_object_size(frames)

    # Note that canvas.getmaxyx() return a tuple: width and height of the window, not a max y and max x values.
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()

    current_row = get_axis_position(next_row_position, object_row_size, canvas_rows_size)
    current_column = get_axis_position(next_column_position, object_column_size, canvas_columns_size)

    return current_row, current_column
