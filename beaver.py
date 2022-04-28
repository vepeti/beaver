#!/usr/bin/python3

import yaml
import jinja2
import subprocess

YAML_FILE="beaver.yml"
with open(YAML_FILE) as fp:
    dataMap=yaml.safe_load(fp)

env=jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='.'))
template=env.get_template(YAML_FILE)

config=yaml.safe_load(template.render(**dataMap))

command="rsync"

for flag in config.items():
    if flag[0] in ("src","dest","private_key","port"):
        continue

    if isinstance(flag[1], bool) and flag[1]:
        command+=" --"+flag[0]

    if isinstance(flag[1], int):
        if flag[0]=="port":
            command+=" --"+flag[0]+"="+str(flag[1])

    if (isinstance(flag[1], str) and flag[1]!=""):
        if flag[0]=="rsh":
            command+=" --"+flag[0]+"='"+flag[1]+"'"
        else:
            command+=" --"+flag[0]+"="+flag[1]

    if isinstance(flag[1], list) and len(flag[1])>0:
        if flag[0]=="exclude":
            command+=str(" --"+flag[0]+" ").join(["", *flag[1]])

command+=" "+config["src"]+" "+config["dest"]

print("Running command: "+command)

syncproc=subprocess.call(command, shell=True)
