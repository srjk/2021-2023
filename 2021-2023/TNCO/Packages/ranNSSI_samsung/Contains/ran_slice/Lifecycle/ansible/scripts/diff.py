import sys
from datetime import datetime
print(datetime.strptime(sys.argv[1],'%Y-%m-%d %H:%M:%S.%f')-datetime.strptime(sys.argv[2],'%Y-%m-%d %H:%M:%S.%f'))