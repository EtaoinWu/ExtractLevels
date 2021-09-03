import os
from lxml import etree
import re
from copy import deepcopy
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("lss_file", help="The .lss file you want to extract levels from.")
parser.add_argument("output_dir", help="The directory you want to save the individual level splits.")
parser.add_argument("-l", "--level", help="The level you want to extract. If not specified, would extract all the levels instead.")
args = parser.parse_args()

original_root = etree.parse(args.lss_file, etree.XMLParser(strip_cdata=False)).getroot()
dup_root = deepcopy(original_root)
dup_segments = dup_root.find("Segments")
dup_segments.clear()

output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

name_pattern = re.compile("^\{(.+)\} ?(.*)$")
for segment in original_root.find("Segments"):
  dup_segments.append(segment)
  name = segment.find("Name").text
  regex_match = name_pattern.match(name)
  if regex_match:
    # End of a (super)split
    level_name = regex_match.group(1)
    if args.level == level_name or args.level == None:
      with (output_dir / (level_name + ".lss")).open(mode="wb") as f:
        etree.ElementTree(dup_root).write(f, xml_declaration=True, encoding='UTF-8')
      dup_segments.clear()



