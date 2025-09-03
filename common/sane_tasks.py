import traceback
import asyncio


all_tasks = [] # kinda like threading.all_threads()


def _handle_errors(task):
	try:
		exc = task.exception() # Also marks that the exception has been handled
		if exc: traceback.print_exception(type(exc), exc, exc.__traceback__)
	except asyncio.exceptions.CancelledError:
		pass


def _task_done(task):
	all_tasks.remove(task)
	_handle_errors(task)


def spawn(awaitable):
    """Spawn an awaitable as a stand-alone task"""
    task = asyncio.create_task(awaitable)
    all_tasks.append(task)
    task.add_done_callback(_task_done)
    return task  
