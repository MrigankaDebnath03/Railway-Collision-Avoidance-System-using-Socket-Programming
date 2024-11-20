from station_base import RailwayStation
import time

def main():
    s10 = RailwayStation("Station 10", ["Track 13", "Track 28", "Track 29", "Track 30"])
    try:
        while True:
            track = input("Enter track (13/28/29/30) for Station 10 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["13", "28", "29", "30"]:
                print("Invalid track for Station 10")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s10.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s10.disconnect()

if __name__ == "__main__":
    main()
