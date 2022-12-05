import os

try:
    os.rmdir("db")
except:
    pass
print("Cleaned")