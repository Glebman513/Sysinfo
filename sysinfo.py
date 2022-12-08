import psutil
import platform
import wmi

computer = wmi.WMI()
gpu_info = computer.Win32_VideoController()[0]
proc_info = computer.Win32_Processor()[0]
cpufreq = psutil.cpu_freq()
svmem = psutil.virtual_memory()

def get_size(bytes, suffix="б"):
    factor = 1024
    for unit in ["", "К", "М", "Г", "Т", "П"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

print("="*40, "Информация о системе", "="*40)
uname = platform.uname()
print(f"Операционная система: {uname.system}")
print(f"Имя устройства: {uname.node}")
print(f"Версия операционной системы: {uname.version}")

print("="*40, "Информация о процессоре", "="*40)
print(f"Архитектура ЦП: {uname.machine}")
print("Имя процессора: {0}".format(proc_info.Name))
print(f"Сведения о ЦП: {uname.processor}")
print("Количество ядер ЦП:", psutil.cpu_count(logical=False))
print("Количество потоков ЦП:", psutil.cpu_count(logical=True))
print(f"Максимальная тактовая частота ЦП: {cpufreq.max:.2f}МГц")
print(f"Текущая тактовая частота ЦП: {cpufreq.current:.2f}Мгц")
print(f"Текущая загрузка ЦП: {psutil.cpu_percent()}%")

print("="*40, "Информация о видеокарте", "="*40)
print("Имя видеокарты: {0}".format(gpu_info.Name))

print("="*40, "Информация об ОЗУ", "="*40)
print(f"Общий объём: {get_size(svmem.total)}")
print(f"Занято: {get_size(svmem.used)}")
print(f"Доступно: {get_size(svmem.available)}")

print("="*40, "Информация о дисках", "="*40)
print("Разделы и использование:")
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Буква диска: {partition.mountpoint} ===")
    print(f"  Файловая система: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    print(f"  Всего места: {get_size(partition_usage.total)}")
    print(f"  Места занято: {get_size(partition_usage.used)}")
    print(f"  Места свободно: {get_size(partition_usage.free)}")
