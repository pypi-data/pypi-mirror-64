from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.video.fx.all import crop
from moviepy.config import get_setting


from moviepy.compat import PY3, DEVNULL
from moviepy.tools import cvsecs
import re
import subprocess
import os



def ffmpeg_parse_infos(filename, print_infos=False, check_duration=True,
                       fps_source='tbr'):
    """Get file infos using ffmpeg.

    Returns a dictionnary with the fields:
    "video_found", "video_fps", "duration", "video_nframes",
    "video_duration", "audio_found", "audio_fps"

    "video_duration" is slightly smaller than "duration" to avoid
    fetching the uncomplete frames at the end, which raises an error.

    """


    # open the file in a pipe, provoke an error, read output
    is_GIF = filename.endswith('.gif')
    cmd = [get_setting("FFMPEG_BINARY"), "-i", filename]
    if is_GIF:
        cmd += ["-f", "null", "/dev/null"]

    popen_params = {"bufsize": 10**5,
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                    "stdin": DEVNULL}

    if os.name == "nt":
        popen_params["creationflags"] = 0x08000000

    proc = subprocess.Popen(cmd, **popen_params)
    (output, error) = proc.communicate()
    infos = error.decode('utf8')

    del proc

    if print_infos:
        # print the whole info text returned by FFMPEG
        print(infos)


    lines = infos.splitlines()
    if "No such file or directory" in lines[-1]:
        raise IOError(("MoviePy error: the file %s could not be found!\n"
                      "Please check that you entered the correct "
                      "path.")%filename)

    result = dict()


    # get duration (in seconds)
    result['duration'] = None

    if check_duration:
        try:
            keyword = ('frame=' if is_GIF else 'Duration: ')
            # for large GIFS the "full" duration is presented as the last element in the list.
            index = -1 if is_GIF else 0
            line = [l for l in lines if keyword in l][index]
            match = re.findall("([0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9])", line)[0]
            result['duration'] = cvsecs(match)
        except:
            raise IOError(("MoviePy error: failed to read the duration of file %s.\n"
                           "Here are the file infos returned by ffmpeg:\n\n%s")%(
                              filename, infos))

    # get the output line that speaks about video
    lines_video = [l for l in lines if ' Video: ' in l and re.search('\d+x\d+', l)]

    result['video_found'] = ( lines_video != [] )

    if result['video_found']:
        try:
            line = lines_video[0]

            # get the size, of the form 460x320 (w x h)
            match = re.search(" [0-9]*x[0-9]*(,| )", line)
            s = list(map(int, line[match.start():match.end()-1].split('x')))
            result['video_size'] = s
        except:
            raise IOError(("MoviePy error: failed to read video dimensions in file %s.\n"
                           "Here are the file infos returned by ffmpeg:\n\n%s")%(
                              filename, infos))

        # Get the frame rate. Sometimes it's 'tbr', sometimes 'fps', sometimes
        # tbc, and sometimes tbc/2...
        # Current policy: Trust tbr first, then fps unless fps_source is
        # specified as 'fps' in which case try fps then tbr

        # If result is near from x*1000/1001 where x is 23,24,25,50,
        # replace by x*1000/1001 (very common case for the fps).

        def get_tbr():
            match = re.search("( [0-9]*.| )[0-9]* tbr", line)

            # Sometimes comes as e.g. 12k. We need to replace that with 12000.
            s_tbr = line[match.start():match.end()].split(' ')[1]
            if "k" in s_tbr:
                tbr = float(s_tbr.replace("k", "")) * 1000
            else:
                tbr = float(s_tbr)
            return tbr

        def get_fps():
            match = re.search("( [0-9]*.| )[0-9]* fps", line)
            fps = float(line[match.start():match.end()].split(' ')[1])
            return fps

        if fps_source == 'tbr':
            try:
                result['video_fps'] = get_tbr()
            except:
                result['video_fps'] = get_fps()

        elif fps_source == 'fps':
            try:
                result['video_fps'] = get_fps()
            except:
                result['video_fps'] = get_tbr()

        # It is known that a fps of 24 is often written as 24000/1001
        # but then ffmpeg nicely rounds it to 23.98, which we hate.
        coef = 1000.0/1001.0
        fps = result['video_fps']
        for x in [23,24,25,30,50]:
            if (fps!=x) and abs(fps - x*coef) < .01:
                result['video_fps'] = x*coef

        if check_duration:
            result['video_nframes'] = int(result['duration']*result['video_fps'])+1
            result['video_duration'] = result['duration']
        else:
            result['video_nframes'] = 1
            result['video_duration'] = None
        # We could have also recomputed the duration from the number
        # of frames, as follows:
        # >>> result['video_duration'] = result['video_nframes'] / result['video_fps']

        # get the video rotation info.
        try:
            rotation_lines = [l for l in lines if 'rotate          :' in l and re.search('\d+$', l)]
            if len(rotation_lines):
                rotation_line = rotation_lines[0]
                match = re.search('\d+$', rotation_line)
                result['video_rotation'] = int(rotation_line[match.start() : match.end()])
            else:
                result['video_rotation'] = 0
        except:
            raise IOError(("MoviePy error: failed to read video rotation in file %s.\n"
                           "Here are the file infos returned by ffmpeg:\n\n%s")%(
                              filename, infos))


    lines_audio = [l for l in lines if ' Audio: ' in l]

    result['audio_found'] = lines_audio != []

    if result['audio_found']:
        line = lines_audio[0]
        try:
            match = re.search(" [0-9]* Hz", line)
            hz_string = line[match.start()+1:match.end()-3]  # Removes the 'hz' from the end
            result['audio_fps'] = int(hz_string)
        except:
            result['audio_fps'] = 'unknown'

    return result


class ClipMaster:
    def __init__(self):
        self._clip_ = ''
        self._target_clip_ = ''
        self._audio_ = ''

    def video_info(self,key_=''):
        """
        #print("ffmpeg -i self._clip_ 2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}' | cut -d'x' -f1".split(' '))
        cmd_str_ = [get_setting("FFMPEG_BINARY"), '-i', self._clip_, '2>&1', '|', 'grep', 'Video:', '|', 'grep', '-Po', "'\\d{3,5}x\\d{3,5}'", '|', 'cut', "-d'x'", '-f1']
        for path in self.execute_(cmd_str_):
            print(path, end="")
        #print(self._clip_,"is converted to",videoname)
        """
        #{'duration': 30.02, 'video_found': True, 'video_size': [1366, 768], 'video_fps': 30.0, 'video_nframes': 901, 'video_duration': 30.02, 'video_rotation': 0, 'audio_found': True, 'audio_fps': 48000}
        if key_ == '':
            return ffmpeg_parse_infos(self._clip_)
        else:
            return ffmpeg_parse_infos(self._clip_)[key_]

    def clip(self,clipname):
        self._clip_ = clipname
        return self
    
    def audio(self,audioname):
        self._audio_ = audioname
        return self

    def execute_(self,cmd_li):
        popen = subprocess.Popen(cmd_li, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd_li)

    def sec2minsec(self,second):
        sec_ = second - 60*int(second / 60)
        min_ = int(second / 60)
        return min_, sec_

    def cut_to(self, target_clip, start_time, end_time):
        #ffmpeg -ss 00:00:30.0 -i input.wmv -c copy -t 00:00:10.0 output.wmv
        #-i  - input
        #-ss - start time - HH:MM:SS.msint / secs
        #-t  - start time - HH:MM:SS.msint / secss
        #found that -ss combined with -c copy resulted in a half-second chop at the start.
        #To avoid that, you have to remove the -c copy (which admittedly will do a transcode).
        #cmd_str_ = [get_setting("FFMPEG_BINARY"),"-ss",start_time,"-i",self._clip_,"-c","copy","-t",end_time,target_clip]
        #https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video
        cmd_str_ = [get_setting("FFMPEG_BINARY"),"-ss",start_time,"-i",self._clip_,"-t",end_time,target_clip]
        for path in self.execute_(cmd_str_):
            print(path, end="")
        print("Scene "+self._clip_+" is cut from "+str(start_time)+" to "+str(end_time)+" sec as "+str(target_clip))
        

    def gif_to(self, target_gif, start_time, end_time):
        clip = (VideoFileClip(self._clip_).subclip((self.sec2minsec(start_time)[0], self.sec2minsec(start_time)[1]),(self.sec2minsec(end_time)[0], self.sec2minsec(end_time)[1])).resize(0.8))
        clip.write_gif(target_gif)


    
    def bind_to(self,videoname):
        my_clip = VideoFileClip(self._clip_)
        audio_background = AudioFileClip(self._audio_)
        final_audio = CompositeAudioClip([ audio_background])
        final_clip = my_clip.set_audio(final_audio)
        final_clip.write_videofile(videoname)

    def crop(self,videoname,sp,ep):
        """croping video"""
        #https://www.reddit.com/r/moviepy/comments/7kervd/how_to_crop_a_centered_square_with_moviepy/
        #https://www.google.com/search?q=how%20to%20crop%20a%20video%20moviepy%20python
        #https://zulko.github.io/moviepy/ref/videofx/moviepy.video.fx.all.crop.html
        #remove text in video online
        #https://ffmpeg.org/ffmpeg-filters.html#crop
        sp1,sp2 = sp
        ep1,ep2 = ep
        out_w = width = ep1 - sp1
        out_h = height = ep2 - sp2
        cmd_str_ = [get_setting("FFMPEG_BINARY"),"-i",self._clip_,"-filter:v",'crop='+str(out_w)+':'+str(out_h)+':'+str(sp1)+':'+str(sp2),videoname]
        for path in self.execute_(cmd_str_):
            print(path, end="")
        print(self._clip_,"is converted to",videoname)

        """
        my_clip = VideoFileClip(self._clip_)
        cropped_clip = crop(my_clip, y1=30)
        cropped_clip.write_videofile(videoname)
        """

    def convert_to_mp4(self,videoname):
        my_clip = VideoFileClip(self._clip_,codec = 'libx264')
        my_clip.write_videofile(videoname)

    def to_mp4(self,videoname):
        #https://blog.addpipe.com/converting-webm-to-mp4-with-ffmpeg/
        if self._clip_.split('.')[-1] == 'webm':
            pass
        #cmd_str_ = [os.path.join(ffmpeg_bin_folder,"ffmpeg.exe"),"-i",self._clip_,videoname]
        cmd_str_ = [get_setting("FFMPEG_BINARY"),"-i",self._clip_,"-movflags","faststart","-profile:v","high","-level","4.2",videoname]
        for path in self.execute_(cmd_str_):
            print(path, end="")
        print(self._clip_,"is converted to",videoname)
    def to_mp3(self,audioname,start_time,end_time):
        #https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg
        cmd_str_ = [get_setting("FFMPEG_BINARY"),'-i',self._clip_,'-ss',start_time,'-t',end_time,'-q:a','0','-map','a',audioname]
        for path in self.execute_(cmd_str_):
            print(path, end="")
        print(self._clip_,"is converted to audio",audioname)
    def add_logo(self,logofile,outputfile):
        # transparent logo png
        # https://ffmpeg.org/ffmpeg-filters.html#Examples-87
        # https://www.ffmpeg.org/ffmpeg-filters.html#pad
        # https://ffmpeg.org/ffmpeg-filters.html#removelogo
        # left
        #cmd_str_ = [get_setting("FFMPEG_BINARY"),'-i', self._clip_, '-i', logofile, '-filter_complex', "overlay=10:main_h-overlay_h-10", outputfile]
        # right
        cmd_str_ = [get_setting("FFMPEG_BINARY"),'-i', self._clip_, '-i', logofile, '-filter_complex',  "overlay=main_w-overlay_w-10:main_h-overlay_h-10", outputfile]
        for path in self.execute_(cmd_str_):
            print(path, end="")
        print("Watermark added to",outputfile)