# -*- coding: utf-8 -*-
# author: https://github.com/jinfagang
import cv2

cap =cv2.VideoCapture()
min_matches = 15
model = cv2.imread('card.jpeg', 0)
print(model.shape)
while True:
    res, frame = cap.read(0)
    if res:
        cv2.imshow('cap', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('model.jpg', frame)
            print('model saved.')
            break;


model = cv2.imread('reference/model.1.jpg', 0)
    print(model.shape)
    video = "http://admin:admin@192.168.199.135:8081/"
    cap = cv2.VideoCapture(video)
    save_f = 'result_1.mp4'
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter(
        save_f, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    while True:
        # read the current frame
        ret, frame = cap.read(0)
        if ret:
            orb = cv2.ORB_create()
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            kp_model, des_model = orb.detectAndCompute(model, None)
            kp_frame, des_frame = orb.detectAndCompute(frame, None)
            matches = bf.match(des_model, des_frame)
            matches = sorted(matches, key=lambda x: x.distance)
            res = cv2.drawMatches(model, kp_model, frame, kp_frame,
                                  matches[: MIN_MATCHES], 0, flags=2)
            cv2.imshow('res', res)
            cv2.waitKey(0)

src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
# compute Homography
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
h, w = model.shape[0], model.shape[1]
pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
# project corners into frame
dst = cv2.perspectiveTransform(pts, M)  
# connect them with lines
img2 = cv2.polylines(frame, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)


def projection_matrix(camera_parameters, homography):
    """
    From the camera calibration matrix and the estimated homography
    compute the 3D projection matrix
    """
    # Compute rotation along the x and y axis as well as the translation
    homography *= -1
    rot_and_transl = np.dot(np.linalg.inv(camera_parameters), homography)
    col_1 = rot_and_transl[:, 0]
    col_2 = rot_and_transl[:, 1]
    col_3 = rot_and_transl[:, 2]
    # normalise vectors
    l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
    rot_1 = col_1 / l
    rot_2 = col_2 / l
    translation = col_3 / l
    # compute the orthonormal basis
    c = rot_1 + rot_2
    p = np.cross(rot_1, rot_2)
    d = np.cross(c, p)
    rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_3 = np.cross(rot_1, rot_2)
    # finally, compute the 3D projection matrix from the model to the current frame
    projection = np.stack((rot_1, rot_2, rot_3, translation)).T
    return np.dot(camera_parameters, projection)
