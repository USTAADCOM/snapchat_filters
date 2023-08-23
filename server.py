"""
Snapchat filters application flask server main page.
"""
from flask import Flask, render_template, Response
from apply_overlay import VideoCamera

app = Flask(__name__)

def gen_frames(videocamera_object):
    """
    method yiled frame from get_frame() method 
    after applying filters.

    Parameters
    ----------
    None

    Return
    ------
    frame: yiled
        yield live streaming frame with filters.
    """
    while True:
        frame = videocamera_object.get_frame()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
@app.route('/')
def index():
    """
    Index page Snapchat_filters over video streaming application.
    
    Parameters
    ----------
    None

    Return
    ------
        render template index.html.
    """
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """
    method return response of yiled frame from gen_frames() method 
    after applyin filters.

    Parameters
    ----------
    None

    Return
    ------
    frame: Response
        return live streaming frame with filters.
    """
    return Response(gen_frames(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
