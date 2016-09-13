# CamTunner

Tool useful for camera calibrate and use with openalpr!

Just adjust the parameters for to correspond the size of plates in pixels on the video, with yours alpr parameters.

The central idea: release a tool for person little knowledge calibrate a camera, for post video processing.

USAGE:

	tunner.py -u <url cam> -o <output dir> -t <trained data>


ALPR parameters that correspond to line 74 of tunner.py

```
74                             if (x > self.left_margin)  and (x < self.right_margin) and (w > 140) and (h > 40) and (w < 214 ) and (h < 80):
```

br.conf

```
plate_width_mm = 400
plate_height_mm = 130

multiline = 0

char_height_mm = 48
char_width_mm = 30

char_whitespace_top_mm = 35
char_whitespace_bot_mm = 20

template_max_width_px = 184
template_max_height_px = 46
```
