# RT_Assignment1_Amani_Ghomrani

The solution demonstrates a basic robotic navigation and manipulation behavior, where the robot is programmed to pick up markers and bring them to a specific reference point. The reference token helps guide the robot's movements during the process.

## Pseudo code
----------------------

```bash
# RT_Assignment1_Amani_Ghomrani

# Pseudo code of the program

Initialize picked_up_markers list
Initialize reference_token and ref_token_code

Function drive(speed, seconds)
    Set linear velocity
    Sleep for seconds
    Stop motors

Function turn(speed, seconds)
    Set angular velocity
    Sleep for seconds
    Stop motors

Function find_token()
    While no markers are seen
        Turn left to look for markers
    For each marker in seen markers
        If marker is not picked up and not reference token
            Update dist, rot_y, and marker
        Else if marker is picked up or reference token
            Print that the token is already picked or is the reference code
    If dist is still 100 or marker is in picked_up_markers or is the reference code
        Return None, -1, -1
    Else
        Return marker, dist, rot_y

Function save_reference_token()
    Call find_token()
    If marker is found
        Save marker as reference_token
        Save marker's code as ref_token_code
        Print "Reference token saved:" and ref_token_code
    Else
        Print "No token found to save as reference."

Function displace_token()
    For each marker in seen markers
        If marker is the reference token
            Update reference_token details
            Set found_it to True
            Break
    If found_it
        While found_it is True
            Move and update the cordinations of the reference token
            If robot is close to reference token by d_th + 0.4
                Release the token
                exit the while-loop
            Else
                Keep moving towards the reference token by calling displace_token() function (using recursion)
    Else
        move and turn a bit for cleared view
        Call displace_token()

Main code
    look for a reference token
    loop
        Call find_token()
        If no tokens are seen
            turn the robot for clearer view by Calling turn(+10, 1)
        Else if robot is close enough to token
            grab the token
            If token is grabbed
                take the held token to reference token using displace_token() function
                move back and turn
                Add token's code to picked_up_markers
        Else
            continue to loop
        move towards the tergeted token
        If the robot picked up all tokes
            Break from the loop and stop

```
