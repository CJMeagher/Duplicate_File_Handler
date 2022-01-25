for i in range(1, 11):
    file_name = f"file{i}.txt"
    with open(file_name, "w") as f:
        f.write(str(i))
