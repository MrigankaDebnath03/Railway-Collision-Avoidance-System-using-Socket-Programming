from station_base import RailwayStation
import time

def main():
    s9 = RailwayStation("Station 9", ["Track 3", "Track 9", "Track 24", "Track 25", "Track 26", "Track 30"])
    try:
        while True:
            track = input("Enter track (3/9/24/25/26/30) for Station 9 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["3", "9", "24", "25", "26", "30"]:
                print("Invalid track for Station 9")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s9.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s9.disconnect()

if __name__ == "__main__":
    main()
