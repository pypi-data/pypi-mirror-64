Django shadow tasks is simple lightweight library for running 
functions as tasks in background.


```bash
pip install django-shadow-tasks
```

Add `shadow_tasks` to `INSTALLED_APPS`


```python

from shadow_tasks.publishing import shadow_task


@shadow_task
def add(a, b):
    c = a + b
    logger.info(f'{a} + {b} = {c}')
```

Run task in background

```python
add.delay()
```

Run background worker to execute tasks from "default" queue. 
Shutdown after 10 tasks

```bash
shadow-tasks-consumer --queue default --tasklimit 10
```

## Build package
````
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```

install from local archive
```
pip install ../django-shadow-tasks/dist/django-shadow-tasks-0.0.6.tar.gz
```