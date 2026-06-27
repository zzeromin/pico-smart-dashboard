# 파일명: dashboard.py 또는 app.py (컴퓨터 모드 Local Python 3에서 실행)
import tkinter as tk
from tkinter import font
import serial
import threading
import time

# --------------------------------------------------------
# [핵심 설정] 내 피코가 연결된 포트 번호에 맞게 수정하세요!
# --------------------------------------------------------
PORT = 'COM3'  # 학생 각자 컴퓨터의 포트(예: COM4, COM5)로 변경 필요
BAUD_RATE = 9600

# 1. 비하인드에서 실시간으로 피코 데이터를 읽어오는 함수
def read_from_pico():
    while True:
        try:
            # 시리얼 통신 통로 개방
            with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
                while True:
                    if ser.in_waiting > 0:
                        # 피코가 보낸 "숫자,숫자" 한 줄 읽기
                        line = ser.readline().decode('utf-8').strip()
                        
                        # 쉼표를 기준으로 온도와 습도 분리 가공
                        if ',' in line:
                            temp, hum = line.split(',')
                            
                            # GUI 화면의 글자 실시간 업데이트
                            temp_label.config(text=f"{temp}°C")
                            hum_label.config(text=f"{hum}%")
                            status_label.config(text="연결 상태: 정상 🟢", fg="#2ecc71")
                    time.sleep(0.1)
        except Exception as e:
            # 케이블이 빠지거나 포트 번호가 틀렸을 때 예외 처리
            temp_label.config(text="--°C")
            hum_label.config(text="--%")
            status_label.config(text="피코 연결을 확인하세요! 🔴", fg="#e74c3c")
            time.sleep(2)

# 2. 대시보드 그래픽 화면(GUI) 디자인 설계
root = tk.Tk()
root.title("우리 교실 스마트홈 대시보드")
root.geometry("450x350")
root.configure(bg="#2c3e50")  # 고급스러운 다크 모드 배경색

# 폰트 스타일 정의
title_font = font.Font(family="맑은 고딕", size=18, weight="bold")
data_font = font.Font(family="Impact", size=48)
label_font = font.Font(family="맑은 고딕", size=14, weight="bold")
sub_font = font.Font(family="맑은 고딕", size=11)

# 메인 타이틀 배치
title_label = tk.Label(root, text="🏫 우리 교실 스마트홈 대시보드", font=title_font, fg="#ecf0f1", bg="#2c3e50")
title_label.pack(pady=20)

# 가로 정렬을 위한 레이아웃 프레임
frame = tk.Frame(root, bg="#2c3e50")
frame.pack(pady=10)

# --- [좌측] 온도 표시 상자 ---
temp_frame = tk.LabelFrame(frame, text=" 현재 온도 ", font=label_font, fg="#e67e22", bg="#34495e", bd=2, padx=15, pady=15)
temp_frame.grid(row=0, column=0, padx=20)

temp_label = tk.Label(temp_frame, text="--°C", font=data_font, fg="#e67e22", bg="#34495e")
temp_label.pack()

# --- [우측] 습도 표시 상자 ---
hum_frame = tk.LabelFrame(frame, text=" 현재 습도 ", font=label_font, fg="#3498db", bg="#34495e", bd=2, padx=15, pady=15)
hum_frame.grid(row=0, column=1, padx=20)

hum_label = tk.Label(hum_frame, text="--%", font=data_font, fg="#3498db", bg="#34495e")
hum_label.pack()

# 하단 상태창 배치
status_label = tk.Label(root, text="피코 연결 대기 중...", font=sub_font, fg="#f1c40f", bg="#2c3e50")
status_label.pack(pady=20)

# 3. 메인 화면 리프레시와 통신이 동시에 굴러가도록 멀티스레드 가동
pico_thread = threading.Thread(target=read_from_pico, daemon=True)
pico_thread.start()

# 윈도우 창 유지 루프
root.mainloop()
