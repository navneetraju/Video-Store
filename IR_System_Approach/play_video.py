import cv2

def play_video(videos):
    '''
    Description: This method plays the video from start_frame to end_frame
    Input: List of tuples in the format (videos, start_frame, end_frame)
    Output: plays all the videos one by one
    '''
    flag = 0
    for video in videos:
        # create a video capture object
        try:
            video_object = cv2.VideoCapture(video[0])
        except:
            return None
            
        start_frame = video[1]
        end_frame = video[2]

        if(video_object.isOpened() == False):
            print("[Error] Opening the Video File")

        video_object.set(1,start_frame)
        
        while(video_object.isOpened()):
            # read frame by frame
            ret, frame = video_object.read()
            video_name = video[0].split('/')[-1].split('.')[0]
            if(ret == True and end_frame != start_frame):
                # displays the frame
                cv2.imshow(video_name + 'Frame', frame)
                # press q on keyboard to exit
                # increasing the wait value decrases the fps
                if(cv2.waitKey(40) & 0xFF == ord('q')):
                    flag = 1
                    break
            else:
                break
            start_frame += 1
        if(flag == 1):
            video_object.release()
            cv2.destroyAllWindows()
            break
        # when playing of the video is done close all of the acquired resources
        video_object.release()
        cv2.destroyAllWindows()

