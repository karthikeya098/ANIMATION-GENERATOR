import pygame
import sys

import cv2
import os
import datetime
import time
import mediapipe as mp
import json

from Dependencies import *
from ColorPalette import *
from GUIPanel import *
from Tools import *

# Check Point Reached

pygame.init()
btn_font = pygame.font.Font("Fonts/unispace bd.ttf", 18)

clock = pygame.time.Clock()
FPS = 60

# Camera Related #
cap = None
video_writer = None # For Video Writer

recording = False
recordingPath = ""

json_data = []

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Media Pipe Related Variables
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# MediaPipe Initializations
# Face Mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces = 1,
    refine_landmarks = True,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)
# Hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
# Pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Frames, Panels and Labels ----------------------------------------------------------------------------------------------------------------------- #
M_Frame = pygame.display.set_mode((MainFrame_Width, MainFrame_Height), vsync=1)
pygame.display.set_caption("Meta Cam InterFace")

GUIFrame = GUIPanel(M_Frame, GUIFrame_Width, GUIFrame_Height, GUIFrame_X_Pos, GUIFrame_Y_Pos, GrizzliesBlue)

OptionsPane = CreateSurface(M_Frame, OptionsPane_Width, OptionsPane_Height, OptionsPane_X, OptionsPane_Y, CadetBlue)
OP_LabelPane = CreateSurface(M_Frame, OP_L_Width, OP_L_Height, OP_L_X, OP_L_Y, GrizzliesBlue)

TextInputPane = CreateSurface(M_Frame, Text_Input_Width, Text_Input_Height, Text_Input_X, Text_Input_Y, EaglesMidnightGreen)
TI_LabelPane = CreateSurface(M_Frame, TI_L_Width, TI_L_Height, TI_L_X, TI_L_Y, DolphinAqua)

OP_Label = CreateLabel("Choose Camera:", white, "unispace bd.ttf", OP_T_Size, True, OP_T_X, OP_T_Y)

TI_Label_1 = CreateLabel("WIFI IP: ", white, "OCRAEXT.TTF", 30, True, TI_L_X+10, TI_L_Y+10)
TI_Label_2 = CreateLabel("Port: ", white, "OCRAEXT.TTF", 30, True, TI_L_X+10, TI_L_Y+60)

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Text Input Variables ---------------------------------------------------------------------------------------------------------------------------- #

IPTxt = ''
PortTxt = ''

DroidCam = False
IP = False
Port = False
TI_1 = btn_font.render(IPTxt, True, white)
TI_2 = btn_font.render(PortTxt, True, white)

# Added press buttons and cleaned the buttons code

TextBox_Pressed = False
TextBox2_Pressed = False

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Additional Functions -------------------------------------------------------------------------------------------------------------------------------- #
def Save_Json_Data(data, filepath):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Button Functions -------------------------------------------------------------------------------------------------------------------------------- #
def CameraID(DC):
    global DroidCam
    global IP
    global Port
    global TI_1
    global TI_2
    global IPTxt
    global PortTxt

    global TextBox_Pressed
    global TextBox2_Pressed

    DroidCam = DC
    if(DroidCam == True):
        # print("System able to take input of IP and Port")
        mouse_pos = pygame.mouse.get_pos()

        # IP Box --------------------------------------------------------#
        TextBox = pygame.Rect(TI_L_X+275, TI_L_Y+10, 200, 30)
        if(TextBox.collidepoint(mouse_pos)):
            if(pygame.mouse.get_pressed()[0]):
                TextBox_Pressed = True
                TextBox2_Pressed = False
                IP = True
                Port = False

        if(TextBox_Pressed == True):
            if (IP == True):
                TI_1 = btn_font.render(IPTxt, True, white)
        # ----------------------------------------------------------------#
        # Port Box -------------------------------------------------------#
        TextBox2 = pygame.Rect(TI_L_X+275, TI_L_Y+60, 200, 30)
        if(TextBox2.collidepoint(mouse_pos)):
            if(pygame.mouse.get_pressed()[0]):
                TextBox_Pressed = False
                TextBox2_Pressed = True
                Port = True
                IP = False
        
        if(TextBox2_Pressed == True):
            if (Port == True):
                TI_2 = btn_font.render(PortTxt, True, white)

        # ------------ ----------------------------------------------------#
        pygame.draw.rect(M_Frame, Lust, TextBox, 4)
        pygame.draw.rect(M_Frame, Lust, TextBox2, 4)
    else:
        # print("System is using WebCam")
        None

def W_Cam():
    global DroidCam
    global IPTxt
    global PortTxt
    global TI_1
    global TI_2

    DroidCam = False
    IPTxt = ''
    PortTxt = ''

    TI_1 = btn_font.render(IPTxt, True, white)
    TI_2 = btn_font.render(PortTxt, True, white)
    
def D_Cam():
    global DroidCam
    DroidCam = True

def Start():
    global video_writer, recording, json_data
    recording = True
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"Captures/recording_{timestamp}.avi"
    json_file = f"Captures/recording_{timestamp}.json"

    # Initialize Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_file, fourcc, 20.0, (600, 400))

    # Initialize JSON DATA
    json_data = {
        "timestamp": timestamp,
        "frames": []
    }

    print(f"Recording started: {output_file}")

def Stop():
    global recording, video_writer, json_data
    recording = False

    if video_writer:
        video_writer.release()
        video_writer = None

    # Save JSON Data
    if json_data:
        json_file = f"Captures/recording_{json_data['timestamp']}.json"
        Save_Json_Data(json_data, json_file)
    print("Recording stopped")

def Submit():
    # Camera Related #
    global cap
    # -------------- #

    if (DroidCam == True):
        if (IPTxt != '' and PortTxt != ''):
            print("IP : ", IPTxt)
            print("Port : ", PortTxt)
            cameraString = f"http://{IPTxt}:{PortTxt}/video"
            if cap is None:
                cap = cv2.VideoCapture(cameraString)
                if not cap.isOpened():
                    print("Error : Could not open WebCam")
        else:
            print("Fill the IPTxt and PortTxt")
    else:
        print("It is using Webcam", 0)

        # Camera Related #
        if cap is None:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error : Could not open WebCam")
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Buttons ----------------------------------------------------------------------------------------------------------------------------------------- #

radio1 = Button(M_Frame, "Webcam", 100, 30, (400, 60), 6, btn_font, onclick = W_Cam)
radio2 = Button(M_Frame, "DroidCam", 100, 30, (400, 110), 6, btn_font, onclick = D_Cam)

button1 = Button(M_Frame, "Start Recording", 200, 50, (175, 475), 6, btn_font, onclick = Start)
button2 = Button(M_Frame, "Stop Recording", 200, 50, (425, 475), 6, btn_font, onclick = Stop)

submit = Button(M_Frame, "Submit", 100, 30, (425, 312), 6, btn_font, onclick= Submit)

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Draw Functions ---------------------------------------------------------------------------------------------------------------------------------- #
def drawPanels():
    GUIFrame.Create_GUI_Panel()

    OptionsPane.DrawSurface()
    OP_LabelPane.DrawSurface()

    TextInputPane.DrawSurface()
    TI_LabelPane.DrawSurface()

def drawLabels():
    OP_Label.DrawLabel(M_Frame)

    TI_Label_1.DrawLabel(M_Frame)
    TI_Label_2.DrawLabel(M_Frame)

def drawButtons():
    radio1.draw()
    radio2.draw()

    button1.draw()
    button2.draw()

    submit.draw()

def draw():
    global cap, video_writer, recording, json_data

    drawPanels()
    drawLabels()
    drawButtons()
    CameraID(DroidCam)
    if DroidCam == True:
        M_Frame.blit(TI_1, (TI_L_X+280, TI_L_Y+10))
        M_Frame.blit(TI_2, (TI_L_X+280, TI_L_Y+60))

    # Camera Related #
    if cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Convert BGR Image to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process Face Mesh
            face_mesh_results = face_mesh.process(image_rgb)

            # Process Hands
            hand_results = hands.process(image_rgb)

            # Process Pose
            pose_results = pose.process(image_rgb)

            # Draw face mesh annotations with a subset of landmarks
            if face_mesh_results.multi_face_landmarks:
                for face_landmarks in face_mesh_results.multi_face_landmarks:
                # Draw only specific landmarks, e.g., around the eyes and mouth
                    landmark_subset = [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 14, 15]  # Example indices
                    for idx in landmark_subset:
                        landmark = face_landmarks.landmark[idx]
                        x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            
            # Draw hand landmarks
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw pose landmarks
            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Convert Frame to RGB Format for pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (600, 400))
            frame_surface = pygame.surfarray.make_surface(frame)
            
            M_Frame.blit(pygame.transform.rotate(frame_surface, -90), (600, 120))

            # Capture and Save Data for JSON
            frame_data = {
                "timestamp": time.time(),
                "face_landmarks": [],
                "hand_landmarks": [],
                "pose_landmarks": []
            }

            # Filter landmarks for JSON data
            landmark_subset = [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 14, 15]  # Example indices

            # Add face landmarks to JSON data
            if face_mesh_results.multi_face_landmarks:
                for face_landmarks in face_mesh_results.multi_face_landmarks:
                    landmarks = [{"x": lm.x, "y": lm.y, "z": lm.z} for idx, lm in enumerate(face_landmarks.landmark) if idx in landmark_subset]
                    frame_data["face_landmarks"].append(landmarks)
            
            # Add hand landmarks to JSON data
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    landmarks = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in hand_landmarks.landmark]
                    frame_data["hand_landmarks"].append(landmarks)

            # Add pose landmarks to JSON data
            if pose_results.pose_landmarks:
                landmarks = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in pose_results.pose_landmarks.landmark]
                frame_data["pose_landmarks"].append(landmarks)

            # Append frame data to JSON data
            if recording:
                json_data["frames"].append(frame_data)

            # If recording Write the Frame
            if recording and video_writer:
                video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# Main Loop --------------------------------------------------------------------------------------------------------------------------------------- #

Run = True
while(Run):
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or 
            (event.type == pygame.KEYDOWN and 
             event.key == pygame.K_ESCAPE)):
            Run = False
            if cap:
                cap.release()
            pygame.display.quit()
            sys.exit()

        if (DroidCam == True) :
            if event.type == pygame.KEYDOWN:
                if IP == True:
                    if event.key == pygame.K_BACKSPACE:
                        IPTxt = IPTxt[0:-1]
                    else:
                        IPTxt += event.unicode
                if Port == True:
                    if event.key == pygame.K_BACKSPACE:
                        PortTxt = PortTxt[0:-1]
                    else:
                        PortTxt += event.unicode

    M_Frame.fill((BroncosNavy))

    draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.display.quit()
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
if cap:
    cap.release()