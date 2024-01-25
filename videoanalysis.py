import cv2
import numpy as np
from processing.court_reference import CourtReference

print("load success")

class VideoAnalysis():

    """
    All Args desc in code :            
    
            path_video (str): The path to the video file.

            frames (list): List of video frames.
            scenes (list): List of detected scenes (start and end frame indices).
            ball_track (list): List of ball positions for each frame.
            homography_matrices (list): List of homography matrices for each frame.
            kps_court (list): List of keypoints for the court in each frame.
            draw_trace (bool): Flag to indicate whether to draw ball trace.
            img (numpy.ndarray): The image on which to draw the labels.
            middle_line_y (int): The y-coordinate of the middle line of the court.
            top_side_hits (int): The number of hits on the top side of the court.
            bottom_side_hits (int): The number of hits on the bottom side of the court.
            bounces (list): List of frames where ball bounces are detected.
            trace (int, optional): Number of frames to trace back for the ball. Defaults to 7.

    """
    def __init__(self):
        print("Tennis  Analysis Initialized")

    def read_video(self , path_video):
        """
        Reads a video file and converts it into a list of frames.
        Returns:
            tuple: A tuple containing a list of frames and the frames per second (fps) of the video.
        """
        cap = cv2.VideoCapture(path_video)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                resized_frame = cv2.resize(frame, (1280, 720))  # Resize for model compatibility
                frames.append(resized_frame)
            else:
                break
        cap.release()
        return frames, fps




    def get_court_img(self ):
        """
        Generates an image of a tennis court layout.

        Returns:
            numpy.ndarray: An image of a tennis court.
        """
        court_reference = CourtReference()
        court = court_reference.build_court_reference()
        court = cv2.dilate(court, np.ones((10, 10), dtype=np.uint8))
        court_img = (np.stack((court, court, court), axis=2) * 255).astype(np.uint8)
        return court_img


    def draw_side_labels(self , img, top_side_hits, bottom_side_hits):
        """
        Draws labels on the tennis court image indicating the number of ground hits on each player's side.
        Returns:
            numpy.ndarray: The image with labels drawn on it.
        """
        height, width, _ = img.shape
        cv2.putText(img, f" X's side ground hits: {top_side_hits}",( (width // 8 )-70, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, f" Y's side ground hits: {bottom_side_hits}", ((width // 8) - 70, height - 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 0, 0), 2, cv2.LINE_AA)
        
        return img


    def find_middle_line_y(self , kps_court):
        """
        Finds the y-coordinate of the middle line of the tennis court.
        Returns:
            int or None: The y-coordinate of the middle line, or None if not enough data is available.
        """
        try:
            if len(kps_court) >= 6:
                y_values = [kps_court[6][0][1], kps_court[11][0][1]]
                net_line_avg_y = sum(y_values) / len(y_values)
                return net_line_avg_y
            else:
                raise ValueError("Insufficient keypoints data")
        except Exception as e:
            print(f"Error in find_middle_line_y: {e}")
            return None



    # def process_frame(self, frame, middle_line_y, bounces, ball_track, i, top_side_hits, bottom_side_hits, frame_number):
    #     """
    #     Processes a single frame for drawing lines, ball positions, and updating hit counts.
    #     Returns:
    #         tuple: A tuple containing the updated frame, top_side_hits, and bottom_side_hits.
    #     """
    #     if middle_line_y is not None:
    #         cv2.line(frame, (300, int(middle_line_y)), ((frame.shape[1]-300 ), int(middle_line_y)), (0, 0, 255), 4)
    #         if i in bounces:
    #             if ball_track[i] is not None and len(ball_track[i]) == 2:
    #                 ball_x, ball_y = ball_track[i]
    #                 if ball_y < middle_line_y:
    #                     top_side_hits += 1
    #                 else:
    #                     bottom_side_hits += 1

    #     frame = self.draw_side_labels(frame, top_side_hits, bottom_side_hits)
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     font_scale = 1
    #     thickness = 2
    #     cv2.putText(frame, f"Frame number : {frame_number}", ( (frame.shape[1]-500),  (frame.shape[0]-50)), font, font_scale, (240, 0, 0), thickness, cv2.LINE_AA)
    #     hits_display_text = f"X side hits: {top_side_hits} | Y side hits: {bottom_side_hits}"
        
    #     text_size_hits = cv2.getTextSize(hits_display_text, font, font_scale, thickness)[0]

    #     cv2.putText(frame, hits_display_text, ( (frame.shape[1]-text_size_hits[0] - 20),  (frame.shape[0]-20)), font, font_scale, (240, 0, 0), 2, cv2.LINE_AA)

    #     return frame, top_side_hits, bottom_side_hits

    def process_frame(self, frame, middle_line_y, bounces, ball_track, i, top_side_hits, bottom_side_hits, frame_number):
        """
        Processes a single frame for drawing lines, ball positions, and updating hit counts.
        Returns:
            tuple: A tuple containing the updated frame, top_side_hits, and bottom_side_hits.
        """
        try:
            if middle_line_y is not None:
                cv2.line(frame, (300, int(middle_line_y)), ((frame.shape[1]-300), int(middle_line_y)), (0, 0, 255), 4)
                if i in bounces:
                    if ball_track[i] is not None and len(ball_track[i]) == 2:
                        ball_x, ball_y = ball_track[i]
                        # Ensure that ball_y and middle_line_y are not None before comparing
                        if ball_y is not None and middle_line_y is not None:
                            if ball_y < middle_line_y:
                                top_side_hits += 1
                            else:
                                bottom_side_hits += 1

            frame = self.draw_side_labels(frame, top_side_hits, bottom_side_hits)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            cv2.putText(frame, f"Frame number : {frame_number}", ((frame.shape[1]-500), (frame.shape[0]-50)), font, font_scale, (240, 0, 0), thickness, cv2.LINE_AA)
            hits_display_text = f"X side hits: {top_side_hits} | Y side hits: {bottom_side_hits}"
            
            text_size_hits = cv2.getTextSize(hits_display_text, font, font_scale, thickness)[0]

            cv2.putText(frame, hits_display_text, ((frame.shape[1]-text_size_hits[0] - 20), (frame.shape[0]-20)), font, font_scale, (240, 0, 0), 2, cv2.LINE_AA)

        except Exception as e:
            print(f"An error occurred in frame {frame_number}: {e}")
            # Optionally, log the error to a file or error monitoring system
            # Continue processing the next frame

        return frame, top_side_hits, bottom_side_hits

    def process_scene (self , frames, scenes,bounces , ball_track, homography_matrices, kps_court, draw_trace, trace):
        """
        Processes scenes detected in the video.

        
        Returns:
            list: List of processed frames for each scene.
        """
        imgs_res = []
        is_track = [x is not None for x in homography_matrices]
        for num_scene in range(len(scenes)):
            sum_track = sum(is_track[scenes[num_scene][0]:scenes[num_scene][1]])
            len_track = scenes[num_scene][1] - scenes[num_scene][0]
            scene_rate = sum_track/(len_track + 1e-15)
            if scene_rate > 0.5:
                court_img = self.get_court_img()
                for i in range(scenes[num_scene][0], scenes[num_scene][1]):
                    img_res = frames[i]
                    inv_mat = homography_matrices[i]
                    if ball_track[i][0]:
                        if draw_trace:
                            for j in range(0, trace):
                                if i-j >= 0 and ball_track[i-j][0]:
                                    draw_x, draw_y = int(ball_track[i-j][0]), int(ball_track[i-j][1])
                                    img_res = cv2.circle(frames[i], (draw_x, draw_y), radius=5, color=(240, 0, 0), thickness=1)
                                    box_size = 40  # Example size, adjust as needed

                                    # Calculate the top-left corner and bottom-right corner coordinates
                                    top_left = (int(ball_track[i][0] - box_size/2), int(ball_track[i][1] - box_size/2))
                                    bottom_right = (int(ball_track[i][0] + box_size/2), int(ball_track[i][1] + box_size/2))

                                    # Draw the rectangle
                                    img_res = cv2.rectangle(img_res, top_left, bottom_right, color=(0, 255, 0), thickness=2)
                                    img_res = cv2.putText(img_res, 'ball', (int(ball_track[i][0]) + 20, int(ball_track[i][1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, thickness=2, color=(0, 255, 0))

                        else:
                            # Define the size of the box around the ball
        
                            img_res = cv2.circle(img_res, (int(ball_track[i][0]), int(ball_track[i][1])), radius=5, color=(0, 255, 0), thickness=2)
                            img_res = cv2.putText(img_res, 'ball', (int(ball_track[i][0]) + 20, int(ball_track[i][1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, thickness=2, color=(0, 255, 0))
                    if kps_court[i] is not None:
                        for point in kps_court[i]:
                            img_res = cv2.circle(img_res, (int(point[0, 0]), int(point[0, 1])), radius=0, color=(0, 0, 255), thickness=10)
                    if i in bounces and inv_mat is not None:
                        ball_point = np.array(ball_track[i], dtype=np.float32).reshape(1, 1, 2)
                        ball_point = cv2.perspectiveTransform(ball_point, inv_mat)
                        court_img = cv2.circle(court_img, (int(ball_point[0, 0, 0]), int(ball_point[0, 0, 1])), radius=0, color=(0, 255, 255), thickness=60)
                    imgs_res.append(img_res)
            else:
                imgs_res.extend(frames[scenes[num_scene][0]:scenes[num_scene][1]])
        return imgs_res


    def main(self ,frames, scenes, bounces, ball_track, homography_matrices, kps_court, draw_trace=True, trace=7):
        """
        Main processing function that orchestrates
          the processing of video frames and scenes.
        Returns:
            list: Processed list of video frames.
        """
        top_side_hits = 0
        bottom_side_hits = 0
        imgs_res = []

        for i in range(len(frames)):
            frame_number = i + 1  # Frame numbers start from 1

            valid_kps = kps_court[i] if kps_court[i] is not None and len(kps_court[i]) >= 6 else None
            middle_line_y = self.find_middle_line_y(valid_kps)
            frame, top_side_hits, bottom_side_hits = self.process_frame(frames[i], middle_line_y, bounces, ball_track, i, top_side_hits, bottom_side_hits, frame_number)

            # frame, top_side_hits, bottom_side_hits = self.process_frame( frames[i], middle_line_y, bounces, ball_track, i, top_side_hits, bottom_side_hits)
            imgs_res.append(frame)

        scene_imgs =self.process_scene(frames, scenes,bounces ,  ball_track, homography_matrices, kps_court, draw_trace, trace)
        imgs_res.extend(scene_imgs)

        return imgs_res , top_side_hits, bottom_side_hits

    


    def write(self , imgs_res, fps, path_output_video):
        height, width = imgs_res[0].shape[:2]
        out = cv2.VideoWriter(path_output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        for num in range(len(imgs_res)):
            frame = imgs_res[num]
            out.write(frame)
        out.release()    
