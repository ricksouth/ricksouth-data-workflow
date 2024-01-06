# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "membership"))
import update_membership_data

def main():
    print("Starting the Python automated workflow.")

    rootpath = os.path.dirname(sys.argv[0])

    update_membership_data.main(rootpath)

    return

if __name__ == "__main__":
    main()