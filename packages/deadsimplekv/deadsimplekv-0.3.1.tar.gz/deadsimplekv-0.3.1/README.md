<h1 align='center'>DeadSimpleKV</h1>

[![Build Status](https://travis-ci.org/beardog108/DeadSimpleKV.svg?branch=master)](https://travis-ci.org/beardog108/DeadSimpleKV)

As the name implies, this is merely a simple key-value store for Python.

Not counting comments and tests, it is less than 100 lines of code.

It doesn't do anything crazy. It just takes json serializable data and stores it to disk.

You can control when and where to read/write, and that's it.

No bloat, only 6 public methods.

## Usage

### Install: 

`python3 setup.py install`

### Create the KV instance:

~~~
# If the file already exists, it will load the json data from it
kv = deadsimplekv.DeadSimpleKV('/path/to/file')
~~~

You can specify how often to refresh and flush to file by passing `flush_seconds` and `refresh_seconds` respectively.

### Get and set values:

~~~
# Automatically reads/writes to disk every time unless no file was specified.
# Set flush_seconds or refresh_seconds to None to disable automatic read/write.
# Set them to >0 values to automatically read/write if time has elapsed. 
kv.put('my_key', True)
kv.get('my_key') # returns True.
~~~

### Delete a key/value pair:

~~~
kv.delete('my_key')
~~~

***Warning:*** **Be sure to keep flush_on_exit set to true or manually flush when destroying the kv instance (such as by exiting your program) to avoid losing data.**

***Warning:*** **flush_on_exit should be set to false when using the same file from multiple threads or processes, otherwise you will lose data.**
