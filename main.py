import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "membership"))
import update_membership_data

def main():
    print("Starting the Python automated workflow.")

    update_membership_data.main()

    return

if __name__ == "__main__":
    main()