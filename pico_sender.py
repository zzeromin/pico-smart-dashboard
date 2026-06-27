# 파일명: pico_sender.py (피코에는 main.py로 저장)
import machine
import time
import dht

# 1. 하드웨어 설정 (GP18 핀에 DHT11 온습도 센서 연결)
sensor = dht.DHT11(machine.Pin(18))

print("=== 피코 온습도 데이터 발송 시작 ===")

while True:
    try:
        # 센서 데이터 측정 가동
        sensor.measure()
        
        # 온도와 습도 데이터 추출
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # [중요] 다른 문자 없이 오직 '숫자,숫자' 형태로만 출력 (예: 24,55)
        print(f"{temp},{hum}")
        
    except OSError as e:
        # 센서 접촉 불량이나 일시적 오류 발생 시 시스템 다운 방지
        print("0,0") 
        
    # 2초마다 주기적으로 데이터 발송
    time.sleep(2)
