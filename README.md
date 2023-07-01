# ricksouth-data-workflow
A repository containing Python scripts which will automatically update data files via Github Actions. 

 _Should_ run every hour, though Github Actions can delay cron jobs when the queue is busy. Pushes only when changes are found.

### Currently used for:
  - Receiving memberships from Github Sponsors, Ko-Fi and Patreon. Output set to a JSON file.
    - For more details check out [ricksouth.com/donate](https://ricksouth.com/donate/).
  - Generating a historical feed, containing new members and the day of donation.
    - Used for the feed located at [serilum.com/feed](https://serilum.com/feed).
