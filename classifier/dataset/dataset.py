import pyedflib


def extract_from_line(lines, i):
    line = lines[i][:-1]
    return line.split('\t')


with open('data/n1.txt') as f:
    outfile = open('data/n1.out', 'w')
    outfile.write("Stage\tStart Instant\tEnd Instant\n")
    lines = f.readlines()
    i = 0
    while i < len(lines):
        values = extract_from_line(lines, i)
        if values[0] == "S1" or values[0] == "S2" or values[0] == "S3" or values[0] == "S4":
            current = values[0]
            start_inst = values[2]
            
            while current == extract_from_line(lines, i+1)[0]:
                i += 1
                
            end_inst = extract_from_line(lines, i)[2]
            outfile.write(current+"\t"+start_inst+"\t"+end_inst+"\n")
        i += 1
    outfile.close()
