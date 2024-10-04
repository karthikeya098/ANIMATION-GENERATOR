MainFrame_Width = 1200
MainFrame_Height = 600

# GUI Frame
GUIFrame_Width = 600
GUIFrame_Height = 600
GUIFrame_X_Pos = 0
GUIFrame_Y_Pos = 0

# OptionsPane
OptionsPane_Width = 500
OptionsPane_Height = 100
OptionsPane_X = 50
OptionsPane_Y = 50

# Options Pane Label
OP_L_Width = OptionsPane_Width//2
OP_L_Height = OptionsPane_Height
OP_L_X = OptionsPane_X
OP_L_Y = OptionsPane_Y

# Text Input Pane
Text_Input_Width = 500
Text_Input_Height = 150
Text_Input_X = 50
Text_Input_Y = 200

# TI_Label Pane
TI_L_Width = Text_Input_Width//2
TI_L_Height = Text_Input_Height
TI_L_X = Text_Input_X
TI_L_Y = Text_Input_Y

# ButtonsPane
offset = 50
ButtonsPane_Width = 500
ButtonsPane_Height = 100
ButtonsPane_X = 50
ButtonsPane_Y = (MainFrame_Height-ButtonsPane_Height) - offset

# Button 1
btn1_Width = (ButtonsPane_Width//2)
btn1_Height = ButtonsPane_Height
btn1_X = ButtonsPane_X
btn1_Y = ButtonsPane_Y

# Button 2
btn2_Width = (ButtonsPane_Width//2)
btn2_Height = ButtonsPane_Height
btn2_X = ButtonsPane_X + btn1_Width
btn2_Y = ButtonsPane_Y

# Choose Camera
OP_T_X = OP_L_X
OP_T_Size = 30
OP_T_Y = (OP_L_Height//2) + (OP_T_Size)