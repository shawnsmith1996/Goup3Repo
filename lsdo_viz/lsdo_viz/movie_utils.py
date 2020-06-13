import subprocess
from subprocess import call


def make_mov(png_filename, fps, movie_filename):
    cmd = 'ffmpeg -i {} -q:v 1 -r {} -vcodec mpeg4 {}.avi'.format(png_filename, fps, movie_filename)
    # cmd = 'ffmpeg -i {} -vcodec mpeg4 {}.avi'.format(png_filename, movie_filename)
    call(cmd.split())
    cmd = 'ffmpeg -i {}.avi -r {} -acodec libmp3lame -ab 384 {}.mov'.format(movie_filename, fps, movie_filename)
    call(cmd.split())


def make_mp4(png_filename, movie_filename):
    bashCommand = "ffmpeg -f image2 -r 3 -i {} -vcodec libx264 -y {}.mp4".format(png_filename, movie_filename)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()