import cv2

def check_cameras(max_cameras=1):
    ## ------ สามารถตรวจสอบเครื่อง ได้หลายเครื่อง
    ## ------ ถ้าให้ตรวจหลายเครื่อง ให้ เอาค่า return ออก เพื่อให้ พิมพ์ค่าออกมา
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            #print(f"Camera {i} is available.")
            return  True
            cap.release()

        else:
            return  False
            #print(f"Camera {i} is not available.")

if __name__ == "__main__":
  x =  check_cameras()
  print(x)
