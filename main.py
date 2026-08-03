import random, cv2, time, serial, math

from custom_timer import CustomTimer
from face_and_hand_reading import HandDetection, FaceDetection



# def random_start_tracker() -> tuple:
#     trackers = ["face", "hand"]
#     set_attacker = ""

#     set_tracked = random.choice(trackers)
#     if set_tracked == "face":
#         set_attacker = "bot"
#     elif set_tracked == "hand":
#         set_attacker = "man"
    
#     return set_tracked, set_attacker


def bot_decision(past_bot_dirs) -> str:

    directions = {"UP", "DOWN", "LEFT", "RIGHT"}

    available_dirs = list(directions - past_bot_dirs)

    return random.choice(available_dirs)


def round_decisiveness(man_dir, bot_dir) -> bool:

    if man_dir == bot_dir:
        return True
    
    return False


def switch_roles(curr_tracker) -> tuple:

    set_curr_tracker, set_attacker = "", ""

    if curr_tracker == "hand":
        set_curr_tracker, set_attacker = "face", "bot"
    elif curr_tracker == "face":
        set_curr_tracker, set_attacker = "hand", "man"

    return set_curr_tracker, set_attacker



def main() -> None:
    hand_detection, face_detection = HandDetection(), FaceDetection()

    arduino_serial = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600)
    time.sleep(5)

    # curr_tracker, attacker = random_start_tracker()
    curr_tracker, attacker = "hand", "man"
    if curr_tracker == "hand":
        tracker = hand_detection
    else:
        tracker = face_detection
    man_dir = "NONE"

    round_interval_time = 5
    dir_gather_moment_time = 2
    transition_time = 0.5

    custom_timer = CustomTimer()

    past_bot_dirs = set()

    strike_count, strike_out_count = 0, 2
    
    #only for debugging and playing around:
    last_read_time = 0

    servo_reset = "RESET"

    cap = cv2.VideoCapture(index = 1)        #camera switch
    start_time = time.time()
    begin_input = ""


    while True:

        if begin_input != "BEGIN":
            begin_input = input("INPUT 'BEGIN' TO START: ")

        ret, frame = cap.read()
        if not ret:
            break
        timestamp_ms = int((time.time() - start_time) * 1000)
        
        custom_timer.resume()

        if custom_timer.elapsed() >= last_read_time + 1:
            countdown = (round_interval_time - math.floor(custom_timer.elapsed()) - 1)
            if countdown <= 0:
                print("GO!")
            else:
                print(countdown)
            last_read_time += 1

        man_dir_check, round_check = False, False
        bot_dir = "NONE"

        if custom_timer.elapsed() >= dir_gather_moment_time:
            man_dir_check = True

        result = tracker.update(frame, timestamp_ms, man_dir_check)
        tracker.draw(frame, result)
        cv2.imshow("", frame)


        if custom_timer.elapsed() >= round_interval_time:
            man_dir = tracker.get_direction()

            if man_dir == "NONE":
                print("TRY AGAIN!")
                time.sleep(1.5)
                custom_timer.reset()
                custom_timer.pause()
                last_read_time = 0
                continue

            bot_dir = bot_decision(past_bot_dirs)
            past_bot_dirs.add(bot_dir)
            print(f"Bot: {bot_dir}  vs  You: {man_dir}")
            arduino_serial.write((bot_dir + "\n").encode())
            custom_timer.reset()
            custom_timer.pause()
            last_read_time = 0
            time.sleep(transition_time)
            round_check = True

            if round_check and round_decisiveness(man_dir, bot_dir):
                strike_count += 1
                if attacker == "man":
                    print(f"BOT: STRIKE {strike_count} / {strike_out_count}")
                else:
                    print(f"YOU: STRIKE {strike_count} / {strike_out_count}")
                time.sleep(2)
                continue
            elif round_check and not round_decisiveness(man_dir, bot_dir):
                curr_tracker, attacker = switch_roles(curr_tracker)
                past_bot_dirs.clear()
                strike_count = 0

        arduino_serial.write((servo_reset + "\n").encode())

        if curr_tracker == "hand":
            tracker = hand_detection
        elif curr_tracker == "face":
            tracker = face_detection


        if strike_count == strike_out_count:
            if attacker == "man":
                print("Winner: YOU")
            else:
                print("Winner: BOT")

            time.sleep(10)
            break
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    cap.release()
    cv2.destroyAllWindows()
    arduino_serial.close()


if __name__ == "__main__":
    main()