from fabric.api import local

def test_cover():
    local('python basitapi/tests/runtests.py --with-coverage --cover-html --cover-package=basitapi')

def test():
    local('python basitapi/tests/runtests.py')
