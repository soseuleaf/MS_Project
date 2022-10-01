import time
import picamera
import RPi.GPIO as GPIO

from PIL import Image

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 6
echo = 16
trig = 20
button = 21

bookLen = []
bookCaseLen = 0

GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)

def ledOnOff(onOff):
    global led
    GPIO.output(led, onOff)

def measureDistance():
    global trig, echo
    GPIO.output(trig, True) # 신호 1 발생
    time.sleep(0.00001) # 짧은시간후 0으로 떨어뜨려 falling edge를 만들기 위함             
    GPIO.output(trig, False) # 신호 0 발생(falling 에지)

    while(GPIO.input(echo) == 0):
        pass
    pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
    while(GPIO.input(echo) == 1):
        pass
    pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림
    pulse_duration = pulse_end - pulse_start
    return 340 * 100 / 2 * pulse_duration

def measureDistanceSecond(n):
    distance = []
    for i in range(n):
        distance.append(measureDistance())
        ledOnOff(True)
        time.sleep(0.5)
        ledOnOff(False)
        time.sleep(0.5)
    avg = sum(distance) / len(distance)
    return (round(avg) == round(distance[1]), avg)

def buttonPressed(pin):
    global bookCaseLen
    checkDistance = measureDistanceSecond(5)
    if checkDistance[0]:
        ledOnOff(True)
        bookCaseLen = checkDistance[1]
        print("측정 완료")
        with open('static/bookLen.txt', 'w') as file:
            file.write(str(bookCaseLen))
    else:
        ledOnOff(False)
        print("에러값 발생")
    time.sleep(5)
    ledOnOff(False)

def getBookLen():
    with open('static/book.txt', 'r') as file:
        for line in file:
            line = line.rstrip().split(',')
            bookLen.append(float(line[3]))

def writeBook(lens):
    with open('static/book.txt', 'a') as file:
        lens = round(lens, 2)
        data = '%s,%s,%s,%s,%s\n' % ("임시" + str(len(bookLen)+1), "출판사", "지은이", lens, "수정이 필요합니다.")
        file.write(data)
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            src = 'static/pic/임시' + str(len(bookLen)+1) + '.jpg'
            print(src)
            '''
            time.sleep(1)
            camera.capture(src)
            img = Image.open(src)
            img = img.transpose(Image.ROTATE_270)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img.save(src)
            '''

            
        bookLen.append(lens)

def inRange(a, b): #a가 b +- 0.5안에 있나?
    return b-1 <= a <= b+1

GPIO.add_event_detect(button, GPIO.RISING, buttonPressed, 200)

print("기존 데이터가 있는지 확인 중 입니다.")

while True :
    with open('static/bookLen.txt', 'r+') as file:
        line = file.readline()
        if line != '':
            getBookLen()
            bookCaseLen = float(line)
            print("기존 데이터가 확인 되었습니다.")
            break
        else:
            print("기존 데이터가 없습니다.")

nowDistance = measureDistance()
while True :
    beforeDistance = nowDistance
    nowDistance = measureDistance()
    dataDistance = bookCaseLen - sum(bookLen)

    if nowDistance > bookCaseLen:
        continue

    if inRange(dataDistance, nowDistance):
        print("정상 범위")
        print("nowDistance", nowDistance)
        print("beforeDistance", beforeDistance)
        print("bookCaseLen", bookCaseLen)
        print("bookLen", sum(bookLen))

    elif not(inRange(nowDistance, beforeDistance)) and nowDistance < beforeDistance:
        print("새 책 발견됨")
        checkDistacne = measureDistanceSecond(5)
        if inRange(checkDistacne[1], nowDistance):
            print("책을 추가합니다.")
            writeBook(beforeDistance - nowDistance)
        else:
            print("단순 에러")
        print("checkDistacne", checkDistacne[1])
        print("nowDistance", nowDistance)
        print("beforeDistance", beforeDistance)
        print("bookCaseLen", bookCaseLen)
        print("bookLen", sum(bookLen))

    else:
        print("비정상 범위 값 초기화가 필요합니다.")
        print("nowDistance", nowDistance)
        print("beforeDistance", beforeDistance)
        print("bookCaseLen", bookCaseLen)
        print("bookLen", sum(bookLen))

    time.sleep(1)