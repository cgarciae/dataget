from collections import namedtuple
import asyncio
import sys

DONE = object()

Stream = namedtuple("Stream", "coroutine queue")


class TaskPool(object):

    def __init__(self, limit = 0):
        self._limit = limit
        self._tasks = []

    def filter_tasks(self):
        self._tasks = [ task for task in self._tasks if not task.done() ]

    async def join(self):
        self.filter_tasks()

        if len(self._tasks) > 0:
            await asyncio.wait(self._tasks)
        

    async def put(self, coro):
        self.filter_tasks()

        # wait until space is available
        while self._limit > 0 and len(self._tasks) >= self._limit:
            await asyncio.sleep(0)

            self.filter_tasks()

        
        task = asyncio.ensure_future(coro)
        self._tasks.append(task)


    async def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc, tb):
        return self.join()
    




def active_tasks(tasks):
    return [ task for task in tasks if not task.done() ]


def f_wrapper(f, queue = None):
    async def _f_wrapper(x):

        y = f(x)

        if hasattr(y, "__await__"):
            y = await y

        if queue is not None:
            await queue.put(y)
    
    return _f_wrapper
        
        
def map(f, stream, limit = 0, queue_maxsize = 0):
    
    qout = asyncio.Queue(maxsize = queue_maxsize)
    
    async def _map(f):
        coroin = stream.coroutine
        qin = stream.queue
        coroin_task = asyncio.ensure_future(coroin)
        f = f_wrapper(f, queue = qout)

        async with TaskPool(limit = limit) as tasks:

            x = await qin.get()
            while x is not DONE:
                
                fcoro = f(x)
                await tasks.put(fcoro)

                x = await qin.get()

            await qout.put(DONE)
            await coroin_task

        
    return Stream(_map(f), qout)

def from_iterable(iterable, queue_maxsize = 0):
    qout = asyncio.Queue(maxsize=queue_maxsize)
    
    async def _from_iterable():
        
        for x in iterable:
            await qout.put(x)
            
        await qout.put(DONE)
        
    return Stream(_from_iterable(), qout)

async def each(f, stream, limit = 0):
    
    coroin = stream.coroutine
    qin = stream.queue
    coroin_task = asyncio.ensure_future(coroin)
    f = f_wrapper(f)

    async with TaskPool(limit = limit) as tasks:

        x = await qin.get()
        while x is not DONE:
            
            fcoro = f(x)
            await tasks.put(fcoro)

            x = await qin.get()

        await coroin_task


def run(stream):
    return stream.coroutine



if __name__ == '__main__':
    import os
    import aiohttp
    import aiofiles


    def download_file(path):
        async def do_download_file(url):
            
            filename = os.path.basename(url)
            filepath = os.path.join(path, filename)

            print(f"Downloading {url}")

            async with aiohttp.request("GET", url) as resp:
                context = await resp.read()

            print(f"Completed {filename}")

            async with aiofiles.open(filepath, "wb") as f:
                await f.write(context)
        
        return do_download_file

    def handle_async_exception(loop, ctx):
        loop.stop()
        raise Exception(f"Exception in async task: {ctx}")

    urls = [
        "https://static.pexels.com/photos/67843/splashing-splash-aqua-water-67843.jpeg",
        "https://cdn.pixabay.com/photo/2016/10/27/22/53/heart-1776746_960_720.jpg",
        "http://www.qygjxz.com/data/out/240/4321276-wallpaper-images-download.jpg"
    ] * 1000000

    path = "/data/tmp/images"

    stream = from_iterable(urls)
    coro = each(download_file(path), stream, limit = 2)

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_async_exception)
    loop.run_until_complete(coro)