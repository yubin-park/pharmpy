# pharmpy 

`pharmpy` is an umbrella Python library for searching the FDA NDC directory, Established Pharmacologic Class (EPC), Anatomical Therapeutic Chemical (ATC) through RxNav, and some other APIs on RxNav.

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

A NOTE for the users who want to use RxNav functions such as ATC and Drug Interactions. For those, we strongly recommend using the [RxNav-in-a-Box](https://rxnav.nlm.nih.gov/RxNav-in-a-Box.html) rather than the RxNav REST APIs. 
The RxNav-in-a-Box is a [Docker](https://www.docker.com/) conatiner image that installs on your local machine. 
To use the image, please follow the set-up instructions, which are available inside the [downloadable zip file](https://mor.nlm.nih.gov/dnwl/auth/docker/rxnav-apis-docker.zip), and carefully read the [UMLS license agreement](https://uts.nlm.nih.gov/license.html).
If you decide to use the RxNAV REST APis, you should control the rate limit (20 calls per second) by yourself. 
This `pharmpy` module does not control the rate limit by itself.

## File Structure
- `pharmpy/`: The package source code is located here.
  - `data/`: The raw data files downloaded from [the FDA website](https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory). If you are using the RxNav functions and data, the caches of the query results will be stored in this folder as well.
  - `epc.py`: Established Pharmacologic Class (EPC) engine from the FDA website
  - `rxcui.py`: A RxNorm Concept Unique Identifier (RxCUI) module that maps from NDC to RxCUI. [Dependancy: RxNav]
  - `atc.py`: A mapping from NDCs to Level-4 Anatomical Therapeutic Chemical (ATC). [Dependency: RxNav]
  - `druginter.py`: A mapping from a list of NDCs to a potential drug-drug interactions. [Dependency: RxNav]
  - `utils.py`: A module for readings data files
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

### Using EPC
```python
>>> from pharmpy.epc import EPCEngine
>>> epe = EPCEngine()
>>> res = epe.get_epc("50090347201")
>>> import json
>>> print(json.dumps(res, indent=2))
{
  "ndc": "50090-3472",
  "name_proprietary": "JANUVIA",
  "name_generic": "sitagliptin",
  "substance_lst": [
    "SITAGLIPTIN PHOSPHATE"
  ],
  "pc_lst": [
    "Dipeptidyl Peptidase 4 Inhibitor [EPC]",
    "Dipeptidyl Peptidase 4 Inhibitors [MoA]"
  ]
}
>>>
```

### Using RxCUI
```python
>>> from pharmpy.rxcui import RxCUIEngine
>>> rce = RxCUIEngine()
>>> res = rce.get_rxcui("50090347201")
>>> print(json.dumps(res, indent=2))
"665044"
>>>
```

### Using ATC
```python
>>> from pharmpy.atc import ATCEngine
>>> ae = ATCEngine()
>>> res = ae.get_atc("50090347201")
>>> print(json.dumps(res, indent=2))
[
  {
    "id": "A10BH",
    "name": "Dipeptidyl peptidase 4 (DPP-4) inhibitors"
  }
]
>>>
```

### Using DrugInter
```python
>>> from pharmpy.druginter import DrugInterEngine
>>> dre = DrugInterEngine()
>>> res = dre.get_interactions_from_rxcui(["88014","8123"])
>>> print(json.dumps(res, indent=2))
[
  {
    "pair": [
      "8123",
      "88014"
    ],
    "desc": [
      "[ONCHigh] Triptans - monoamine oxidase (MAO) inhibitors"
    ]
  }
]
>>>
```

### Warming-up Caches

For the RxNav functions, `pharmpy` keeps cache, so that you do not need to query again for the same results. 
For most use cases, we recommend you warm up the cache before using any of the RxNav functions. 
The warm-up process goes through a comprehensive list of NDCs, and store all results into a local drive. 
The total process takes up about 6 hours, however, you would rarely need to query new results after warming up the cache.

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
- https://rxnav.nlm.nih.gov/RxNav-in-a-Box.html
- https://mor.nlm.nih.gov/pubs/pdf/2018-amia-lp-poster.pdf
- https://rxnav.nlm.nih.gov/APIsOverview.html




