from station_base import RailwayStation
import time

def main():
    s8 = RailwayStation("Station 8", ["Track 4", "Track 12", "Track 19", "Track 20", "Track 21", "Track 22", "Track 23", "Track 26", "Track 29"])
    try:
        while True:
            track = input("Enter track (4/12/19/20/21/22/23/26/29) for Station 8 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["4", "12", "19", "20", "21", "22", "23", "26", "29"]:
                print("Invalid track for Station 8")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s8.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s8.disconnect()

if __name__ == "__main__":
    main()
