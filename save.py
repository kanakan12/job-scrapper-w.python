import csv

def save_to_file(jobs, word):
    file = open(f"jobs-{word}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(['Title', 'Company', 'Location', 'Link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return