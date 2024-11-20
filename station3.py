from station_base import RailwayStation
import time

def main():
    s3 = RailwayStation("Station 3", ["Track 1", "Track 4", "Track 6", "Track 10", "Track 18"])
    try:
        while True:
            track = input("Enter track (1/4/6/10/18) for Station 3 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["1", "4", "6", "10", "18"]:
                print("Invalid track for Station 3")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s3.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s3.disconnect()

if __name__ == "__main__":
    main()
