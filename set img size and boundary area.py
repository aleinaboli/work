import cv2
import json
import numpy as np

videodir = 'E:/00_openpose/build/bin/kangli/10.0.44.20_01_20210413153730206.mp4'
cap = cv2.VideoCapture(videodir)
if cap.isOpened():
    print('Video device Initialized.')
else:
    print('Video open failed!')
    exit()
fps = cap.get(cv2.CAP_PROP_FPS)
size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("fps: {}\nsize: {}".format(fps, size))

####查看和设置参数文件####
rbutton_times = 0
img_size_list = []
img_x_y_list = []
boundary_list = []
bdpoint = []
alpoint = []
input_model_size = (360, 640)


####原图裁剪函数######

def draw_img_size(*args):
    window_name = 'SET-THE-IMG-SIZE'
    window_size_rate = 0.8
    """
    @draw_img_size  for set show img from video
    @window_size_rate  default:0.8
    When run in this function,last step is 'exit()' 
    """

    def SET_IMG_SIZE(event, x, y, flags, param):
        global rbutton_times, img_size_list
        if event == cv2.EVENT_RBUTTONDOWN:
            rbutton_times += 1
            cap.release()
            print("video has been paused by 'right button click'")
            cv2.putText(img, "'left button' to select points,'right button' to define", (20, 100), \
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.putText(img, "just need **'TWO POINTS'**", (20, 125), \
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.waitKey(0)
        if event == cv2.EVENT_LBUTTONDOWN:
            point = (int(x / window_size_rate), int(y / window_size_rate))
            img_size_list.append(point)
            print('selected point', img_size_list)
            xy = f'x{int(x / window_size_rate)},y{int(y / window_size_rate)}'
            cv2.circle(img, (x, y), 5, (0, 255, 0), 2)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        if rbutton_times == 2:
            cv2.putText(img, "'right button' to SAVE and CLOSE this window", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, \
                        (255, 0, 0), 2)
            point1 = (int(img_size_list[0][0] * window_size_rate), int(img_size_list[0][1] * window_size_rate))
            point2 = (int(img_size_list[1][0] * window_size_rate), int(img_size_list[1][1] * window_size_rate))
            cv2.rectangle(img, point1, point2, (0, 0, 255), 2)
        cv2.imshow(window_name, img)
        if rbutton_times == 3:
            print("img size has been defined", img_size_list)
            if len(img_size_list) == 2:
                json.dump({'img': {'modify': 1, "img_size_list": img_size_list}}, f)
            f.close()
            print("window has been closed by 'right button'")
            # time.sleep(1)
            cv2.destroyAllWindows()
            exit()

    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (int(window_size_rate * img.shape[1]), int(window_size_rate * img.shape[0])))
        cv2.namedWindow(window_name)
        cv2.putText(img, "fps:{}  size:{}".format(fps, size), (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(img, "'q' or 'right button' to PAUSE  'ESC' to STOP", (20, 50), \
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        cv2.setMouseCallback(window_name, SET_IMG_SIZE)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("video has been paused by 'q'")
            cv2.putText(img, "press 'q' to play".format(fps, size), (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, \
                        (255, 0, 0), 2)
            cv2.imshow(window_name, img)
            cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == 27:
            print("window has been closed by 'ESC'")
            break
        cv2.imshow(window_name, img)
    f.close()
    cap.release()
    cv2.destroyAllWindows()
    exit()


####界限禁区绘制#####

def draw_boundary(*args):
    window_name = 'SET_THE-BOUNDARY'
    """
    @draw_boundary  for set boundary area from img window
    When run in this function,last step is 'exit()' 
    """

    def SET_BOUNDARY(event, x, y, flags, param):
        global rbutton_times, boundary_list, bdpoint, alpoint

        if event == cv2.EVENT_RBUTTONDOWN:
            rbutton_times += 1
            cap.release()
            print("video has been paused by 'right button click'")
            cv2.putText(img, "'left button' draw bdpoint and alpoint.'bdpoint first'", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.waitKey(0)
        if event == cv2.EVENT_LBUTTONDOWN:
            point = (x, y)
            boundary_list.append(point)
            print('selected point', boundary_list)
            xy = 'x:{},y:{}'.format(x, y)
            cv2.circle(img, (x, y), 5, (0, 255, 0), 2)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
        if rbutton_times == 1:
            if len(boundary_list) == 2 and len(bdpoint) != 2:
                bdpoint.append(boundary_list)
                cv2.line(img, bdpoint[len(bdpoint) - 1][0], bdpoint[len(bdpoint) - 1][1], (0, 255, 0), 2)
                boundary_list = []
            if len(boundary_list) > 3:
                alpoint.append(boundary_list)
                print('alpoint', alpoint)
                boundary_list = []
                alpoint_poly = np.array(alpoint, np.int32)
                print('alpoint_poly', alpoint_poly)
                cv2.polylines(img, alpoint_poly, True, (0, 255, 0), thickness=2)
        if rbutton_times == 2:
            cv2.line(img, bdpoint[len(bdpoint) - 2][0], bdpoint[len(bdpoint) - 2][1], (0, 0, 255), 2)
            cv2.line(img, bdpoint[len(bdpoint) - 1][0], bdpoint[len(bdpoint) - 1][1], (0, 0, 255), 2)
            alpoint_poly = np.array(alpoint, np.int32)
            cv2.polylines(img, alpoint_poly, True, (0, 0, 255), thickness=2)
            print('rb = 2', rbutton_times, bdpoint, alpoint)
        cv2.imshow(window_name, img)
        if rbutton_times == 3 and len(bdpoint) == 2 and len(alpoint[0]) > 3:
            a['boundary_bdpoint'] = {'modify': 1, "bdpoint": bdpoint}
            a['boundary_alpoint'] = {'modify': 1, "alpoint": alpoint}
            with open('./args_down.txt', 'w') as f:
                json.dump(a, f)
            # time.sleep(1)
            cv2.destroyAllWindows()
            exit()

    while True:
        ret, img = cap.read()
        img = img[img_y0:img_y1, img_x0:img_x1]
        img = cv2.resize(img, input_model_size, interpolation=cv2.INTER_AREA)
        cv2.namedWindow(window_name)
        cv2.putText(img, "fps:{}  size:{}".format(fps, size), (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(img, "'right button' to PAUSE 'ESC' to CLOSE ", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 0, 0), 1)
        try:
            if len(a['boundary_bdpoint']['bdpoint']) == 2:
                cv2.line(img, tuple(a['boundary_bdpoint']['bdpoint'][0][0]), \
                         tuple(a['boundary_bdpoint']['bdpoint'][0][1]), \
                         (255, 0, 255), 2)
                cv2.line(img, tuple(a['boundary_bdpoint']['bdpoint'][1][0]), \
                         tuple(a['boundary_bdpoint']['bdpoint'][1][1]), \
                         (255, 0, 255), 2)
        except:
            pass
        try:
            if len(a['boundary_alpoint']['alpoint'][0]) > 3:
                alpoint_poly = np.array(a['boundary_alpoint']['alpoint'], np.int32)
                cv2.polylines(img, [alpoint_poly], True, (255, 0, 255), thickness=2)
        except:
            pass

        cv2.setMouseCallback(window_name, SET_BOUNDARY)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("video has been paused by 'q'")
            cv2.putText(img, "press 'q' to play".format(fps, size), (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 0), 1)
            cv2.imshow(window_name, img)
            cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == 27:
            print("window has been closed by 'ESC'")
            break
        cv2.imshow(window_name, img)
    f.close()
    cap.release()
    cv2.destroyAllWindows()
    exit()


####读取json，保存参数到程序#####
try:
    f = open("./args_down.txt", 'r')
    a = json.load(f)
    # logger.info('a_load success')
    if a['img']['modify'] == 1 and len(a['img']['img_size_list']) == 2:
        img_x_y_list = a['img']['img_size_list']
        img_x0 = min(img_x_y_list[0][0], img_x_y_list[1][0])
        img_x1 = max(img_x_y_list[0][0], img_x_y_list[1][0])
        img_y0 = min(img_x_y_list[0][1], img_x_y_list[1][1])
        img_y1 = max(img_x_y_list[0][1], img_x_y_list[1][1])
    try:
        if a['boundary_bdpoint']['modify'] == 1 and len(a['boundary_bdpoint']['bdpoint']) == 2:
            bdpoint = a['boundary_bdpoint']['bdpoint']
        else:
            draw_boundary()
    except:
        draw_boundary()
    try:
        if a['boundary_alpoint']['modify'] == 1 and len(a['boundary_alpoint']['alpoint'][0]) > 3:
            alpoint = a['boundary_alpoint']['alpoint']
        else:
            draw_boundary()
    except:
        draw_boundary()

except (json.decoder.JSONDecodeError, FileNotFoundError, KeyError):
    f = open("./args_down.txt", 'w')
    draw_img_size()

print('file open success,it is:\n', a)

print('x0', img_x0)
print('x1', img_x1)
print('y0', img_y0)
print('y1', img_y1)
print(bdpoint)
print(alpoint)
