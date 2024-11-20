from station_base import RailwayStation
import time

def main():
    s4 = RailwayStation("Station 4", ["Track 5", "Track 6", "Track 7", "Track 9", "Track 15", "Track 22"])
    try:
        while True:
            track = input("Enter track (5/6/7/9/15/22) for Station 4 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["5", "6", "7", "9", "15", "22"]:
                print("Invalid track for Station 4")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s4.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s4.disconnect()

if __name__ == "__main__":
    main()
