from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoAlertPresentException,TimeoutException,NoSuchElementException,WebDriverException,ElementNotVisibleException
import os
import time
import shutil
import platform
import subprocess
import shaonutil
import pipreqs


def get_package_name():
    vname = ''
    lines = shaonutil.file.read_file('setup.py')
    if lines:
        i = 0
        for line in lines:
            if 'name=' in line.replace(' ',''):
                marker = '\''
                s = line
                start = s.find(marker) + len(marker)
                end = s.find(marker, start)
                vname = s[start:end]
                break
            i+=1
    else:
        vname = input("Give Package Name : ")
    return vname


package_name = get_package_name()

def initialize_git(project_github_url=''):
    if project_github_url == '':
        project_github_url = input("Give Project Github Url : ")
    commit_message = input("Give Commit Message : ")
    commands = f"""git init
git remote add origin {project_github_url}.git
git add .
git commit -m "{commit_message}
git push -u origin master"""
    commands = commands.split("\n")
    for command in commands:
        for path in execute_shell(command):
            print(path, end="")

def create_setup_py():
    config = shaonutil.file.read_configuration_ini('private/package.config')
    """
    package_name = input("Enter package_name : ")
    version = input("Enter version : ")
    author = input("Enter author : ")
    author_email = config['PACKAGE']['github_user']
    project_url = input("Enter project_url : ")
    config = shaonutil.file.read_configuration_ini('private/package.config')
    project_github_url = config['PACKAGE']['github_project_url']
    keywords = input("Enter keywords seperated by comma : ")
    console_decision = input("Do u need console_scripts ? : ")
    """
    package_name = "PackageMaster"
    version = "0.0.0.1.1"
    author = "Shaon Majumder"
    author_email = config['PACKAGE']['github_user']
    project_url = "https://github.com/ShaonMajumder/PackageMaster"
    project_github_url = config['PACKAGE']['github_project_url']
    keywords = "Package Maker,PyPi Uploader,Shaon Majumder"
    console_decision = "y"

    classifiers = []
    download_url = project_github_url+'/archive/'+version+'.tar.gz'
    keywords = keywords.split(',')

    dirs = [dir_+'/*' for dir_ in shaonutil.file.get_all_dirs() if dir_ != 'private']
    dirs.append('*')
    

    if console_decision == 'y':
        StR = f"""#from distutils.core import setup
from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = '{package_name}',
    packages = ['{package_name}'],
    version = '{version}',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = '{author}',
    author_email = '{author_email}',
    url = '{project_url}',
    download_url = '{download_url}',
    keywords = {keywords},
    classifiers = {classifiers},
    setup_requires=['wheel'],
    entry_points={{
        'console_scripts': [
            '{package_name}={package_name}.{package_name}:main',
        ],
    }},
    package_data= {{'': {dirs}}}
)"""
    else:
        StR = f"""#from distutils.core import setup
from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = '{package_name}',
    packages = ['{package_name}'],
    version = '{version}',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = '{author}',
    author_email = '{author_email}',
    url = '{project_url}',
    download_url = '{download_url}',
    keywords = {keywords},
    classifiers = {classifiers},
    setup_requires=['wheel']
)"""

    shaonutil.file.write_file("setup.py",StR)


def execute_shell(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def cleaning_before_commit(package_name):
    files= package_name+""".egg-info
build
dist
.eggs
geckodriver.log
"""
    print("Cleaning files -",files)

    files = files.split('\n')

    for file in files:
        if os.path.exists(file):
            try:
                shutil.rmtree(file)
            except:
                os.remove(file)


def get_version_name():
    vname = ''
    lines = shaonutil.file.read_file('setup.py')
    if lines:
        i = 0
        for line in lines:
            if 'version=' in line.replace(' ',''):
                marker = '\''
                s = line
                start = s.find(marker) + len(marker)
                end = s.find(marker, start)
                vname = s[start:end]
                break
            i+=1
    else:
        vname = input("Give Version Name : ")
    return vname
    
    

def changing_version_name(prev_vname,new_vname):
    lines = shaonutil.file.read_file('setup.py')

    strs ='\n'.join(lines)
    strs = strs.replace(prev_vname,new_vname)
    shaonutil.file.write_file('setup.py',strs)

def changing_version_name_prev(new_vname):
    lines = shaonutil.file.read_file('setup.py')

    i = 0
    for line in lines:
        if '__version__' in line:
            marker = '\''
            s = line
            start = s.find(marker) + len(marker)
            end = s.find(marker, start)
            vname = s[start:end]
            s = s.replace(vname,new_vname)
            break
        i+=1
    
    lines[i] = s
    strs = '\n'.join(lines)
    shaonutil.file.write_file('setup.py',strs)
    
def make_config():
    """
    package_name
    initial_version
    #0.0.0.0.1
    author
    author_email
    git_project_url
    download_url
    keywords
    """
    pass




def checks_folder(package_name):
    dirs = shaonutil.file.get_all_dirs()
    print("Checking the required files/folders ...")
    folders = f"""private/
private/package.config
setup.py
{package_name}/
README.md
requirements.txt
LICENSE
.gitignore
.git"""

    folders = folders.split('\n')
    for folder in folders:
        if not os.path.exists(folder):
            print("Warning :",folder,"does not exist.")
            if '.gitignore' in folder:
                input_ = input("Do u want to create "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    shaonutil.file.write_file('.gitignore','private/')
            elif 'private/package.config' in folder:
                input_ = input("Do u want to create package.config "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    github_project_url = input("Enter Github Project url : ")
                    github_user = input("Enter Github User : ")
                    github_pass = input("Enter Github Password : ")
                    pypi_user = input("Enter PyPi User : ")
                    pypi_pass = input("Enter PyPi Password : ")

                    strs = f"""; github config
[PACKAGE]
github_project_url = {github_project_url}
github_user = {github_user}
github_pass = {github_pass}
pypi_user = {pypi_user}
pypi_pass = {pypi_pass}"""

                    shaonutil.file.write_file("private/package.config",strs)
            elif 'private/' in folder:
                input_ = input("Do u want to create directory "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    os.mkdir('private')
            elif 'setup.py' in folder:
                input_ = input("Do u want to create "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    create_setup_py()
            elif '.git' in folder:
                input_ = input("Do u want to create "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    config = shaonutil.file.read_configuration_ini('private/package.config')
                    initialize_git(config['PACKAGE']['github_project_url'])
            elif 'requirements.txt' in folder:
                input_ = input("Do u want to create "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    commands = """pipreqs ."""
                    commands = commands.split("\n")

                    for command in commands:
                        for path in execute_shell(command):
                            print(path, end="")
            elif 'README.md' in folder:
                input_ = input("Do u want to create "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    shaonutil.file.write_file('README.md','')
            elif package_name in folder:
                input_ = input("Do u want to create "+folder+" (y/n) : ")
                if input_ == 'y' or input_ == 'Y':
                    os.mkdir(package_name)
                    #moveall()
                    print(folders)
                    for dir_ in shaonutil.file.get_all_files_dirs():
                        print(dir_)
                        #if os.path.isdir(dir_) and dir_ != 'private':
                        if os.path.isdir(dir_):
                            dir_ = dir_+'/'

                        if not dir_ in folders:
                            #[f for f in folders if not f != dir_]
                            dir_ = dir_.replace('/','')
                            print(dir_)
                            shutil.move(dir_,os.path.join(package_name,dir_))
                    


def check_modules():
    print("Checking the required modules ...")
    modules = """setuptools
wheel
twine
pipreqs"""
    modules = modules.split('\n')
    
    for module in modules:
        found = shaonutil.file.package_exists(module)
        if not found:
            print(module," package is not installed.")
            print(module," package is installing.")

            if platform.system() == 'Linux':
                command = """pip3 install """+module
            elif platform.system() == 'Windows':
                command = """pip3 install """+module

            for path in execute_shell(command):
                print(path, end="")


def commit_push():
    commit_msg = input("Give Commit Message : ")

    if platform.system() == 'Linux':
        commands = """git add .
git commit -m \""""+commit_msg+"""\";
git push -u origin master"""
    elif platform.system() == 'Windows':
        commands = """git add .
git commit -m \""""+commit_msg+"""\";
git push -u origin master"""

    commands = commands.split("\n")

    for command in commands:
        for path in execute_shell(command):
            print(path, end="")




def make_release(release_tag,git_url,github_user,github_pass):
    git_url = git_url + '/releases/new'
    print("Making release ...")
    
    
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if platform.system() == 'Linux':
        driver_path_firefox = os.path.join(script_dir,'resources/geckodriver')
    elif platform.system() == 'Windows':
        driver_path_firefox = os.path.join(script_dir,'resources/geckodriver.exe')


    options = Options()
    #options.headless = True
    try:
        driver = webdriver.Firefox(executable_path=driver_path_firefox,options=options)
    except WebDriverException:
        raise WebDriverException("invalid argument: can't kill an exited process\n Check if Firefox version and geckodriver in resources folder is not matched")
    
    driver.get('https://github.com')
    driver.find_element_by_xpath('//a[@href="/login" and contains(@data-ga-click,"text:sign-in")]').click()
    driver.find_element_by_xpath('//input[@type="text" and @name="login" and @id="login_field" and @autocomplete="username"]').click()
    driver.find_element_by_xpath('//input[@type="text" and @name="login" and @id="login_field" and @autocomplete="username"]').send_keys(github_user)
    driver.find_element_by_xpath('//input[@type="password" and @name="password" and @id="password" and @autocomplete="current-password"]').click()
    driver.find_element_by_xpath('//input[@type="password" and @name="password" and @id="password" and @autocomplete="current-password"]').send_keys(github_pass)
    driver.find_element_by_xpath('//input[@type="submit" and @name="commit" and @value="Sign in"]').click()
    driver.get(git_url)
    driver.find_element_by_xpath('//input[@placeholder="Tag version" and @list="git-tags" and contains(@class,"release-tag-field") and contains(@class,"js-release-tag-field") and @aria-label="Enter tag name or version number" and @data-existing-id="none" and @type="text" and @name="release[tag_name]" and @id="release_tag_name"]').click()
    driver.find_element_by_xpath('//input[@placeholder="Tag version" and @list="git-tags" and contains(@class,"release-tag-field") and contains(@class,"js-release-tag-field") and @aria-label="Enter tag name or version number" and @data-existing-id="none" and @type="text" and @name="release[tag_name]" and @id="release_tag_name"]').send_keys(release_tag)
    driver.find_element_by_xpath('//button[contains(@class,"js-publish-release") and @type="submit" and text()="Publish release"]').click()
    
    try:
        link_release = driver.find_element_by_xpath('//a[contains(@href,"releases/tag/0.0.0.27.1") and text()="0.0.0.27.1"]')
        driver.close()
        driver.quit()
        return True
    except:
        driver.close()
        driver.quit()
        #raise NoSuchElementException('Release was not created.')
        print('Release was not created.')
        return False

    
    


    
def upload_to_pypi(pypi_user,pypi_pass):
    
    if platform.system() == 'Linux':
        commands = f"""twine upload dist/* -u {pypi_user} -p {pypi_pass}"""
    elif platform.system() == 'Windows':
        commands = f"""twine upload dist/* -u {pypi_user} -p {pypi_pass}"""

    commands = commands.split("\n")

    for command in commands:
        for path in execute_shell(command):
            print(path, end="")

def create_dist():
    if platform.system() == 'Linux':
        commands = """python3 setup.py sdist bdist_wheel"""
    elif platform.system() == 'Windows':
        commands = """python setup.py sdist bdist_wheel"""

    commands = commands.split("\n")

    for command in commands:
        for path in execute_shell(command):
            print(path, end="")

def locally_install():
    if platform.system() == 'Linux':
        #commands = """pip3 uninstall """+package_name+""" -y
        commands = """python3 setup.py install"""
    elif platform.system() == 'Windows':
        #commands = """pip3 uninstall """+package_name+""" -y
        commands = """python setup.py install"""


    commands = commands.split("\n")

    for command in commands:
        for path in execute_shell(command):
            print(path, end="")

def main():
    check_modules()
    checks_folder(package_name)

    pre_vname = get_version_name()
    print("Showing Previous Version :",pre_vname)
    new_vname = input("Give    New Version Name : ")

    changing_version_name(pre_vname,new_vname)

    cleaning_before_commit(package_name)

    commit_push()
    
    config = shaonutil.file.read_configuration_ini('private/package.config')
    git_url = config['PACKAGE']['github_project_url']
    github_user = config['PACKAGE']['github_user']
    github_pass = config['PACKAGE']['github_pass']
    release_tag = input("Give New Release tag : ")
    make_release(release_tag,git_url,github_user,github_pass)

    ### git diff-index --quiet HEAD || git commit -m \""""+commit_msg+"""\";

    create_dist()

    pypi_user = config['PACKAGE']['pypi_user']
    pypi_pass = config['PACKAGE']['pypi_pass']
    # pypi_user = input("Give pypi user : ")
    # pypi_pass = input("Give pypi pass : ")
    upload_to_pypi(pypi_user,pypi_pass)

    locally_install()

    cleaning_before_commit(package_name)

if __name__ == '__main__':
    main()