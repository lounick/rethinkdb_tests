import rethinkdb as r
from tornado import ioloop, gen
from tornado.concurrent import Future, chain_future
import functools
import time

r.set_loop_type("tornado")
connection = r.connect(host='localhost', port=28015)


@gen.coroutine
def single_row(connection_future):
    # Wait for the connection to be ready
    connection = yield connection_future
    # Insert some data
    yield r.table('test').insert([{"id": 0}, {"id": 1}, {"id": 2}]).run(connection)
    # Print the first row in the table
    row = yield r.table('test').get(0).run(connection)
    print(row)


@gen.coroutine
def print_cfeed_data(connection_future, table, feeds_ready):
    connection = yield connection_future
    feed = yield r.table(table).changes().run(connection)
    feeds_ready[table].set_result(True)
    while (yield feed.fetch_next()):
        item = yield feed.next()
        print(item)


# def init():
#     r.set_loop_type("tornado")
#     connection = r.connect(host='localhost', port=28015)
#     return connection

@gen.coroutine
def main():
    print("Hello rethink!")
    feeds_ready = {'tv_shows':Future()}
    ioloop.IOLoop.current().add_callback(print_cfeed_data, connection, 'tv_shows', feeds_ready)
    yield feeds_ready
    while(True):
        conn = yield connection
        # yield r.table('test').insert([{"id": 0}, {"id": 1}, {"id": 2}]).run(connection)
        yield r.table('tv_shows').insert([{ "name": 'Star Trek TNG', "episodes": 178 }]).run(conn)
        yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 10)
        print("Hello again!")






if __name__ == "__main__":
    # main()
    ioloop.IOLoop.current().run_sync(main)
    ioloop.IOLoop.current().start()

#------------------------------------------------------------------------------------------------

# Example of non-blocking sleep.
# import time
# from tornado.ioloop import IOLoop
# from tornado import gen
#
#
# @gen.engine
# def f():
#     print 'sleeping'
#     yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)
#     print 'awake!'
#
#
# if __name__ == "__main__":
#     # Note that now code is executed "concurrently"
#     IOLoop.instance().add_callback(f)
#     IOLoop.instance().add_callback(f)
#     IOLoop.instance().start()