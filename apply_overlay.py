import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
specs_ori = cv2.imread('images/glasses.png', -1)
cigar_ori = cv2.imread('images/cigar.png', -1)
mus_ori = cv2.imread('images/mustache.png', -1)
hat_ori = cv2.imread('images/hat.png', -1)
# get(CV_CAP_PROP_FPS)
cv2.VideoCapture(0)

def transparent_overlay(src_img: np.ndarray, overlay_img: np.ndarray,
                        pos = (0, 0), scale = 1)-> np.ndarray:
    """
    take image roi and the overlay image and paste the overlay image in foreground
    over the roi of original image.

    Parameters
    ----------
    src_img: ndarray
        original image array capture from frame.
    overlay_img: ndarray
        original image array capture from frame.
    pos: tuple
        cordinate of point of saturation.
    scale: int
        scale for resize.
    """
    overlay = cv2.resize(overlay_img, (0, 0), fx = scale, fy = scale)
    height, width, _ = overlay_img.shape  # Size of foreground
    rows, cols, _ = src_img.shape  # Size of background Image
    y_axis, x_axis = pos[0], pos[1]  # Position of foreground/overlay image

    for i in range(height):
        for j in range(width):
            if x_axis + i >= rows or y_axis + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src_img[x_axis + i][y_axis + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src_img[x_axis + i][y_axis + j]
    return src_img

class VideoCamera(object):
    """
    Class Doc string.
    """
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 10)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        """
        method yiled frame from get_frame() method 
        after applying overlay images.

        Parameters
        ----------
        None

        Return
        ------
        frame: bytes 
            return live streaming frame with overlay images and 
            landmarks in bytes form.
        """
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame, 1.2, 5, 0, (120, 120), (350, 350))
        for (x, y, w, h) in faces:
            if h > 0 and w > 0:
                hat_symin = int(y + -4 * h / 12)
                hat_symax = int(y + -1 * h / 12)
                sh_hat = hat_symax - hat_symin

                glass_symin = int(y + 1.5 * h / 5)
                glass_symax = int(y + 2.5 * h / 5)
                sh_glass = glass_symax - glass_symin

                cigar_symin = int(y + 4 * h / 6)
                cigar_symax = int(y + 5.5 * h / 6)
                sh_cigar = cigar_symax - cigar_symin

                mus_symin = int(y + 3.5 * h / 6)
                mus_symax = int(y + 5 * h / 6)
                sh_mus = mus_symax - mus_symin

                face_hat_roi = frame[hat_symin : hat_symax, x : x + w]
                face_glass_roi = frame[glass_symin : glass_symax, x : x + w]
                face_cigar_roi = frame[cigar_symin : cigar_symax, x : x + w]
                face_mus_roi = frame[mus_symin:mus_symax, x:x + w]

                hat = cv2.resize(hat_ori, (w, sh_hat), interpolation=cv2.INTER_CUBIC)
                specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
                cigar = cv2.resize(cigar_ori, (w, sh_cigar), interpolation=cv2.INTER_CUBIC)
                mustache = cv2.resize(mus_ori, (w, sh_mus), interpolation=cv2.INTER_CUBIC)

                transparent_overlay(face_hat_roi, hat)
                transparent_overlay(face_glass_roi, specs)
                transparent_overlay(face_cigar_roi, cigar, (int(w / 2), int(sh_cigar / 2)))
                transparent_overlay(face_mus_roi, mustache)
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
