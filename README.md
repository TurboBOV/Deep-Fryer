# Deep Fryer

<p align="center">
  <img width="100%" src="cover.png" />
</p>

Wrapper around `ffmpeg` to automatically give videos the [deep fried meme](http://knowyourmeme.com/memes/deep-fried-memes) effect.

## Dependencies

```bash
pip install ffmpy
```
## Usage

```bash
python deep-fryer.py -i data/sample.mp4 -o data/deep_fried_sample.mp4
```

## Optional Parameters

Arg | Description | Default
:------- | :---------- | :----------
--video\_dip, -vd | Amount of times to run the video through deep fry filter. | 3
--audio\_dip, -ad | Amount of times to run the audio through deep fry filter. | 10