from station_base import RailwayStation
import time

def main():
    s5 = RailwayStation("Station 5", ["Track 10", "Track 12", "Track 13", "Track 16"])
    try:
        while True:
            track = input("Enter track (10/12/13/16) for Station 5 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["10", "12", "13", "16"]:
                print("Invalid track for Station 5")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s5.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s5.disconnect()

if __name__ == "__main__":
    main()
