from __future__ import print_function
import time
from sr.robot import *

picked_up_markers = []
reference_token = None
ref_token_code = 0

a_th = 2.0
d_th = 0.4

R = Robot()

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token():
    global picked_up_markers, ref_token_code
    dist = 100
    markers = R.see()

    while len(markers) == 0:
        turn(-25, 0.7)
        print("I have turned to the left to look for markers")
        markers = R.see()

    print("I can see", len(markers), "markers:")
    marker = None

    for token in markers:
        if token.dist < dist and (token.info.code not in picked_up_markers) and (token.info.code != ref_token_code):
            dist = token.dist
            rot_y = token.rot_y
            marker = token
        elif (token.info.code in picked_up_markers) or (token.info.code == ref_token_code):
            print("I already picked this token or it is the reference code")
            marker = token

    if (dist == 100 and marker.info.code in picked_up_markers) or (marker.info.code == ref_token_code):
        return None, -1, -1
    else:
        return marker, dist, rot_y

def save_reference_token():
    global reference_token, ref_token_code
    marker, _, _ = find_token()
    if marker:
        reference_token = marker
        ref_token_code = reference_token.info.code
        print("Reference token saved:", ref_token_code)
    else:
        print("No token found to save as reference.")

def displace_token():
    global reference_token
    markers = R.see()
    found_it = False
    for marker in markers:
        if reference_token.info.code == marker.info.code:
            reference_token = marker
            found_it = True
            break
        else: 
            continue
    if found_it:
    	while(found_it):
		dist = reference_token.dist
		rot_y = reference_token.rot_y
		if dist < d_th + 0.4:
		    print("I arrived to referance!")
		    R.release()
		    print("I relesed the token")
		    found_it = False
		    break
		else:
		    print("Aww, I'm not close enough.")

		if -a_th <= rot_y <= a_th:
		    print("Ah, that'll do.")
		    drive(25, 0.5)
		elif rot_y < -a_th:
		    print("Left a bit...")
		    turn(-2, 0.5)
		elif rot_y > a_th:
		    print("Right a bit...")
		    turn(2, 0.5)
		displace_token()
    else:
        print("I don't see the ref token")
        drive(10, 1)
        turn(10, 1)
        displace_token()


# Main code
print("I am starting the main code")
save_reference_token()
print("The reference token is:", reference_token)

while True:
    
    token, dist, rot_y = find_token()

    if dist == -1:
        print("I don't see any token!!")
        turn(+10, 1)
    elif dist < d_th:
        print("Found it!")
        if R.grab():
            print("Gotcha!")
            displace_token()
            drive(-40, 2.5)
            turn(-30, 2)
            picked_up_markers.append(token.info.code)
            print("The picked up markers", picked_up_markers)

    else:
        print("Aww, I'm not close enough.")

    if -a_th <= rot_y <= a_th:
        print("Ah, that'll do.")
        drive(25, 0.5)
    elif rot_y < -a_th:
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(2, 0.5)
    if len(picked_up_markers) == 5:
    	print("AAAAND I'm done! time to rest")
    	break
