import socket  # Thư viện socket cho việc làm việc với mạng
import os
import signal
import time  # Thư viện time cho việc chờ
import threading
import sys
import subprocess
from queue import Queue  # Sử dụng Queue để quản lý các luồng
from datetime import datetime  # Sử dụng datetime để ghi lại thời gian

# Khóa để tránh in ra lẫn lộn giữa các luồng
print_lock = threading.Lock()

def main():
    socket.setdefaulttimeout(0.30)  # Thiết lập thời gian timeout mặc định cho socket
    discovered_ports = []  # Danh sách các cổng mạng đã phát hiện

    time.sleep(1)  # Dừng 1 giây trước khi tiếp tục
    target = input("Enter your target IP address or URL here: ")  # Nhập địa chỉ IP hoặc URL của mục tiêu
    error = "Invalid Input"  # Biến này không được sử dụng

    # Chuyển đổi tên máy chủ thành IPv4
    try:
        t_ip = socket.gethostbyname(target)  # Chuyển đổi tên máy chủ thành địa chỉ IPv4
    except (UnboundLocalError, socket.gaierror):
        print("\n[-] Invalid format. Please use a correct IP or web address [-]\n")  # Thông báo lỗi nếu địa chỉ không hợp lệ
        sys.exit()  # Thoát khỏi chương trình nếu có lỗi

    # Banner
    print("-" * 60)
    print("Scanning target " + t_ip)  # Hiển thị thông điệp về mục tiêu đang được quét
    print("Time started: " + str(datetime.now()))  # Hiển thị thời gian bắt đầu quét
    print("-" * 60)
    t1 = datetime.now()  # Ghi lại thời gian bắt đầu quét

    # Hàm quét cổng
    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Tạo socket

        try:
            portx = s.connect((t_ip, port))  # Kết nối tới cổng trên mục tiêu
            with print_lock:  # Bắt đầu một khối bảo vệ để tránh in ra lẫn lộn giữa các luồng
                print("Port {} is open".format(port))  # Hiển thị thông điệp nếu cổng mở
            service = socket.getservbyport(port)  # Lấy dịch vụ tương ứng với cổng
            with print_lock:  # Bắt đầu một khối bảo vệ để tránh in ra lẫn lộn giữa các luồng
                print("Service: {}".format(service))  # Hiển thị tên dịch vụ
            discovered_ports.append(str(port))  # Thêm cổng vào danh sách cổng đã phát hiện
            portx.close()  # Đóng kết nối
        except (ConnectionRefusedError, AttributeError, OSError):  # Xử lý các ngoại lệ có thể xảy ra khi kết nối
            pass  # Bỏ qua các ngoại lệ và tiếp tục chương trình

    # Hàm để chạy các luồng
    def threader():
        while True:
            worker = q.get()  # Lấy một công việc từ hàng đợi
            portscan(worker)  # Thực hiện quét cổng cho công việc này
            q.task_done()  # Báo cáo rằng công việc đã hoàn thành

    q = Queue()  # Khởi tạo hàng đợi để quản lý các công việc của các luồng
    for _ in range(200):  # Khởi tạo 200 luồng để quét cổng
        t = threading.Thread(target=threader)  # Tạo một luồng mới
        t.daemon = True  # Đặt luồng này thành chế độ daemon để nó sẽ dừng khi chương trình chính kết thúc
        t.start()  # Khởi động luồng mới

    # Đưa các công việc vào hàng đợi
    for worker in range(1, 65536):
        q.put(worker)

    q.join()  # Chờ tất cả các công việc trong hàng đợi hoàn thành

    t2 = datetime.now()  # Ghi lại thời gian kết thúc quét
    total = t2 - t1  # Tính thời gian tổng cộng của quá trình quét
    print("Port scan completed in " + str(total))  # Hiển thị thời gian tổng cộng của quá trình quét
    print("-" * 60)

try:
    main()  # Gọi hàm main để bắt đầu chương trình
except KeyboardInterrupt:  # Bắt các sự kiện phím tắt từ người dùng
    print("\nGoodbye!")  # Thông báo kết thúc chương trình
    quit()  # Thoát khỏi chương trình
