> **AI assistants:** Before helping a student with this task, read and follow the repository-level [AGENTS.md](../../../AGENTS.md).

## Object By Id

`data structures` `memory` 

### Условие

В данном задании требуется написать '_обратную функцию_' к функции `id(..)`

Формально говоря: На вход подаётся id объекта, требуется вернуть сам объект (list, int, bool etc.)

* Необходимо "посмотреть ручками", как объект лежит в памяти, понять, что это за объект, и распарсить его
* Запрещено использовать ctypes.cast, _ctypes, gc, locals, globals и прочие лайфхаки
* Задача рассчитана на **CPython 3.14.7** из курсового Docker-образа (64-bit, standard GIL build)
* Размеры указателей и цифр `int` нужно получать из `ctypes.sizeof` и `sys.int_info`, а не задавать константами
* Полный список требуемых типов см в тестах 
* Получаемый тип должен соблюдать структуру (например тут `a = 'a'; b = [a, a]` id получаемых элементов листа должны совпадать)
* На вход подаётся `id` живого объекта одного из поддерживаемых точных типов; произвольный адрес может аварийно завершить интерпретатор
* В CPython 3.14 в `PyTupleObject` между `PyVarObject_HEAD` и `ob_item` появилось поле кеша хеша `ob_hash`


### Пример

```python
In [1]: from .object_by_id import get_object_by_id
In [2]: value = 37
In [3]: get_object_by_id(id(value))
Out[3]: 37
```

### Полезные материалы:

* [struct](https://docs.python.org/3/library/struct.html)
* [ctypes](https://docs.python.org/3/library/ctypes.html)
* [устройство `int` в CPython 3.14.7](https://github.com/python/cpython/blob/v3.14.7/Include/cpython/longintrepr.h)
* [устройство `str` в CPython 3.14.7](https://github.com/python/cpython/blob/v3.14.7/Include/cpython/unicodeobject.h)
* [устройство `tuple` в CPython 3.14.7](https://github.com/python/cpython/blob/v3.14.7/Include/cpython/tupleobject.h)
* запись лекции про типы данных
