import os

# print('CPU_NUM: %s' % os.system('cat /proc/cpuinfo | grep "processor"| wc -l'))

cpu_num = os.system('cat /proc/cpuinfo | grep "processor"| wc -l')
print(type(cpu_num))
os.system('export CPU_NUM=%d' % (cpu_num if cpu_num else 3))

print(os.getenv('CPU_NUM'))
