<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/pratyushvshah/TheFirstFloor">
    <img src="logo.ico" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">TheFirstFloor™</h3>

  <p align="center">
    A Poor Man's Spotify
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#todo">TODO</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

TheFirstFloor™ is aimed towards creating a CLI for managaing your music requirements. It is a simple, easy to use, and lightweight music player. It is a work in progress and is not yet complete. Refer to [TODO](#todo) for more information.

### Features

1. Login/Create user (Supporting hashing of passwords)
1. Stream songs online
1. Download songs from all major sources (YouTube, Spotify, SoundCloud, etc.) as well and some miscellaneous sites
1. Search for podcasts
1. Listen to radio stations all around the world
1. Identify music from media files or by recording
1. Strong error logging to help with future debugging

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

1. Python
1. PostgreSQL

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

1. Use the `log.sql` file in the directory get the commands through which you can create your own database.
1. You can host the database on a platform like [bit.io](https://bit.io/).
1. After hosting the database, Make a `filekeys.py` file in the directory and add the following lines:

```python
postgresqluri = "<YOUR POSTGRESQL DATABASE URI>"
referralkey = "<YOUR REFERRAL KEY>"
spotclientid = "<YOUR SPOTIFY CLIENT ID>"
spotsecretid = "<YOUR SPOTIFY CLIENT SECRET ID>"
```

4. You can get your Spotify Client ID and Secret ID by following the steps [here](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/).
1. Voila! You can now use this CLI!

### Prerequisites

1. You must download ffmpeg from [here](https://ffmpeg.org/download.html) and extract it to the root of the C directory.
1. You must then add ffmpeg to your PATH environment variable.
1. Go to the directory where you downloaded the project and run the following command in the terminal:

```bash
pip install -r requirements.txt
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

There's no instructions, just run `main.py` in your terminal and follow the instructions on the screen!
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## TODO

- [ ] Make a playlist handler to play store a user's playlist and give option to download and play locally
- [ ] Make a better UI for streaming music, particularly the searching aspect
- [ ] Make a better UI for radio tracks to display 15 countries/stations at a time
- [ ] Stream podcasts in the program rather than redirecting
- [ ] Make a help menu

See the [open issues](https://github.com/pratyushvshah/TheFirstFloor/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Pratyush Shah - <a href = "mailto: pratyushvshah@gmail.com">Email</a>, [LinkedIn](https://www.linkedin.com/in/pratyushvshah/)

Project Link: [https://github.com/pratyushvshah/TheFirstFloor](https://github.com/pratyushvshah/TheFirstFloor)

<p align="right">(<a href="#top">back to top</a>)</p>
