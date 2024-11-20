from station_base import RailwayStation
import time

def main():
    s2 = RailwayStation("Station 2", ["Track 2", "Track 3", "Track 14", "Track 21"])
    try:
        while True:
            track = input("Enter track (2/3/14/21) for Station 2 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["2", "3", "14", "21"]:
                print("Invalid track for Station 2")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s2.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s2.disconnect()

if __name__ == "__main__":
    main()
