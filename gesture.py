import cv2 
import mediapipe as mp 
import math

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

reactions = {
    "finger": cv2.imread("gesture_react_image.py/react1.png"),
    "mouth": cv2.imread("gesture_react_image.py/react2.png"),
    "pray": cv2.imread("gesture_react_image.py/react3.png"),
    "phone": cv2.imread("gesture_react_image.py/react4.png"),
    "idle": cv2.imread("gesture_react_image.py/react_idle.png")
}

def detect_gesture(hands_result, pose_result):
    """Fungsi untuk mendeteksi gesture"""
    if not hands_result.multi_hand_landmarks:
        return "idle"
    
    hand_landmarks = hands_result.multi_hand_landmarks[0]
    lm = hand_landmarks.landmark
    
    # Cek status setiap jari
    thumb_extended = abs(lm[4].x - lm[2].x) > 0.05
    index_extended = is_finger_extended(lm, 8, 6)
    middle_extended = is_finger_extended(lm, 12, 10)
    ring_extended = is_finger_extended(lm, 16, 14)
    pinky_extended = is_finger_extended(lm, 20, 18)
    
    # HITUNG JARAK antara ujung jempol dan telunjuk
    thumb_tip = lm[4]
    index_tip = lm[8]
    pinch_distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + 
                               (thumb_tip.y - index_tip.y)**2)
    
    # Deteksi gesture spesifik
    
    # 1. PHONE/OK GESTURE (jempol + telunjuk bertemu di dekat mulut)
    if pinch_distance < 0.05:  # Jempol dan telunjuk dekat/bersentuhan
        if pose_result.pose_landmarks:
            mouth = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT.value]
            wrist = lm[0]
            # Cek apakah tangan dekat mulut
            if distance(wrist, mouth) < 0.2:
                return "phone"  # atau "mouth" sesuai kebutuhan
    
    # 2. FINGER (hanya telunjuk yang terbuka)
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        if not thumb_extended or pinch_distance > 0.1:  # Pastikan bukan OK gesture
            return "finger"
    
    # 3. MOUTH (tangan dekat mulut tanpa pinch)
    if pose_result.pose_landmarks:
        mouth = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT.value]
        wrist = lm[0]
        if distance(wrist, mouth) < 0.15:
            return "mouth"
    
    # 4. PRAY (dua tangan bertemu)
    if hands_result.multi_hand_landmarks and len(hands_result.multi_hand_landmarks) == 2:
        hand1_wrist = hands_result.multi_hand_landmarks[0].landmark[0]
        hand2_wrist = hands_result.multi_hand_landmarks[1].landmark[0]
        if distance(hand1_wrist, hand2_wrist) < 0.1:
            return "pray"
    
    return "idle"

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def is_finger_extended(landmarks, tip_id, pip_id):
    """Cek apakah jari terbuka (extended)"""
    return landmarks[tip_id].y < landmarks[pip_id].y

def detect_gesture(hands_result, pose_result):
    """Fungsi untuk mendeteksi gesture"""
    if not hands_result.multi_hand_landmarks:
        return "idle"
    
    hand_landmarks = hands_result.multi_hand_landmarks[0]
    lm = hand_landmarks.landmark
    
    # Cek status setiap jari (apakah terbuka?)
    thumb_extended = abs(lm[4].x - lm[2].x) > 0.05  # Ibu jari
    index_extended = is_finger_extended(lm, 8, 6)    # Telunjuk
    middle_extended = is_finger_extended(lm, 12, 10) # Tengah
    ring_extended = is_finger_extended(lm, 16, 14)   # Manis
    pinky_extended = is_finger_extended(lm, 20, 18)  # Kelingking
    
    # Hitung jumlah jari yang terbuka
    fingers_up = sum([index_extended, middle_extended, ring_extended, pinky_extended])
    if thumb_extended:
        fingers_up += 1
    
    # Deteksi gesture spesifik
    # 1. FINGER (hanya telunjuk yang terbuka)
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "finger"
    
    # 2. MOUTH (tangan dekat mulut)
    if pose_result.pose_landmarks:
        nose = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE.value]
        wrist = lm[0]
        if distance(wrist, nose) < 0.15:
            return "mouth"
    
    # 3. PRAY (dua tangan bertemu)
    if hands_result.multi_hand_landmarks and len(hands_result.multi_hand_landmarks) == 2:
        hand1_wrist = hands_result.multi_hand_landmarks[0].landmark[0]
        hand2_wrist = hands_result.multi_hand_landmarks[1].landmark[0]
        if distance(hand1_wrist, hand2_wrist) < 0.1:
            return "pray"
    
    # 4. PHONE (tangan di dekat telinga)
    if pose_result.pose_landmarks:
        ear = pose_result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR.value]
        wrist = lm[0]
        if distance(wrist, ear) < 0.15:
            return "phone"
    
    return "idle"

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_result = pose.process(rgb)
        hands_result = hands.process(rgb)

        # Deteksi gesture
        gesture = detect_gesture(hands_result, pose_result)

        # Tampilkan gambar reaksi
        reaction_img = reactions.get(gesture, reactions["idle"])
        if reaction_img is not None:
            reaction_img = cv2.resize(reaction_img, (w, h))
            combined = cv2.hconcat([frame, reaction_img])
        else:
            combined = frame

        # Gambarkan landmarks
        if pose_result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, pose_result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if hands_result.multi_hand_landmarks:
            for hand_landmarks in hands_result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame, f"Gesture: {gesture}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Gesture Reaction", combined)

        if cv2.waitKey(1) & 0xFF == 27:  
            break

        

cap.release()
cv2.destroyAllWindows()