

def extract_matrix_from_file(fileName: str):
    with open(fileName, mode ='r') as file:
        n = 0
        for line in file:
            n = n+1
            print(n,line)