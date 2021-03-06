from collections import defaultdict
import csv
import os
import subprocess

def count_intervals(dict, genes):
    res = defaultdict(int)
    for name in dict.keys():
        gene_list = dict[name]  # List of genes for a trait
        interval_set = set()  # Count every interval once
        for gene in genes:
            if gene in gene_list:  # If gene belongs to the trait
                # Add every corresponding interval to set
                for interval in genes[gene]:
                    interval_set.add(int(interval))
        res[name] = len(interval_set)
    return res

# Extract gene names that are in intersection
def get_overlapping_features(path_to_bed, path_to_gene_file, out_file):
    genes = defaultdict(list)  # Gene -> interval id
    subprocess.call("bedtools intersect -a {0} -b {1} -loj > {2}".format(path_to_bed, path_to_gene_file, out_file), shell=True)
    with open(out_file, 'r', newline='') as inter:  # Our result of clumping (SNPs sets)
        my_reader = csv.reader(inter, delimiter='\t')
        for row in my_reader:
            genes[row[-1]].append(row[3])
    return genes

def get_snp_locations(tsv_file):
    input_dict = defaultdict(list)
    with open(tsv_file, 'r', newline='') as csvfile:  # Convert tsv to dictionary
        my_reader = csv.reader(csvfile, delimiter='\t')
        first_row = list(next(my_reader))
        try:  # We find necessary indices from header
            chrom = first_row[0]
            pos = int(first_row[1])
            variant_id = first_row[2]
        except ValueError:
            print("Check that your tsv file has no headers and the format is correct!")
            exit(1)
        input_dict[variant_id] = (chrom, pos)
        for row in my_reader:  # Start from second row
            input_dict[row[2]] = [row[0], int(row[1])]
    return input_dict


def read_gmt(path):
    d = defaultdict(list)
    with open(path, 'r', newline='') as db:
        my_reader = csv.reader(db, delimiter='\t')
        for row in my_reader:
            for gene in row[2:]:
                d[row[0]].append(gene)
    return d

def get_features_from_dir(path):
    file_set = [x for x in os.listdir(path) if x.endswith('.bed')]
    feature_set_dict = defaultdict(list)
    with open('features.bed', 'w') as features_file:
        for bed in file_set:
            bed_file = open(f'{path}/{bed}', 'r')
            bed_contents = [x.strip() for x in bed_file.readlines()]
            bed_file.close()
            set_name = bed.replace('.bed', '')
            for i, bed_entry in enumerate(bed_contents):
                elems = bed_entry.strip().split('\t')
                feature_name = f'{set_name}:{i}'
                features_file.write(f'{elems[0]}\t{elems[1]}\t{elems[2]}\t{feature_name}\n')
                feature_set_dict[set_name].append(feature_name)
    return feature_set_dict

def read_features(path):
    feature_dict = defaultdict(list)
    feature_file = open(path, 'r')
    features = [line.strip().split('\t') for line in feature_file]
    feature_file.close()
    for feature in features:
        feature_dict[feature[3]] = feature
    return feature_dict
