Milestone 1
^^^^^^^^^^^^

* :func:`.BaseField.clean` and :func:`.BaseModel.clean` -> :func:`.clean`, :func:`.delete` separation
* :func:`.RStore.remove_model` added
* :func:`.RUnit.remove` session integration
* :class:`.rset` session integration
* :func:`.rhahs.incr` added
* :func:`.rzlist.set` removed, use :func:`.rzlist.add`
* :class:`.rzlist` session integration
* :class:`.RSession` refactoring
* :class:`.Cursor` cleaning unnecessary function
* :func:`.rhash.__contains__` use :func:`redis.hexists`
* Removed :func:`.rhash.all`, use :func:`.rhash.data`
* Removed :func:`.BaseModel.fields_data`, :func:`.BaseModel.process_data`. :func:`.BaseModel.data` uses :func:`.FieldIter.data`
* Correct typing :func:`.rlist.range` and :func:`.rlist.pop` by :func:`.rlist.process_result` and :func:`.rlist.typer`
* Removed dublicated :func:`.rlist.data`, use :func:`.rlist.range`