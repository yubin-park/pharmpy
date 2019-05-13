import csv
import json
import re
import os
from pkg_resources import resource_filename as rscfn

def convert_ndc(ndc, digits):
    tokens = ndc.split("-")
    if len(tokens) != 3:
        return "na"
    ndc_format = "-".join([str(len(token)) for token in tokens])
    padding = ""
    if digits == 11:
        padding = "0"
    out = "na"
    if ndc_format == "4-4-2":
        out = (padding + tokens[0] + tokens[1] + tokens[2])
    elif ndc_format == "5-3-2":
        out = (tokens[0] + padding + tokens[1] + tokens[2])
    elif ndc_format == "5-4-1":
        out = (tokens[0] + tokens[1] + padding + tokens[2])
    return out

def read_package(digits=11):
    packages = {} 
    products = read_product(digits)
    fn = rscfn(__name__, "data/package.txt")
    with open(fn, "r", encoding="ISO-8859-1") as fp:
        reader = csv.reader(fp, delimiter="\t")
        header = next(reader)
        for row in reader:
            ndc_package = row[2]
            ndc_product = row[1]
            if ndc_product in products:
                key = convert_ndc(ndc_package, digits)
                packages[key] = products[ndc_product]
                #packages[key]["ndc_org"] = ndc_package
    return packages

def read_product(digits=11):
    products = {}
    fn = rscfn(__name__, "data/product.txt")
    col_dct = {"ndc": {"cnm": "PRODUCTNDC"},
            "name_proprietary": {"cnm": "PROPRIETARYNAME"},
            "name_generic": {"cnm": "NONPROPRIETARYNAME"}, 
            "substance_lst": {"cnm": "SUBSTANCENAME"},
            "pc_lst": {"cnm": "PHARM_CLASSES"}}
    with open(fn, "r", encoding="ISO-8859-1") as fp:
        reader = csv.reader(fp, delimiter="\t")
        header = next(reader)
        for k, v in col_dct.items():
            v["idx"] = header.index(v["cnm"])
        for row in reader:
            d = {}
            for k, v in col_dct.items():
                if "_lst" in k:
                    d[k] = [x for x in row[v["idx"]].split(",") 
                            if len(x) > 0]
                else:
                    d[k] = row[v["idx"]]
            key = row[col_dct["ndc"]["idx"]]
            products[key] = d
    return products

def read_cache(fn):
    fn = rscfn(__name__, fn)
    exists = os.path.isfile(fn)
    cache = {}
    if exists:
        with open(fn, "r") as fp:
            cache = json.load(fp)
    return cache

def write_cache(cache, fn):
    fn = rscfn(__name__, fn)
    with open(fn, "w") as fp:
        json.dump(cache, fp=fp, indent=2)





