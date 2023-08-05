# ShortJob
## Download
```sh
git clone https://github.com/xxmawhu/ShortJob.git
```
## Install
```sh
python setup.py install
```
You can also install it into your local directory by
```sh
python setup.py install --user
```
## Usage
You should prepare two root script, i.e. `cut.cxx` and `fit.cxx`, then
you can make a bash file to run those two script.
* make a directory, such as jobs, then work at the jobs
```sh
mkdir jobs
cd jobs
```
* Write a py file, i.e test.py
```py
#!/usr/bin/env python
from ShortJob import MkMulJob
mk = MkMulJob.MkMulJob(["cut.cxx", "fit.cxx"])
cut_argv = [1.1, 1.2]
fit_argv = ["mass < 2.4"]
mk.Make(1, [cut_argv, fit_argv])
```
* Running test.py
```sh
python test.py
```
or
```sh
./test.py
```

After running this python file, you will get a bash script named `job_1.sh`
the content is
```sh
cd /abspath/to/ShortJob/test
cd .. 
root -l -b -q 'cut.cxx(1.1,1.2,0)'>>test/log0001.cut;
root -l -b -q 'fit.cxx("d<1")'>>test/log0001.fit;
```
## More complex example
```py
#!/usr/bin/env python
import os
from ShortJob import MkMulJob


mk = MkMulJob.MkMulJob(["run.C"])
for i in range(100):
    cutchisq = 2*i
    mk.Make(i, [(cutchisq)])
```
[How to submit those bash file?](https://github.com/xxmawhu/SmartHepSub)

