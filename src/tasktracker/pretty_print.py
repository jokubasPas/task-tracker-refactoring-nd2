
"""Pretty printing utilities for the task tracker application.

This module provides formatted output functions for displaying tasks in tables
and showing user feedback messages for various task operations.
"""

from typing import List
from .colors import Color
from .tasks import Task


def _get_column_widths(tasks: List[Task]) -> tuple:
    """Calculate table column widths."""
    return (
        max(3, max(len(str(task.index)) for task in tasks)),
        max(4, max(len(task.description) for task in tasks)),
        max(6, max(len(task.status) for task in tasks)),
        max(10, max(len(str(task.createdAt)) for task in tasks)),
        max(10, max(len(str(task.updatedAt)) for task in tasks))
    )


def _format_task_row(task: Task, widths: tuple, highlighted: bool) -> str:
    """Format a task row with optional background color."""
    values = (
        str(task.index),
        task.description,
        task.status,
        str(task.createdAt),
        str(task.updatedAt)
    )

    padded_values = [
        value.ljust(width)
        for value, width in zip(values, widths)
    ]

    if highlighted:
        cells = [
            f"{Color.BG_CYAN} {Color.BLACK}{value}"
            for value in padded_values
        ]
        return " | ".join(cells) + Color.RESET

    return " | ".join(f" {value}" for value in padded_values)


def print_table(tasks: List[Task], title: str = '') -> None:
    """Print tasks in a formatted table with optional title.

    Args:
        tasks: List of Task objects to display.
        title: Optional title displayed above the table.
    """
    if not tasks:
        print(f'{Color.RED} There is no task to display {Color.RESET}')
        return

    widths = _get_column_widths(tasks)

    headers = ('ID', 'Task', 'Status', 'Created At', 'Updated At')
    header = " | ".join(
        f" {name.ljust(width)}"
        for name, width in zip(headers, widths)
    )
    header_width = len(header)

    print('\n')

    if title:
        print('=' * header_width)
        print(f"{Color.BLUE}{title.center(header_width)}{Color.RESET}")
        print('=' * header_width)

    print(f"{Color.YELLOW}{header}{Color.RESET}")
    print('-' * header_width)

    for index, task in enumerate(tasks):
        row = _format_task_row(
            task,
            widths,
            highlighted=(index % 2 != 0)
        )
        print(row)

    print('=' * header_width)
    print('\n')


def print_by_tasks_command(command: str, **kwargs) -> None:
    """Print formatted success messages for task operations.

    Displays color-coded success messages for various task operations including
    add, delete, update, and status changes. Each message type has specific
    formatting and visual indicators.

    Args:
        command: The operation type. Valid values are 'add', 'delete', 'update', 'status'.
        **kwargs: Keyword arguments containing operation-specific data.
                 Expected to contain 'task' key with a Task object.

    Returns:
        None. Prints the formatted message directly to stdout.

    Raises:
        KeyError: If 'task' key is not found in kwargs.
        AttributeError: If the task object doesn't have required attributes.

    Example:
        >>> task = Task("Buy groceries", "todo")
        >>> print_by_tasks_command('add', task=task)

        ------------------------------
        ✓ - Your Task -> Buy groceries
          - with ID number -> 1
          - has been successfully added!
        ------------------------------
    """
    if 'task' in kwargs:
        task = kwargs['task']

        print('\n')
        # Create border based on task description length plus padding
        border_length = (len(kwargs['task'].description)) + 30
        print('-' * border_length)

        if command == 'add':
            print(f'{Color.GREEN} ✓{Color.RESET} - Your Task -> {Color.GREEN}{task.description}{Color.RESET} \n   - with ID number -> {Color.GREEN}{task.index}{Color.RESET} \n   - has been successfully added!')

        elif command == 'delete':
            print(f'{Color.RED} ✗{Color.RESET} - Your Task -> {Color.RED}{task.description}{Color.RESET} \n   - with ID number -> {Color.RED}{task.index}{Color.RESET} \n   - has been successfully Deleted!!')

        elif command == 'update':
            print(f'{Color.GREEN} ✓{Color.RESET} - The Task with the ID number -> {Color.BLUE}{task.index}{Color.RESET} \n   - has been {Color.GREEN}successfully{Color.RESET} Updated!!')

        elif command == 'status':
            print(f'{Color.GREEN} ✓{Color.RESET} - Your Task Status with ID {task.index} has been {Color.GREEN}successfully{Color.RESET} updated!!')

        print('-' * border_length)
        print('\n')
