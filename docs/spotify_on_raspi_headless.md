# spotify on HiFiBerry headless

1. install [raspotify](https://dtcooper.github.io/raspotify/), see [blog](https://www.hifiberry.com/blog/spotify-connect-the-easy-way/)
1. check which sound device is the HiFiBerry `aplay -l`
1. set that card number as default in `/usr/share/alsa/alsa.conf` - for card #1 like so
    ```
    defaults.ctl.card 1
    defaults.pcm.card 1
    ```
