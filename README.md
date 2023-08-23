# snapchat_filters Real Time
Perform snapchat like filters on live stream.

## Setup
  
  clone project with Python 3.10.10
  ```code
  git clone https://github.com/USTAADCOM/snapchat_filters.git
  cd snapchat_filters
  pip install -r requirements.txt
  ```

## Project Structure

```bash
snapchat_filters
  │   apply_overlay.py
  │   haarcascade_frontalface_default.xm
  │   server.py
  │
  ├───images
  │       cigar.png
  │       doggy_ears.png
  │       doggy_nose.png
  │       doggy_tongue.png
  │       glasses.png
  │       hat.png
  │       mustache.png
  │       rainbow.png
  │
  ├───templates
  │       index.html
```

## Real Time Filter Application 
```code
python server.py
```
