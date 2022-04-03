import os


def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_data_files(base_url,queue,crawled):
    if not os.path.isfile(queue):
        write_file(queue,base_url)

    if not os.path.isfile(crawled):
        write_file(crawled,"")


def write_file(path,data):
    file=open(path,'w')
    file.write(data)
    file.close()

def append_to_file(path,data):
    with open(path,'a') as file:
        file.write(data+"\n")

def delete_file_contents(path):
    # emptying the file content. this replace the file with a new file
    with open(path,"w"):
        pass

def file_to_set(file_name):
    results=set()
    with open(file_name,'rt') as file:
        for line in file:
            results.add(line.replace("\n",""))
    return results

def set_to_file(links_set,file):
    delete_file_contents(file)
    for link in sorted(links_set):
        append_to_file(file,link)



    