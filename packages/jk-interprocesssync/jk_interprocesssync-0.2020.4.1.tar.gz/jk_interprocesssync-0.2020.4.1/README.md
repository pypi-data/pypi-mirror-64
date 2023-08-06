jk_interprocesssync
==========

Introduction
------------

This python module provides simple synchronization and data transfer mechanisms for processes residing on the same host.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
* [pypi.python.org](https://pypi.python.org/pypi/jk_interprocesssync)

Why this module?
----------------

Sometimes it is necessary to implement a single application as a set of multiple processes that cooperate on a specific problem or task. If that is the case these processes need to interoperate.

Limitations of this module
--------------------------

At this point, the implementation of this module is not very sophisticated. It is based on frequent polls of files or directory contents.

This approach is sufficient for limited amounts of data though. For larger amounts of data you require more sophisticated approaches. These might be added to this module at some point in the future, but for today this more simple approach exists.

This approach is somehow limited and costs a little bit of performance. In addition it is not extremely fast. Nevertheless if you use a RAM disk you will be able to process up to tens of thousands of data points per second.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_interprocesssync.fs
```

### Basic concepts

Then - after importing - you need to follow this approach:

* Instantiate an object that assists in synchronization or data transfer.
* Use methods on this object for signalling, data transfer, waiting for signals or to wait for incoming data.

More about this is explained in the next sections.

Regular Events
----------------------

### Introduction

A regular event is a synchronization mechanism that has two operations:
* sender : `signal` : signal the event;
* listener : `wait` : blocks until it receives a signal; autoreset the signal;

This mechanism is implemented by `Event`.

NOTE: This implementation is to work in situations with ...
* a single sender and a single listener
* a single sender and multiple listeners

### Implement a sender

Example:

```python
evt = jk_interprocesssync.fs.Event("/my/dir/to/eventfile")

while True:
	... do something ...
	evt.signal()
```

### Implement a listener

Example:

```python
evt = jk_interprocesssync.fs.Event("/my/dir/to/eventfile")

for _ in evt.waitG():
	... do something ...
```


JSON Data Events
----------------------

### Introduction

A JSON data event is a synchronization mechanism that has two operations:
* sender : `signal` : signal the event; additionally pass data to the listener;
* listener : `wait` : blocks until it receives a signal; autoreset the signal; the data sent by the sender is returend and can be processed by the listener;

This mechanism is implemented by `JSONDataEvent`.

NOTE: This implementation is to work in situations with ...
* a single sender and a single listener

### Implement a sender

Example:

```python
evt = jk_interprocesssync.fs.JSONDataEvent("/my/dir/to/ramdisk/eventfile")

while True:
	... do something ...
	evt.signal(... data ...)
```

### Implement a listener

Example:

```python
evt = jk_interprocesssync.fs.JSONDataEvent("/my/dir/to/ramdisk/eventfile")

for data in evt.waitG():
	... do something using the data...
```


JSON Data Queue
----------------------

### Introduction

A JSON data event is a synchronization mechanism that has two operations:
* sender : `put` : put data into the queue; notifies the listener;
* listener : `get` : blocks until it receives data; automatically remove the data from the queue;

This mechanism is implemented by `JSONDataQueue`.

NOTE: This implementation is to work in situations with ...
* a single sender and a single listener
* a single sender and a multiple listeners
* a multiple senders and a single listener
* a multiple senders and multiple listeners

### Implement a sender

Example:

```python
queue = jk_interprocesssync.fs.JSONDataQueue("/my/dir/to/ramdisk/queuedir")

while True:
	... do something ...
	queue.put(... data ...)
```

### Implement a listener

Example:

```python
queue = jk_interprocesssync.fs.JSONDataQueue("/my/dir/to/ramdisk/queuedir")

for data in queue.getG():
	... do something using the data...
```


Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



