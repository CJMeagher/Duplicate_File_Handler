with open("salary.txt") as monthly_file, open("salary_year.txt", "w") as yearly_file:
    for monthly_salary in monthly_file:
        yearly_file.write(str(int(monthly_salary) * 12) + "\n")
