# Tennis Video Analysis Application



- This developed system is a sophisticated tool for analyzing tennis matches from video footage. It integrates advanced computer vision techniques to detect the court, track the ball's position, and identify bounces. The system visualizes this information on the video frames, providing a detailed view of the match, including which side of the court the ball hits and tracking the ball's trajectory. This could be a valuable tool for coaches, players, and enthusiasts to analyze gameplay and improve strategies.


# Features

- Court Detection: Identifies the tennis court within the video and extracts relevant key points for analysis.
- Ball Tracking: Tracks the ball's position throughout the match, providing a visual representation of its trajectory.
- Bounce Detection: Detects when( at which frame ) and where the ball bounces on the court.
- Ground Hit Countnter Visualization: Displays the count of the number of ground hits for the ball on each side,
- Scene Processing: Analyze different scenes within the video for in-depth match analysis.
- Output Video Generation: Creates an output video with all the visual analytics overlaid on the original footage.

# Models
The application uses three main models:

- CourtDetectorNet: neural network for detection of 14 main key points of tennis court .
- BallDetector: Tracks the ball's position frame by frame by Tracknet which is a deep learning network for tracking the tennis ball from broadcast videos in which the ball images are small, blurry, and sometimes even invisible. TrackNet takes multiple consecutive frames as input, model will learn not only object tracking but also trajectory to enhance its capability of positioning and recognition.TrackNet generates gaussian heat map centered on ball to indicate position of the ball.
  
- BounceDetector: Used to predict ball bounces during the game based on ball trajectory detected by Tracknet neural network .
  
## Before running the application, ensure you have the following prerequisites installed
Clone this repository to your local machine.
```bash

 git clone 
```
Install all required dependencies.
```bash

 pip install -r requirements.txt 
```
Run the script with the following command, specifying the input and output video paths:
```bash
 python app.py --path_input_video "path/to/your/input/video.mp4" --path_output_video "path/to/your/output/video.mp4"
```
