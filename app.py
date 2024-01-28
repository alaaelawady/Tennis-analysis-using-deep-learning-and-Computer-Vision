import argparse
import torch
import videoanalysis 
from processing.court_detection_net import CourtDetectorNet
from processing.bounce_detector import BounceDetector
from processing.ball_detector import BallDetector
from processing.utils import scene_detect


video_processing = videoanalysis.VideoAnalysis()

# Paths to your models

bounce_model_path = 'models/ctb_regr_bounce.cbm'
ball_track_model_path = 'models/model_best.pt'
court_model_path = 'models/model_tennis_court_det.pt'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--path_input_video', type=str, help='path to input video')
    parser.add_argument('--path_output_video', type=str, help='path to output video')
    args = parser.parse_args()
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    frames, fps = video_processing.read_video(args.path_input_video) 

    scenes = scene_detect(args.path_input_video)    


    print('Start court detection .. \n')
    court_detector = CourtDetectorNet(court_model_path, device)
    homography_matrices, kps_court = court_detector.infer_model(frames)
    # print("kps_court" , kps_court)

    print('Start ball detection and Tracking ..\n')
    ball_detector = BallDetector(ball_track_model_path, device)
    ball_track = ball_detector.infer_model(frames)
    # print("ball_track" , ball_track)


    # bounce detection
    print("Start bounce detection ..\n")
    bounce_detector = BounceDetector(bounce_model_path)
    x_ball = [x[0] for x in ball_track]
    y_ball = [x[1] for x in ball_track]
    bounces = bounce_detector.predict(x_ball, y_ball)
    print("The bounces detected at frames number :  " , bounces )


    imgs_res , top_side_hits, bottom_side_hits = video_processing.main(frames, scenes, bounces, ball_track, homography_matrices, kps_court, draw_trace=True)

    video_processing.write(imgs_res, fps, args.path_output_video)
    print("The number of hits at each side :" )
    print( "top_side_hits" , top_side_hits , "\n")
    print("bottom_side_hits" ,bottom_side_hits ,  "\n")
    

