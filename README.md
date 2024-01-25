# Tennis Video Analysis Application



- This developed system is a sophisticated tool for analyzing tennis matches from video footage. It integrates advanced computer vision techniques to detect the court, track the ball's position, and identify bounces. The system visualizes this information on the video frames, providing a detailed view of the match, including which side of the court the ball hits and tracking the ball's trajectory. This could be a valuable tool for coaches, players, and enthusiasts to analyze gameplay and improve strategies.


# Features

- Court Detection: Identifies the tennis court within the video and extracts relevant key points for analysis.
- Ball Tracking: Tracks the ball's position throughout the match, providing a visual representation of its trajectory.
- Bounce Detection: Detects when( at which frame ) and where the ball bounces on the court.
- Ground Hit Countnter Visualization: Displays the number of ground hits on each side of the court.
- Scene Processing: Analyze different scenes within the video for in-depth match analysis.
- Output Video Generation: Creates an output video with all the visual analytics overlaid on the original footage.

# Models
The application uses three main models:

- CourtDetectorNet: Detects the tennis court and key points.
- BallDetector: Tracks the ball's position frame by frame.
- BounceDetector: Identifies bounce events of the ball.
  
## Before running the application, ensure you have the following prerequisites installed
Clone this repository to your local machine.
- git clone 

Install all required dependencies.
- pip install -r requirements.txt 

Run the script with the following command, specifying the input and output video paths:

- python app.py --path_input_video "path/to/your/input/video.mp4" --path_output_video "path/to/your/output/video.mp4"
