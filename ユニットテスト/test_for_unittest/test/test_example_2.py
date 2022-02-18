import sys

sys.path.append("./src/")
from example_2 import name_management

def test_class(mocker):
    
    test_instance = name_management()
    mocker.patch.object(test_instance, 'activate_GUI')
    mocker.patch.object(test_instance, 'tmp', ['部長'])
    
    test_instance.person_sort()
    
    return test_instance.df