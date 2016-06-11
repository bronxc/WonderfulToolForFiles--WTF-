#!/usr/bin/python

# Author: Partha & Dipankar, 2016
# Making all the necessary imports
import os, shutil, time, datetime, sys, getopt

# The actual work of copying is done
# by the below function which is called by the wrapper
# function -> `copy_modified`
def start_copying(dir_list, src_path, dest_path, date_specified=None):
    queried_date = date_specified[-1] if date_specified else datetime.datetime.now().day
    queried_month = date_specified[-2] if date_specified else datetime.datetime.now().month
    queried_year = date_specified[-3] if date_specified else datetime.datetime.now().year   
    # Iterate over the filtered list and move the files
    # to the `DESTINATION` folder.
    for file in dir_list:
        if not os.path.exists(os.path.join(dest_path, file)):
            try:
                shutil.copy(os.path.join(src_path, file), dest_path)
            except Exception as e:
                print 'FATAL_ERROR_OCCURED: During copying, ERROR -> %s' % str(e)
                sys.exit(2)
        else:
            if time.localtime(os.path.getmtime(os.path.join(dest_path, file))).tm_mday != queried_date and time.localtime(os.path.getmtime(os.path.join(dest_path, file))).tm_mon != queried_month and time.localtime(os.path.getmtime(os.path.join(dest_path, file))).tm_year != queried_year:
                try:
                    shutil.copy(os.path.join(src_path, file), dest_path)
                except Exception as e:
                    print 'FATAL_ERROR_OCURRED: During copying, ERROR -> %s' % str(e)
                    sys.exit(2)
            else:
                print 'FILE_ALREADY_EXISTS:: The `MODIFIED` recent version of the file -> (%s) already exixts in `DEST` -> (%s) folder!!!' % (file, dest_path)

# Show the appropriate usage details to the user
# Invoked either by `-h` or `--help`
def show_usage(py_script):
    print '---> Usage: python %s `SRC_PATH` `DEST_PATH` [<-d | --date> YYYY-MM-DD<STR> | <-t | --today> noArg<NONE>]' % py_script
    print '--->    Eg: python %s <`SRC_PATH` `DEST_PATH`> [-h | --help]' % py_script
    print '--->    Eg: python %s `SRC_PATH` `DEST_PATH` [-d | --date] 2015-04-12' % py_script
    print '--->    Eg: python %s `SRC_PATH` `DEST_PATH` [-t | --today]' % py_script

# This function makes use of the list comprehesion feature of python
# that lists out all the
# files in the `SOURCE` directory and also makes sure that
# they are regular files and not directories.
# Once established, it filters out only those files that were modified 
# in the given date argument.
def copy_modified(cpy_script, src_path, dest_path, argv):
    try:
        opts, args = getopt.getopt(argv, 'htd:', ['help', 'today', 'date='])
        if not opts:
            show_usage(cpy_script)
            sys.exit(2) 
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                show_usage(cpy_script)
                sys.exit()
            elif opt in ('-d', '--date'):
                try:
                    arg = arg.split('-')
                    if len(arg) == 3:
                        new_arg = []
                        for val in arg:
                            int_repr = int(val)
                            new_arg.append(int_repr)
                    else:
                        raise ValueError()
                except Exception:
                    print '---> Invalid argument for dateArg -> Check Usage'
                    show_usage(cpy_script)
                    sys.exit(2)
                dir_list = [file for file in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, file)) if time.localtime(
        os.path.getmtime(os.path.join(src_path, file))).tm_mday == new_arg[-1] and time.localtime(
        os.path.getmtime(os.path.join(src_path, file))).tm_mon == new_arg[-2] and time.localtime(
        os.path.getmtime(os.path.join(src_path, file))).tm_year == new_arg[-3]]
                
                if dir_list:
                    # Start the copying work
                    start_copying(dir_list, src_path, dest_path, new_arg)
                else:
                    print 'EMPTY_LIST_RETURNED:: No files found to be modified for given time in `SRC` -> (%s) folder' % src_path
                    sys.exit(2)
            elif opt in ('-t', '--today'):
                dir_list = [file for file in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, file)) if time.localtime(
        os.path.getmtime(os.path.join(src_path, file))).tm_mday == datetime.datetime.now().day and  time.localtime(os.path.getmtime(os.path.join(src_path, file))).tm_mon == datetime.datetime.now().month and time.localtime(os.path.getmtime(os.path.join(src_path, file))).tm_year == datetime.datetime.now().year]
                
                if dir_list:
                    # Start the copying work
                    start_copying(dir_list, src_path, dest_path)
                else:
                    print 'EMPTY_LIST_RETURNED:: No files found to be modified for given time in `SRC` -> (%s) folder' % src_path
                    sys.exit(2)
    except getopt.GetoptError:
        show_usage(cpy_script)
        sys.exit(2)

# The main `ENTRY` to the application
# The below function starts the actual copying task
if __name__ == '__main__':
    if not sys.argv[1:]: print 'INVOKE_ERROR:=> Need arguments -> Check Usage'; show_usage(sys.argv[0]); sys.exit()
    if sys.argv[1] not in ('-h', '--help'):
        if os.path.isdir(sys.argv[1]):
            # In Python, if the first argument of `AND` is `FALSE`, it does not
            # care to check the second argument. As a result, we don't get
            # `IndexError` even if second command line flag is not given
            if sys.argv[2:] and sys.argv[2] not in ('-h', '--help'):
                if os.path.isdir(sys.argv[2]):
                    copy_modified(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3:])
                    # ****** Comment out below section in deployment ****** #
                    print '*----------* Script Verifying `DEST` -> (%s) directory *----------*' % sys.argv[2]
                    print os.system('ls -alrth %s' % sys.argv[2])
                    # ****** XXXXXX ****** #
                else:
                    print '`DEST_PATH` -> (%s) argument error -> Check Usage' % sys.argv[2]
                    show_usage(sys.argv[0])
            else:
                # The same principle applies here as well
                # Therefore, we are checking the slice of the second argument
                # rather than the individual argument value
                if not sys.argv[2:]:
                    print '`DEST_PATH` -> Not provided -> Check Usage'
                show_usage(sys.argv[0])
        else:
            print '`SRC_PATH` -> (%s) argument error -> Check Usage' % sys.argv[1]
            show_usage(sys.argv[0])
    else:
        show_usage(sys.argv[0])
