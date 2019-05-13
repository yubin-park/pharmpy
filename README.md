# pharmpy 

## Installing

Installing from the source:
```
$ git clone git@github.com:yubin-park/pharmpy.git
$ cd pharmpy
$ python setup.py develop
```

Or, simply using `pip`:
```
$ pip install pharmpy
```

## File Structure
- `pharmpy/`: The package source code is located here.
  - `data/`: The raw data files downloaded from the H-CUP website.
- `tests/`: test scripts to check the validity of the outputs.
- `LICENSE.txt`: Apache 2.0.
- `README.md`: This README file.
- `setup.py`: a set-up script.

## Code Examples
`pharmpy` is really simple to use. 
Please see some examples below.
NOTE that all functions used below have docstrings. 
If you want to see the input parameter specifications,
please type `print(<instance>.<function>.__doc__)`.

```python
TBD
```

### Warming-up Caches

- RxCUI Cache Warm-up
```python
>> from pharmpy.rxcui import RxCUIEngine
>> rce = RxCUIEngine()
>> rce.run_cache() # this takes about 2-3 hours using RxNav-in-a-Box
```
- ATC Cache Warm-up
```python
from pharmpy.atc import ATCEngine
ae = ATCEngine()
ae.run_cache() # takes about 10-20 minutes using RxNav-in-a-Box
```
- DrugInter Cache Warm-up
```python
from pharmpy.druginter import DrugInterEngine
dre = DrugInterEngine()
dre.run_cache() # takes about 2 hours using RxNav-in-a-Box
```
The caches are stored in a local drive indefinitely. 
Thus, you just need to run these warm-up scripts periodically whenever you update the RxNav-in-a-Box monthly images.

Please refer to the test scripts under the `tests/` folder if you want to see other example use cases.

## License
Apache 2.0

## Authors
Yubin Park, PhD

## References
- https://open.fda.gov/data/ndc/
- https://www.accessdata.fda.gov/cder/ndctext.zip
- https://www.fda.gov/drugs/drug-approvals-and-databases/ndc-product-file-definitions
- https://www.fda.gov/drugs/drug-approvals-and-databases/ndc-package-file-definitions





