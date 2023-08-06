import os, time
import shutil

class Organize:
    # This method used to navigation
    def organize(self):
        print("Welcome to Junk File Organizer")
        print("[1] Extenssion")
        print("[2] File Modify Date")
        print("[3] File Size")
        print("[4] File Creation Date")
        choice = int(input("Enter Your Choice: "))
        # According To Extension
        if choice == 1:
            path = input("Enter Directory: ")
            if(os.path.exists(path)):
                self.arrange_file_with_ext(path)
            else:
                print("Directory Not Exists")
        
        # According To File Modification Date
        elif choice == 2:
            path = input("Enter Directory: ")
            if(os.path.exists(path)):
                self.arrange_file_with_modification_date(path)
            else:
                print("Directory Not Exists")
        
        # According To File Size
        elif choice == 3:
            path = input("Enter Directory: ")
            if(os.path.exists(path)):
                self.arrange_file_with_size(path)
            else:
                print("Directory Not Exists")
        
        # According To File Creation Date
        elif choice == 4:
            path = input("Enter Directory: ")
            if(os.path.exists(path)):
                self.arrange_file_with_creation_date(path)
            else:
                print("Directory Not Exists")
        else:
            print("Wrong Input !!")

    # Make Base directory (arranged)
    def make_base_directory(self, path):
        if os.path.exists(path+"/arranged"):
            pass
        else:
            os.mkdir(path+"/arranged")

    # Make day directory (today, yesterday, earlier)
    def make_day_directory(self, path):
        # For Today
        if os.path.exists(path+"/arranged/today"):
            pass
        else:
            os.mkdir(path+"/arranged/today")
        # For Yesterday
        if os.path.exists(path+"/arranged/yesterday"):
            pass
        else:
            os.mkdir(path+"/arranged/yesterday")
        
        # For Erlier
        if os.path.exists(path+"/arranged/earlier"):
            pass
        else:
            os.mkdir(path+"/arranged/earlier")

    # To remove the directory after moved all file to arranged directory
    def remove_directory(self, path):
        all_dir = os.listdir(path)
        for dir in all_dir:
            rm_dir = path+"/"+dir
            if dir == "arranged":
                pass
            else:
                try:
                    shutil.rmtree(rm_dir)
                except NotADirectoryError:
                    os.unlink(rm_dir)
    
    # To move file from source to destination
    def move_file(self, src, dest):
        try:
            return shutil.move(src, dest)
        except shutil.Error:
            pass
            # print("Not Moved !!")

    #=================Arrange According to Modification Date======
    def arrange_file_with_modification_date(self, path):
        # Make Base Directory
        self.make_base_directory(path)
        # Make Day Directory
        self.make_day_directory(path)
        all_files = os.walk(path)
        # Get Today date
        today_time_touple = time.localtime(time.time())
        today = str(today_time_touple[2])+"-"+str(today_time_touple[1])+"-"+str(today_time_touple[0])
        # Get Yesterday date
        yesterday = str(today_time_touple[2]-1)+"-"+str(today_time_touple[1])+"-"+str(today_time_touple[0])
        for dir, fileName, files in all_files:
            for f in files:
                directory = dir+'/'+f
                # print(f, time.ctime(os.path.getmtime(directory)))
                modify_date_touple = time.localtime(os.path.getmtime(directory))
                modify_date = str(modify_date_touple[2])+"-"+str(modify_date_touple[1])+"-"+str(modify_date_touple[0])

                if modify_date == today:
                    dest = path+"/arranged/today/"
                    self.move_file(directory, dest)
                    # print("Today ",f, modify_date)
                elif modify_date == yesterday:
                    dest = path+"/arranged/yesterday/"
                    self.move_file(directory, dest)
                    # print("Yesterday ",f, modify_date)
                else:
                    dest = path+"/arranged/earlier/"
                    self.move_file(directory, dest)
                    # print("Earlerr",f, modify_date)

        # Remove all directory except arranged directory
        self.remove_directory(path)
        print("Arranged File Successfully")

    #=================Arrange According to Creation Date======
    def arrange_file_with_creation_date(self, path):
        # Make Base Directory
        self.make_base_directory(path)
        # Make Day Directory
        self.make_day_directory(path)
        all_files = os.walk(path)
        today_time_touple = time.localtime(time.time())
        today = str(today_time_touple[2])+"-"+str(today_time_touple[1])+"-"+str(today_time_touple[0])
        yesterday = str(today_time_touple[2]-1)+"-"+str(today_time_touple[1])+"-"+str(today_time_touple[0])
        for dir, fileName, files in all_files:
            for f in files:
                directory = dir+'/'+f
                # print(f, time.ctime(os.path.getmtime(directory)))
                created_date_touple = time.localtime(os.path.getctime(directory))
                created_date = str(created_date_touple[2])+"-"+str(created_date_touple[1])+"-"+str(created_date_touple[0])
                if created_date == today:
                    dest = path+"/arranged/today/"
                    self.move_file(directory, dest)
                    # print("Today ",f, modify_date)
                elif created_date == yesterday:
                    dest = path+"/arranged/yesterday/"
                    self.move_file(directory, dest)
                    # print("Yesterday ",f, modify_date)
                else:
                    dest = path+"/arranged/earlier/"
                    self.move_file(directory, dest)
                    # print("Earlerr",f, modify_date)

        # Remove all directory except arranged directory
        self.remove_directory(path)
        print("Arranged File Successfully")

    # ================Arrange According To Size===================
    def arrange_file_with_size(self, path):
        self.make_base_directory(path)
        file_list = []
        all_files = os.walk(path)
        for dir, fileName, files in all_files:
            for f in files:
                directory = dir+'/'+f
                file_list.append(directory)   
        else:
            for file in file_list:
                if os.stat(file).st_size >= 0 and os.stat(file).st_size <= (500*1024):
                    move_dir = path+"/arranged/0kb-500kb"
                    if(os.path.exists(move_dir)):
                        self.move_file(file, move_dir)
                    else:
                        os.mkdir(move_dir)
                        self.move_file(file, move_dir)
                elif os.stat(file).st_size >= (500*1024) and os.stat(file).st_size <= (1024*1024):
                    move_dir = path+"/arranged/500kb-1mb"
                    if(os.path.exists(move_dir)):
                        self.move_file(file, move_dir)
                    else:
                        os.mkdir(move_dir)
                        self.move_file(file, move_dir)
                else:
                    move_dir = path+"/arranged/1mb-larger"
                    if(os.path.exists(move_dir)):
                        self.move_file(file, move_dir)
                    else:
                        os.mkdir(move_dir)
                        self.move_file(file, move_dir)

        # Remove all directory except arranged directory
        self.remove_directory(path)
        print("Arranged Successfully")
    # ================End Section=================================
    
    # ================Arrange According To Extenssion=============
    def make_ext_dir(self, path):
        all_files = os.walk(path)
        for dir, fName, files in all_files:
            for file in files:
                ext = file.split(sep=".")
                directory = path+"/arranged/"+ext[-1]+"_files"
                if os.path.exists(directory):
                    pass
                else:
                    os.mkdir(directory)

    def arrange_file_with_ext(self, path):
        # Create base directory
        self.make_base_directory(path)
        self.make_ext_dir(path)

        all_files = os.walk(path)
        for dir, file_name, files in all_files:
            for f in files:
                directory = dir+'/'+f
                ext = f.split(sep=".")
                try:
                    moving_dir = path+"/arranged/"+ext[-1]+"_files"
                    shutil.move(directory, moving_dir)
                except shutil.Error:
                    # print("Not Moved !!")
                    continue
        print("Arranged All Files")

        # Remove empty folders
        self.remove_directory(path)
    # ================End Section=================================
    
# Create A Object
# a = Organize()

# Callig arrange() method to arrange the file
# a.organize()
