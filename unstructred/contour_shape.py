import cv2
import numpy as np
shapes={}
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def getQuadrilateral(cordinates):
    # print(cordinates[2][0])
    vector_one=cordinates[0][0]-cordinates[1][0]
    vector_two = cordinates[1][0]-cordinates[2][0]
    vector_three = cordinates[2][0]-cordinates[3][0]
    vector_four = cordinates[3][0]-cordinates[0][0]
    vector_one_mag=np.linalg.norm(vector_one)
    vector_two_mag = np.linalg.norm(vector_two)
    vector_three_mag = np.linalg.norm(vector_three)
    vector_four_mag = np.linalg.norm(vector_four)
    unit_vector_one=vector_one/vector_one_mag
    unit_vector_two = vector_two / vector_two_mag
    unit_vector_three = vector_three / vector_three_mag
    unit_vector_four = vector_four / vector_four_mag
    dot_product_one = np.dot(unit_vector_one, unit_vector_two)
    dot_product_two = np.dot(unit_vector_two, unit_vector_three)
    dot_product_three = np.dot(unit_vector_three, unit_vector_four)
    dot_product_four = np.dot(unit_vector_four, unit_vector_one)
    angle_one = round(180-np.arccos(dot_product_one)*(180/np.pi),0)
    angle_two =round(180-np.arccos(dot_product_two)*(180/np.pi),0)
    angle_three = round(180-np.arccos(dot_product_three)*(180/np.pi),0)
    angle_four = round(180-np.arccos(dot_product_four)*(180/np.pi),0)
    print(angle_one,angle_two,angle_three,angle_four)
    print(vector_one_mag, vector_two_mag, vector_three_mag, vector_four_mag)
    opposite_angle_one = 1 if abs(angle_one-angle_three) < 5 else 0
    opposite_angle_two = 1 if abs(angle_two - angle_four) < 5 else 0
    opposite_side_one = 1 if ((vector_one_mag/vector_three_mag) > 0.98) and ((vector_one_mag/vector_three_mag) < 1.05) else 0
    opposite_side_two = 1 if ((vector_two_mag/vector_four_mag) > 0.98) and ((vector_two_mag/vector_four_mag) < 1.05) else 0
    all_sides_equal = 1 if ((((vector_one_mag/vector_two_mag) > 0.98) and ((vector_one_mag/vector_two_mag) < 1.05)) and (((vector_three_mag/vector_four_mag) > 0.98) and ((vector_three_mag/vector_four_mag) < 1.05))) else 0
    all_angles_equal = 1 if ((((angle_one/angle_two) > 0.98) and ((angle_one/angle_two) < 1.05)) and (((angle_three/angle_four) > 0.98) and ((angle_three/angle_four) < 1.05))) else 0
    if all_angles_equal:
        if all_sides_equal:
            quadrilateral="Square"
        else:
            quadrilateral="Rectangle"
    else:
        if all_sides_equal :
            quadrilateral="Rhombus"
        elif opposite_angle_one and opposite_angle_two and opposite_side_one and opposite_side_two:
            quadrilateral="Parallelogram"
        else:
            quadrilateral = "Quadrilateral"
    return quadrilateral


def getContours(imag,img):

    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # contours,hierarchy = cv2.findContours(img,1,2)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            M=cv2.moments(cnt)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(len(approx))
            objCor = len(approx)
            # print(f'cor:{len(approx)} corner : {approx}')
            x, y, w, h = cv2.boundingRect(approx)
            Xc = int(M['m10']/M['m00'])
            Yc = int(M['m01']/M['m00'])
            if objCor == 3:
                objectType = "Triangle"
            elif objCor == 4:
                quad=getQuadrilateral(approx)
                objectType = quad
            elif objCor == 5:
                objectType = "Pentagon"
            elif objCor == 6:
                objectType = "Hexagon"
            else:
                objectType = "Circle"
            color = ""
            b, g, r = (imag[Yc, Xc])
            if b == 255: color = "blue"
            if g == 128: color = "green"
            if r == 255: color = "red"
            shapes.update({objectType: [color, area, Xc, Yc]})
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)




path = 'polygon1.png'
img = cv2.imread(path)
imgContour = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
# imgCanny = cv2.Canny(imgBlur,100,200)
ret, thresh = cv2.threshold(imgBlur, 245, 255, cv2.THRESH_BINARY_INV)
# getContours(img,imgCanny)
getContours(img,thresh)
sorted_shapes=sorted(shapes.items(),key=lambda val: val[1][1],reverse=True)
print(sorted_shapes)
shapes=dict(sorted_shapes)
# imgBlank = np.zeros_like(img)
# imgStack = stackImages(0.6,([img,imgGray,imgBlur],
#                             [thresh,imgContour,imgBlank]))
# imS = cv2.resize(imgContour, (960, 540))
cv2.imshow("Stack", imgContour)

cv2.waitKey(0)
