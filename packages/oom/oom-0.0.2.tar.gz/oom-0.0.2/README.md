# Out Of ~~Mana~~ Memory

Provides a function that keeps an eye on your RAM and stops executing of the process if you running out of memory.

### Example:
```python
from oom import exit_on_out_of_ram

one_gigabyte = 1 << 30
exit_on_out_of_ram(one_gigabyte)

# explode your RAM
extremely_big_number = 1 << 9999999
_ = [i for i in range(extremely_big_number)]
```