from station_base import RailwayStation
import time

def main():
    s1 = RailwayStation("Station 1", ["Track 1", "Track 5", "Track 20", "Track 24"])
    try:
        while True:
            track = input("Enter track (1/5/20/24) for Station 1 or 'q' to quit: ")
            if track.lower() == 'q':
                break
            if track not in ["1", "5", "20", "24"]:
                print("Invalid track for Station 1")
                continue
            train_time = int(input("Enter train journey time (minutes): "))
            s1.send_train(f"Track {track}", train_time)
            time.sleep(1)  # Small delay between messages
    finally:
        s1.disconnect()

if __name__ == "__main__":
    main()
