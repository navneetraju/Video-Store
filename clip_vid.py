from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2 
import time
import imutils

'''
Returns Video FPS
Return:
    int: fps of video
    None: Could not get FPS of video/could not read video
'''
def get_video_fps(file_name):
    try:
        video = cv2.VideoCapture(file_name)
    except:
        return None
    (major_ver,minor_ver,subminor_ver)=(cv2.__version__).split('.')
    if int(major_ver)<3:
        fps=video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps=video.get(cv2.CAP_PROP_FPS)
    fps=int(fps)
    return fps

'''
Returns total frames in video
Return:
    int: total frames in video
    None: Could not get frames of video/could not read video
'''
def get_num_frames(file_name):
    try:
        video = cv2.VideoCapture(file_name)
    except:
        return None

    if imutils.is_cv2():
        prop=cv2.cv.CV_CAP_PROP_FRAME_COUNT
    else:
        prop=cv2.CAP_PROP_FRAME_COUNT
    try:
        total=int(video.get(prop))
    except:
        return None
    return total

'''
Clips video between start frame and end frame, stores video after clipping
Return:
    path:str - Path of clipped video(with activity name)
    None - Could not clip video/could not find video
'''
def clip_video(movie_name,start_frame,end_frame,activity_name):
    vid_fps=get_video_fps(movie_name)
    total_frames=get_num_frames(movie_name)
    if vid_fps == None:
        print('[ERROR] Something went wrong')
        return None
    if start_frame > end_frame:
        print('[ERROR] End frame cannot be before start frame')
    if start_frame < 0 or start_frame > total_frames:
        print('[ERROR] Start frame out of range!')
        return None
    if end_frame < 0 or end_frame > total_frames:
        print('[ERROR] End frame out of range!')
        return None
    print('[INFO] Video FPS = ',vid_fps)
    print('[INFO] Total frames in video = ',total_frames)
    start_time = start_frame / vid_fps
    end_time = end_frame / vid_fps
    print('[INFO] Start Time: ',start_time,' End Time: ',end_time)
    target_file_name=movie_name.split('.')[0] + "_" +activity_name+".mp4"
    ffmpeg_extract_subclip(movie_name, start_time, end_time, targetname=target_file_name)
    return target_file_name

'''
if __name__=="__main__":
    file_name="baseball.mp4"
    clip_video(file_name,1,45,'pitching')
'''
    