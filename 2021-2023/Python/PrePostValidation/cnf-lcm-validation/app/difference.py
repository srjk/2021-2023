import sys
import difflib


def find_number_less_than(numbers, target):
    prev_num = None
    for num in numbers:
        if num >= target:
            break
        prev_num = num
    return prev_num


def print_line_from_file(file_path, line_number,output):
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if i == line_number:
                output.write(line)
                break


def search_string_in_file(file_path, search_string):
    print("inside search")
    print(file_path)
    with open(file_path, "r") as f:
        for line in f:
            print(line)
            print(search_string)
            if search_string.replace("echo ") in line:
                return True
    return False

def grenreate_diff(file1_name, file2_name,output_file):
    try:
        # Read the contents of the first cfg file
        with open(file1_name, "r") as file1:
            file1_contents = file1.readlines()

        # Read the contents of the second cfg file
        with open(file2_name, "r") as file2:
            file2_contents = file2.readlines()

        # Find the line numbers of the first matching echo line
        echo_line_numbers = []
        echo_content=[]
        for i, line in enumerate(file1_contents):
            if line.startswith("echo") and line in file2_contents:
                echo_line_numbers.append(i)
                echo_content.append(line.strip())

        # Compare the two cfg files and print the difference lines
        line_number=[]
        with open(output_file, "w") as output:
            diff = difflib.unified_diff(file1_contents, file2_contents, fromfile=file1_name, tofile=file2_name,n=0)
            for line in diff:
                if line.startswith("@@"):
                    line_number=line.replace("@@","").replace(" ","").split("+")
                    continue
                if len(line_number)!=0:
                    if  line.startswith("-"):
                        if "," in line_number[1]:
                            line_number=line_number[1].split(",")
                            result=find_number_less_than(echo_line_numbers,int(line_number[0]))
                        result=find_number_less_than(echo_line_numbers,int(line_number[1]))
                        if result is not None:
                            output.write("#---------------------\n")
                            output.write(echo_content[echo_line_numbers.index(result)])
                            output.write("\n#---------------------\n")
                            output.write(line.strip())  # add 3 to get the correct line number
                        else:
                            output.write(line.strip())
                    else:
                        output.write("    ")
                        output.write(line)
        status="Success"
        return status
    except Exception as e:
        print(e)
        status="Failure"
        return status
