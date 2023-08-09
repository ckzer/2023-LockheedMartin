# import
import time
import cv2 as cv
import numpy
from threading import Thread
from djitellopy import Tello
import pyzbar.pyzbar as pyzbar

# 변수 선언
Dec_r = Dec_g = Dec_b = 0
R_flag = B_flag = G_flag = 0
cap_r = cap_g = cap_b = 0
centerX, centerY = 0, 0
find_r, find_g, find_b = 0, 0, 0
right_flag, left_flag, top_flag, bottom_flag = 0, 0, 0, 0

QR_flag = 0
print_qr = 0

i = 0
degree = 0

barcode_data = ""
objectType = ""
type = 0
qr = 0


# 함수 선언
def detect():
    global R_flag, B_flag, G_flag, QR_flag
    global degree
    global kill
    global qr

    R_flag = 0
    G_flag = 0
    B_flag = 0
    
    B_triangle = 0

    QR_flag = 0
    kill = 0

    tello.takeoff()
    # print("takeoff")

    tello.move_up(20)
    time.sleep(1)
    # print("up")

    while R_flag == 0: # 빨간색 미션 안끝났을 때
        degree = 0
        if Dec_r == 0: # 빨간색 도형을 못찾으면a
            while degree != 360:
                tello.rotate_clockwise(20) #  20식 돈다
                # print("turn 20")
                degree += 20
                time.sleep(2)
                if Dec_r == 1: # 도형을 찾으면 도는것 멈추기
                    break
            if Dec_r == 0: # 한바퀴동안 빨간색 못찾으면 20 내려가기
                tello.move_down(20)
                # print("down 20")
                time.sleep(1)
        elif Dec_r == 1: # 빨간색 찾으면
            # 위치에 따라 도형을 중앙에 두기
            if right_flag == 1:
                tello.move_right(20)
                # print("right 20")
                time.sleep(1)
            elif left_flag == 1:
                tello.move_left(20)
                # print("left 20")
                time.sleep(1)
            if top_flag == 1:
                tello.move_up(20)
                # print("up 20")
                time.sleep(1)
            elif bottom_flag == 1:
                tello.move_down(20)
                # print("down 20")
                time.sleep(1)
            if right_flag == 0 and left_flag == 0 and top_flag == 0 and bottom_flag == 0:
                #도형의 중심이 중앙에 있을 때
                tello.move_forward(20) #당일 조정가능, 앞으로 이동(크기가 작은 것을 고려)
                # print("foward 40")
                print(type)
                time.sleep(1)
                if type == 1: # Front이면
                    tello.move_down(20)
                    # print("down 20") # 20 하강
                    time.sleep(1)
                    if qr == 1: # qr을 찍으면
                        R_flag = 1 # R 미션 완료
                        tello.move_up(30)

                        print("Red Finish")
                        break
                    else: # 못찾으면 찾을 때 까지 20씩 하강]
                        tello.move_down(20)
                        # print("down 20")
                        # d = 1
                        while qr == 0:
                            tello.move_down(20)
                            # d += 1
                            # print("down 20")
                            time.sleep(1)
                        R_flag = 1
                        print("Red finish")
                        break
                elif type == 2: # Back일 경우 반대편으로 이동
                    tello.move_left(50)
                    # print("left 50")
                    time.sleep(1)
                    tello.move_forward(100)
                    # print("foward 100")
                    time.sleep(1)
                    tello.move_right(50)
                    # print("right 50")
                    time.sleep(1)
                    tello.rotate_clockwise(180)
                    # print("rotate 180")
                    time.sleep(1)
                    # tello.land()
                    # print("landing")
                    # time.sleep(1)

    # for u in range(d):
    tello.move_up(20)
    # print("up 20")
    time.sleep(1)

    while G_flag == 0: # 빨간색 미션 안끝났을 때
        degree = 0
        if Dec_g == 0: # 빨간색 도형을 못찾으면
            while degree != 360:
                tello.rotate_clockwise(20) #  20식 돈다
                # print("turn 20")
                degree += 20
                time.sleep(2)
                if Dec_g == 1: # 도형을 찾으면 도는것 멈추기
                    break
            if Dec_g == 0: # 한바퀴동안 빨간색 못찾으면 20 내려가기
                tello.move_down(20)
                # print("down 20")
                time.sleep(1)
        elif Dec_g == 1: # 빨간색 찾으면
            # 위치에 따라 도형을 중앙에 두기
            if right_flag == 1:
                tello.move_right(20)
                # print("right 20")
                time.sleep(1)
            elif left_flag == 1:
                tello.move_left(20)
                # print("left 20")
                time.sleep(1)
            if top_flag == 1:
                tello.move_up(20)
                # print("up 20")
                time.sleep(1)
            elif bottom_flag == 1:
                tello.move_down(20)
                # print("down 20")
                time.sleep(1)
            if right_flag == 0 and left_flag == 0 and top_flag == 0 and bottom_flag == 0:
                #도형의 중심이 중앙에 있을 때
                tello.move_forward(20) #당일 조정가능, 앞으로 이동(크기가 작은 것을 고려)
                # print("foward 40")
                print(type)
                time.sleep(1)
                if type == 1: # Front이면
                    tello.move_down(20)
                    # print("down 20") # 20 하강
                    
                    if qr == 1: # qr을 찍으면
                        G_flag = 1 # R 미션 완료
                        tello.move_up(30)
                        # print("up 20")
                        print("Green Finish")
                        break
                    else: # 못찾으면 찾을 때 까지 20씩 하강
                        tello.move_down(20)
                        # print("down 20")
                        # d = 1
                        while qr == 0:
                            # d += 1
                            tello.move_down(20)
                            # print("down 20")
                            time.sleep(1)
                        G_flag = 1
                        print("Green finish")
                        break
                elif type == 2: # Back일 경우 반대편으로 이동
                    tello.move_left(50)
                    # print("left 50")
                    time.sleep(1)
                    tello.move_forward(100)
                    # print("foward 100")
                    time.sleep(1)
                    tello.move_right(50)
                    # print("right 50")
                    time.sleep(1)
                    tello.rotate_clockwise(180)
                    # print("rotate 180")
                    time.sleep(1)
                    # tello.land()
                    # print("landing")
                    # time.sleep(1)


    # while B_flag == 0: # 빨간색 미션 안끝났을 때
    #     degree = 0
    #     if Dec_b == 0: # 빨간색 도형을 못찾으면
    #         while degree != 360:
    #             tello.rotate_clockwise(20) #  20식 돈다
    #             # print("turn 20")
    #             degree += 20
    #             time.sleep(1)
    #             if Dec_b == 1: # 도형을 찾으면 도는것 멈추기
    #                 break
    #         if Dec_b == 0: # 한바퀴동안 빨간색 못찾으면 20 내려가기
    #             tello.move_down(20)
    #             # print("down 20")
    #             time.sleep(1)
    #     elif Dec_b == 1: # 빨간색 찾으면
    #         # 위치에 따라 도형을 중앙에 두기
    #         if right_flag == 1:
    #             tello.move_right(20)
    #             # print("right 20")
    #             time.sleep(1)
    #         elif left_flag == 1:
    #             tello.move_left(20)
    #             # print("left 20")
    #             time.sleep(1)
    #         if top_flag == 1:
    #             tello.move_up(20)
    #             # print("up 20")
    #             time.sleep(1)
    #         elif bottom_flag == 1:
    #             tello.move_down(20)
    #             # print("down 20")
    #             time.sleep(1)
    #         if right_flag == 0 and left_flag == 0 and top_flag == 0 and bottom_flag == 0:
    #             #도형의 중심이 중앙에 있을 때
    #             tello.move_forward(20) #당일 조정가능, 앞으로 이동(크기가 작은 것을 고려)
    #             # print("foward 40")
    #             print(type)
    #             time.sleep(1)
    #             if type == 1: # Front이면
    #                 tello.move_down(20)
    #                 # print("down 20") # 20 하강
    #                 time.sleep(1)
    #                 time.sleep(5)
    #                 if qr == 1: # qr을 찍으면
    #                     G_flag = 1 # R 미션 완료
    #                     break
    #                 else: # 못찾으면 찾을 때 까지 20씩 하강
    #                     tello.move_down(20)
    #                     while qr == 0:
    #                         tello.move_down(20)
    #                         # print("down 20")
    #                         time.sleep(1)
    #             elif type == 2: # Back일 경우 반대편으로 이동
    #                 tello.move_left(50)
    #                 # print("left 50")
    #                 time.sleep(1)
    #                 tello.move_forward(100)
    #                 # print("foward 100")
    #                 time.sleep(1)
    #                 tello.move_right(50)
    #                 # print("right 50")
    #                 time.sleep(1)
    #                 tello.rotate_clockwise(180)
    #                 # print("rotate 180")
    #                 time.sleep(1)
    #                 # tello.land()
    #                 # print("landing")
    #                 # time.sleep(1)
    
    # for u in range(d):
    tello.move_up(20)
    # print("up 20")
    time.sleep(1)
    
    while B_flag == 0:  # 파란색 미션 안 끝났을 때
        degree = 0
        if Dec_b == 0:  # 파란색 도형을 못 찾으면
            while degree != 360:
                tello.rotate_clockwise(20)  # 20도씩 돈다
                # print("turn 20")
                degree += 20
                time.sleep(2)
                if Dec_b == 1:  # 도형을 찾으면 도는 것 stop
                    break
            if Dec_b == 0:  # 한 바퀴동안 파란색 못 찾으면 20 내려가기
                tello.move_down(20)
                # print("down 20")
                time.sleep(1)
        
        elif Dec_b == 1:    # 파란색 찾으면
            # 위치에 따라 도형을 중앙에 두기
            if right_flag == 1:
                tello.move_right(20)
                # print("right 20")
                time.sleep(1)
            elif left_flag == 1:
                tello.move_left(20)
                # print("left 20")
                time.sleep(1)
            if top_flag == 1:
                tello.move_up(20)
                # print("up 20")
                time.sleep(1)
            elif bottom_flag == 1:
                tello.move_down(20)
                # print("down 20")
                time.sleep(1)
            
            # 도형의 중심이 중앙에 있을 때
            if right_flag == 0 and left_flag == 0 and top_flag == 0 and bottom_flag == 0:
                tello.move_forward(20) #! 당일 조정 가능! 앞으로 이동 (크기가 작은 것 고려)
                # print("foward 40")
                print(type)
                time.sleep(1)

                # Back(type==2)일 경우 삼각형 detect 후 반대편으로 이동
                #! 다음 연습 때 기둥으로 확인해보고 수정 가능
                if type == 2:
                    # 파란색 삼각형 contour한 후 front로 이동
                    print("파란색 삼각형 detect 완료!")
                    B_triangle = 1 # 파란 삼각형 인식했다고 0 -> 1로 값 변경
                    # Front(type==1)로 와서 detect + qr 미션까지!
                    tello.move_left(50)
                    # print("left 50")
                    time.sleep(1)
                    tello.move_forward(100)
                    # print("foward 100")
                    time.sleep(1)
                    tello.move_right(50)
                    # print("right 50")
                    time.sleep(1)
                    tello.rotate_clockwise(180)
                    # print("rotate 180")
                    time.sleep(1)

                
                # 초록qr 미션까지 한 다음에 바로 파란색 flag3의 front(원)로 올 경우 반대편 back(삼각형)으로 이동
                elif type == 1 and B_triangle == 0:   # Front이면
                    print("얌마! back에서 삼각형 먼저 갔다와!")

                    tello.move_left(50)
                    # print("left 50")
                    time.sleep(1)
                    tello.move_forward(100)
                    # print("foward 100")
                    time.sleep(1)
                    tello.move_right(50)
                    # print("right 50")
                    time.sleep(1)
                    tello.rotate_clockwise(180)
                    # print("rotate 180")
                    time.sleep(1)
                
                elif type == 1 and B_triangle == 1:
                    print("파란색 원 detect 완료!")
                    tello.move_down(20) # 20 하강
                    # print("down 20")
                    

                    if qr == 1: # qr을 찍으면
                        B_flag = 1  # B 미션 완료
                        tello.land()
                        # print("Landing")
                        break
                    else:   # 못 찾으면 찾을 때까지 20씩 하강
                        tello.move_down(20)
                        # print("down 20")
                        while qr == 0:
                            tello.move_down(20)
                            # print("down 20")
                            time.sleep(1)
                        B_flag = 1
                        print("Green finish")
                        tello.land()
                        # print("Landing")
                        break
                    



# tello 연결
tello = Tello()
tello.connect()
print(tello.get_battery())

# tello 영상 읽어오기
tello.streamon()

# thread 설정
move = Thread(target=detect)
move.start()
# detect 스레드 시작

cap = cv.VideoCapture(1)

while True:
    # _, img_color = cap.read()
    img_color = tello.get_frame_read().frame
    height, width = img_color.shape[:2]
    cell_width = width / 3
    cell_height = height / 3
    img_color = cv.resize(img_color, (width, height), interpolation=cv.INTER_AREA)
    
    imgContour = img_color.copy()
    # tello에서만 활성화
    imgContour = cv.cvtColor(imgContour, cv.COLOR_RGB2BGR)

    img_hsv = cv.cvtColor(img_color, cv.COLOR_RGB2HSV) #웹캠은 BGR로 드론은 RGB로
    imgGray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)

    imgBlur = cv.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv.Canny(imgBlur, 50, 50)

    decoded = pyzbar.decode(imgGray)
    
    qr = 0
    for d in decoded:
        x, y, w, h = d.rect

        barcode_data = d.data.decode("utf-8")
        barcode_type = d.type

        text = '%s (%s)' %(barcode_data, barcode_type)
        print(barcode_data)
        qr = 1
    # getContours(imgCanny)
    contours, hierarchy = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 10000:
            # print(area)
            cv.drawContours(imgContour, cnt, -1, (0, 250, 250), 3)
            peri = cv.arcLength(cnt, True)

            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            # print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv.boundingRect(approx)

            if objCor == 3: # 꼭지젓이 3개일때
                objectType = "Back" #프린트 할 타입
                type = 2 #detect에서 판단하기 위한 변수
            elif objCor == 8: # 원일때
                objectType = "Front"
                type = 1
            else:
                objectType = " "
                type = 0

            cv.rectangle(imgContour, (x, y), (x+w, y+h), (0, 250, 0), 2)
            centerX = int( (x + x + w) / 2) # 중심 X값
            centerY = int( (y + y + h) / 2) # 중심 Y값

    cv.imshow("Contours", imgContour)
    
    # hue값 이용 > RGB 색상 판별

    if centerY != 0 and centerX != 0:
        hue = img_hsv[centerY][centerX][0]

        # 빨간색 범위 (Hue: 0~20, 160~180)
        if (hue >= 0 and hue <= 20) or (hue >= 160 and hue <= 180):
            find_r = 1
        else:
            find_r = 0

        # 초록색 범위 (Hue: 50~90)
        if (hue >= 50) and (hue <= 90):
            find_g = 1
        else:
            find_g = 0

        # 파란색 범위 (Hue: 100~120)
        if (hue >= 100) and (hue <= 120):
            find_b = 1
        else:
            find_b = 0
    
    if centerY != 0 and centerX != 0:
        if centerX < width - (cell_width * 2):
            # print("image is on left")
            left_flag = 1
            right_flag = 0
        elif centerX > width - cell_width:
            # print("image is on right")
            right_flag = 1
            left_flag = 0
        else:
            # print("x is on center")
            right_flag = 0
            left_flag = 0

        if centerY < height - (cell_height * 2):
            # print("image is on top")
            top_flag = 1
            bottom_flag = 0
        elif centerY > height - cell_height:
            # print("image is on bottom")
            top_flag = 0
            bottom_flag = 1
        else:
            # print("y is on center")
            top_flag = 0
            bottom_flag = 0

    if qr == 0: #qr 판독 안했을 때
        if find_r == 1 and objectType != " ": # 빨간색 탐색했을 때
                    Dec_r = 1
                # if top_flag == 0 and bottom_flag == 0 and right_flag == 0 and left_flag == 0:
                    print("r")
                    print(objectType)
                    cv.imwrite('red %d.jpg' % i, imgContour)
                    print("Red Capture finish")
                    # objectType = " " # 초기화가 필요한지 모르겠네요
                    time.sleep(1)
                    Dec_r = 0
        i += 1

        if find_g == 1 and objectType != " ":
                # if top_flag == 0 and bottom_flag == 0 and right_flag == 0 and left_flag == 0:
                    Dec_g = 1
                    print("g")
                    print(objectType)
                    cv.imwrite('green_%d.jpg' % i, imgContour)
                    print("Green Capture finish")
                    # objectType = " "
                    time.sleep(1)
                    Dec_g = 0
        i += 1
        if find_b == 1 and objectType != " ":
                # if top_flag == 0 and bottom_flag == 0 and right_flag == 0 and left_flag == 0:
                    Dec_b = 1
                    print("b")
                    print(objectType)
                    cv.imwrite('blue%d.jpg' % i, imgContour)
                    print("Blue Capture finish")
                    # objectType = " "
                    time.sleep(1)
                    Dec_b = 0

        i += 1


    cv.waitKey(1)


    # ESC 키누르면 종료
    if cv.waitKey(1) & 0xFF == 27:
        break

cv.destroyAllWindows()
kill = 1
move.join()
tello.land()
tello.end()