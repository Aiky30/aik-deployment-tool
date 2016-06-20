from fabric.api import local, prompt

class File(object):

    def __init__(self, Environment):

        self.Environment = Environment

    def destroy_files(self, files_dict):
        for label, file_dict in files_dict.iteritems():

            if 'destroy' in file_dict:
                self.destroy_file(file_dict)

class LocalFile(File):

    # Delete any files
    def destroy_file(self, file_dict):

        answered = False

        while answered is False:

            file_path = file_dict['path']
            answer = prompt('Are you sure you want to delete: %s (y/n)' % file_path)

            if answer == 'y':
                answered=True
                local("sudo rm %s" % file_path)

            elif answer == 'n':
                answered = True
                print("you answered no")

            else:
                print("Wrong answer, please try again.")