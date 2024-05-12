import nmap

# Khởi tạo một đối tượng PortScanner từ nmap
nm = nmap.PortScanner()

# Nhập host cần quét từ người dùng
hostscan = input("Nhập host cần quét: ")

# In ra phiên bản của nmap
print("Phiên bản của nmap: " + nmap.__version__)

# Sử dụng method scan của đối tượng PortScanner để quét các cổng từ 1 đến 1024
nm.scan(hostscan, '1-1024', '-v', '-sP')

# In ra thông tin quét
print("Thông tin quét: ")
print(nm.scaninfo())

# In ra trạng thái của địa chỉ IP được quét
print("Trạng thái IP: " + nm[hostscan].state())

# In ra protocol được phát hiện trên địa chỉ IP đã quét
print("Protocol: " + ','.join(nm[hostscan].all_protocols()))

# Nếu có các cổng mở được phát hiện, in ra danh sách các cổng
if 'tcp' in nm[hostscan]:
    open_ports = nm[hostscan]['tcp'].keys()
    print("Cổng mở:")
    for port in open_ports:
        print("Cổng:", port, "Trạng thái:", nm[hostscan]['tcp'][port]['state'])
else:
    print("Không có cổng mở được phát hiện.")