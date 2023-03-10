import os
import time

import pytest
from config.utils import get_project_path

if __name__ == '__main__':
    path = get_project_path('/test_case/testCreateOrder.py')
    pytest.main([path])
    time.sleep(2)
    os.system('allure generate ./reports/temps -o ./reports/report --clean')
