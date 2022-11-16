from more_itertools import unique_everseen
with open('members.csv', 'r') as f, open('cleanedmembers.csv', 'w') as out_file:
    out_file.writelines(unique_everseen(f))

