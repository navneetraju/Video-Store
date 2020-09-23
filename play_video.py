import cv2

def play_video(videos):
    '''
    Description: This method plays the video from start_frame to end_frame
    Input: List of tuples in the format (videos, start_frame, end_frame)
    Output: plays all the videos one by one
    '''

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
                if(cv2.waitKey(25) & 0xFF == ord('q')):
                    break
            else:
                break
            start_frame += 1

        # when playing of the video is done close all of the acquired resources
        video_object.release()
        cv2.destroyAllWindows()

# if __name__ == "__main__":
#     videos = [('../dataset/sample/video1.mp4', 300, 400), ('../dataset/sample/video2.mp4', 200, 250), ('../dataset/sample/video3.mp4', 280, 320)]
#     play_video(videos)