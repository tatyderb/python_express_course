"""time() и ctime()"""

import time

print('time()               =', time.time())        # 1524116343.1965854
print('ctime()              =', time.ctime())       # Thu Apr 19 08:39:03 2018
later = time.time() + 15                            # 15 sec later
print('ctime(time()+15 sec) =', time.ctime(later))  # Thu Apr 19 08:39:18 2018
