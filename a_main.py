from classes.result_folder import SgltResultFolder
from classes.file import get_file, File

schedule_file:File = get_file(r"C:\Users\macie\PycharmProjects\VMOpt\Source\schedule 2023-07-27.xlsx")
print(schedule_file.path)

print (SgltResultFolder().folder)