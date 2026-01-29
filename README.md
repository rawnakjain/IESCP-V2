# IESCP V2

<video width="320" height="240" controls>
  <source src="https://drive.google.com/file/d/1ZRv4HtxRnImPunedjp-xHazl3Iz0uVZc/view?usp=drive_link" type="video/mp4">
</video>


to run the project do:

- cd into backend `cd backend`
- run the scripts `./start_redis`, `./start_celery`, `./start_beat`, `./start_mailhog`, `python3 app.py`

    These scripts will set up environment of backend and run all services
- cd into frontend folder `cd frontend`
- run `npm i` to install all packages
- run `npm run serve` to run development server
- go to `localhost:8080` to see app
