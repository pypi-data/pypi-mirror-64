"""
This package is consistent of four module, i.e. `command`, `MkJob`, `MkMulJob`,
`GetResult`.
* command Specify each fileType with one execute command, such as
> .sh -> bash
> .C -> root -l -b -q
* MkMulJob generate a massive bash scripts with input tasks
Example:
```bash
cd /home/maxx/work/GitHub/ShortJob/test
cd ..
root -l -b -q 'run.C(3.14,2.3,"a")' > test/log1.run
python test.py a b c > test/log1.test
bash run.sh a > test/log1.run
```
* MkJob generate a massive bash scripts with only one task
* GetResult pick the result of interest from the log file.

"""
from ShortJob import MkJob
from ShortJob import MkMulJob
from ShortJob import command
