import os
import random
import ffmpy
import argparse
from collections import OrderedDict
from shutil import copyfile, rmtree
from utils import line_break, make_random_value, get_total_seconds, get_dimensions

TMP_FOLDER = './tmp'
if not os.path.exists(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)


def create_filter_args():
    """
    Create randomized "deep fried" visual filters
    returns command line args for ffmpeg's filter flag -vf
    """
    saturation = make_random_value([2, 3])
    contrast = make_random_value([1.5, 2])
    noise = make_random_value([30, 60])
    gamma_r = make_random_value([1, 3])
    gamma_g = make_random_value([1, 3])
    gamma_b = make_random_value([1, 3])

    eq_str = 'eq=saturation={}:contrast={}'.format(saturation, contrast)
    eq_str += ':gamma_r={}:gamma_g={}:gamma_b={}'.format(gamma_r, gamma_g, gamma_b)
    noise_str = 'noise=alls={}:allf=t'.format(noise)
    sharpness_str = 'unsharp=5:5:1.25:5:5:1'

    return ['-vf', ','.join([eq_str, noise_str, sharpness_str])]


def extract_audio(input_file):
    output_args = ['-y', '-vn']
    output = '{}/input_audio.wav'.format(TMP_FOLDER)
    ff = ffmpy.FFmpeg(inputs={input_file: None}, outputs={output: output_args})

    try:
        ff.run()
    except Exception as e:
        line_break(3)
        print('Failed to extract audio.\n{}'.format(e))

    return output

def extract_video(input_file):
    output_args = ['-y', '-an']
    output = '{}/input_video.mp4'.format(TMP_FOLDER)
    ff = ffmpy.FFmpeg(inputs={input_file: None}, outputs={output: output_args})

    try:
        ff.run()
    except Exception as e:
        line_break(3)
        print('Failed to extract video.\n{}'.format(e))

    return output


def deep_fry_video(input_video, video_dip):
    output_args = create_filter_args()
    video_file = None

    for idx in range(0, video_dip):
        input_file = video_file or input_video
        output = '{}/tmp_video_{}.mp4'.format(TMP_FOLDER, idx)

        ff = ffmpy.FFmpeg(inputs={input_file: None}, outputs={output: output_args})
        try:
            ff.run()
            video_file = output
        except Exception as e:
            line_break(3)
            print('Failed to deep fry video.\n{}'.format(e))

    return output


def deep_fry_audio(input_audio, amt):
    output_args = ['-y', '-af', 'volume=10, bass=g=0, treble=0']
    audio_file = None

    for idx in range(0, amt):
        input_file = audio_file or input_audio
        output = '{}/tmp_audio_{}.wav'.format(TMP_FOLDER, idx)
        ff = ffmpy.FFmpeg(inputs={input_file: None}, outputs={output: output_args})
        try:
            ff.run()
            audio_file = output
        except Exception as e:
            line_break(3)
            print('Failed to increase audio.\n{}'.format(e))

    return audio_file

def create_final_video(fried_video, boosted_audio, output_file):
    inputs = OrderedDict([
        (fried_video, None),
        (boosted_audio, None),
    ])
    outputs = OrderedDict([
        (output_file, ['-y', '-vcodec', 'libx264']),
    ])

    ff = ffmpy.FFmpeg(inputs=inputs, outputs=outputs)

    try:
        ff.run()
        line_break(3)
        print('Succesfully deep fried video at {}!'.format(output_file))
        line_break(3)
        return output_file
    except Exception as e:
        line_break(3)
        print('Failed to create final video.\n{}'.format(e))


def main(input_file, output_file, video_dip, audio_dip):
    extracted_audio = extract_audio(input_file)
    boosted_audio = deep_fry_audio(extracted_audio, audio_dip)

    extracted_video = extract_video(input_file)
    fried_video = deep_fry_video(extracted_video, video_dip)

    create_final_video(fried_video, boosted_audio, output_file)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input_file', help='input file')
    ap.add_argument('-o', '--output_file', help='output file')
    ap.add_argument('-vd', '--video_dip', help='amount of times to run video through filter', default=3, type=int)
    ap.add_argument('-ad', '--audio_dip', help='amount of times to run audio through filter', default=10, type=int)
    args = ap.parse_args()

    assert args.input_file is not None, 'No input file provided...'
    assert args.output_file is not None, 'No output file provided...'

    main(args.input_file, args.output_file, args.video_dip, args.audio_dip)
