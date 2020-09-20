from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2 
import time
import imutils

#Returns FPS and number of frames in video
def get_video_details(movie_name):
    video = cv2.VideoCapture(movie_name)
    (major_ver,minor_ver,subminor_ver)=(cv2.__version__).split('.')
    if int(major_ver)<3:
        fps=video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps=video.get(cv2.CAP_PROP_FPS)
    try:
        if imutils.is_cv2():
            prop=cv2.cv.CV_CAP_PROP_FRAME_COUNT 
        else:
            prop=cv2.CAP_PROP_FRAME_COUNT
        total=int(video.get(prop))
    except:
        print('[INFO] Could not get total frames')
        return (None,None)
    fps=int(fps)
    return (fps,total)

def clip_video(movie_name,start_frame,end_frame,activity_name):
    vid_fps,total_frames=get_video_details(movie_name)
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
    