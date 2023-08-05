import pandas as pd
from sequana import vcf_filter


import sys

print(sys.argv)

if len(sys.argv) <= 1:
    print("usage: vcf2csv infile")
    print("usage: vcf2csv infile mindepth")

infile = sys.argv[1]
threshold = 6
if len(sys.argv) == 3:
    print("removing all reads with depth<{}".format(threshold))
    threshold = sys.argv[2]


print("Reading VCF")
v = vcf_filter.VCF(infile).vcf.get_variants()
print("Converting to dataframe")
data = [x.resume for x in v]
df1 = pd.DataFrame(data)
df1 = df1.sort_values(by=["chr", "position"]).query("depth>@threshold")

outfile = infile.replace(".vcf", ".csv")
print("saving file in {}".format(outfile))
df1.to_csv(outfile)

