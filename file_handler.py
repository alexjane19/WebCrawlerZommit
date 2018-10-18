import os
from datetime import datetime



class FileHandler:
    def __init__(self,filename,dir="logs/"):
        try:
            os.makedirs(dir, 0o0755)
        except OSError as e:
            if e.errno == 17:  # errno.EEXIST
                os.chmod(dir, 0o0755)
                # if not os.path.exists(dir):
                # os.makedirs(dir)
        self.file = open(dir + filename, 'a')
        # file_output.truncate() #erase file

    def write(self,data):
        self.file.write(self.get_now_time() + ":  " + data + "\n")

    def get_now_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def close(self):
        self.file.close()


# def get_directory_files(dir="Dataset/"):
#     dir_files = []
#     for root, dirs, files in os.walk(dir):
#         for file in files:
#             if file.endswith(".txt"):
#                 dir_files.append({'directory':os.path.join(root, file),'filename': file})
#                  #print(os.path.join(root, file))
#     return dir_files
