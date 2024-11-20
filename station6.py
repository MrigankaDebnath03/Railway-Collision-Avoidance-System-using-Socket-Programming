from station_base import RailwayStation
import time

def main():
    s6 = RailwayStation("Station 6", ["Track 14", "Track 15", "Track 16", "Track 23", "Track 28"])
    try:
        while True:
            track = input("Enter track (14/15/16/23/28) for Station 6 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["14", "15", "16", "23", "28"]:
                print("Invalid track for Station 6")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s6.send_train(f"Track {track}", train_time)
            time.sleep(1)
    finally:
        s6.disconnect()

if __name__ == "__main__":
    main()
