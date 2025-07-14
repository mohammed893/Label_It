from .hands import HandsPipeline
from .pose import PosePipeline
from .face import FacePipeline

PIPELINES = {
    "hands": HandsPipeline,
    "pose": PosePipeline,
    "face": FacePipeline,
}
landmark_positions = {
    "hands": [
        (250, 450),  # wrist
        (300, 400),  # thumb_cmc
        (320, 350),  # thumb_mcp
        (340, 300),  # thumb_ip
        (360, 250),  # thumb_tip
        (200, 400),  # index_finger_mcp
        (210, 350),
        (220, 300),
        (230, 250),
        (180, 400),  # middle_finger_mcp
        (190, 350),
        (200, 300),
        (210, 250),
        (160, 400),  # ring_finger_mcp
        (170, 350),
        (180, 300),
        (190, 250),
        (140, 400),  # pinky_finger_mcp
        (150, 350),
        (160, 300),
        (170, 250),
    ],
     "pose": [
        (250, 50),    # 0 - Nose
        (230, 40),    # 1 - Left Eye Inner
        (220, 40),    # 2 - Left Eye
        (210, 40),    # 3 - Left Eye Outer
        (270, 40),    # 4 - Right Eye Inner
        (280, 40),    # 5 - Right Eye
        (290, 40),    # 6 - Right Eye Outer
        (200, 70),    # 7 - Left Ear
        (300, 70),    # 8 - Right Ear
        (230, 90),    # 9 - Mouth Left
        (270, 90),    #10 - Mouth Right
        (180, 150),   #11 - Left Shoulder
        (320, 150),   #12 - Right Shoulder
        (150, 200),   #13 - Left Elbow
        (350, 200),   #14 - Right Elbow
        (140, 260),   #15 - Left Wrist
        (360, 260),   #16 - Right Wrist
        (130, 280),   #17 - Left Pinky
        (370, 280),   #18 - Right Pinky
        (150, 280),   #19 - Left Index
        (350, 280),   #20 - Right Index
        (160, 280),   #21 - Left Thumb
        (340, 280),   #22 - Right Thumb
        (200, 300),   #23 - Left Hip
        (300, 300),   #24 - Right Hip
        (190, 370),   #25 - Left Knee
        (310, 370),   #26 - Right Knee
        (180, 450),   #27 - Left Ankle
        (320, 450),   #28 - Right Ankle
        (170, 470),   #29 - Left Heel
        (330, 470),   #30 - Right Heel
        (160, 490),   #31 - Left Foot Index
        (340, 490),   #32 - Right Foot Index
    ]
}

landmark_connections = {
    "hands": [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9,10), (10,11), (11,12),
        (0,13), (13,14), (14,15), (15,16),
        (0,17), (17,18), (18,19), (19,20)
    ],
    "pose": [
        (0, 1), (1, 2), (2, 3),      # Left eye
        (0, 4), (4, 5), (5, 6),      # Right eye
        (0, 9), (0, 10),             # Nose to mouth
        (11, 12),                    # Shoulders
        (11, 13), (13, 15),          # Left arm
        (12, 14), (14, 16),          # Right arm
        (15, 17), (15, 19), (15, 21),# Left fingers
        (16, 18), (16, 20), (16, 22),# Right fingers
        (11, 23), (12, 24),          # Torso sides
        (23, 24),                    # Hips
        (23, 25), (25, 27), (27, 29), (27, 31), # Left leg
        (24, 26), (26, 28), (28, 30), (28, 32)  # Right leg
    ]
}
def get_pipeline_class(name):
    return PIPELINES.get(name)