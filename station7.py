from station_base import RailwayStation
import time

def main():
    s7 = RailwayStation("Station 7", ["Track 2", "Track 7", "Track 18", "Track 19", "Track 25"])
    try:
        while True:
            track = input("Enter track (2/7/18/19/25) for Station 7 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["2", "7", "18", "19", "25"]:
                print("Invalid track for Station 7")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s7.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s7.disconnect()

if __name__ == "__main__":
    main()
