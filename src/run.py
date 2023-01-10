import os
import pytest
from config.utils import get_project_path

if __name__ == '__main__':
    path = get_project_path('/test_case/testCreateOrder.py')
    pytest.main([path])
    os.system('allure generate ./report -o ./report/html')
