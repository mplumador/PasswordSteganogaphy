# What is this?
I recently saw [this clip](https://www.youtube.com/shorts/Udf44K6rt-E) of someone using steganography as a password manager.
I was curious enough to build a basic version.

This will download a random image from various subreddits, generate a secure password, then will encode or decode that password into/from the downloaded image.

# Quick Start

# Project Setup
1. Python 3.6+ is required (to make use of the secrets builtin)
2. A reddit app and developer account are needed
3. `pip install -r requirements.txt`

## Reddit API handling

1. Create a reddit app at https://www.reddit.com/prefs/apps/
2. Follow the instructions at https://www.reddit.com/wiki/api/
3. Create a .env-file in this parent directory with the valuest supplied from the .env-template
4. If you don't already have a refresh token, get one using the helper script from PRAW `python fetchRfreshToken.py`
5. Add the refresh token to your .env file
6. You are now set up to pull images from various subreddits


## Password Generation

By default, password generation is set to 16 characters, including a-z, A-Z, 0-9, as well as !"#$%&\'()*+,-./;<=>?@[\\]^_`{|}~

There is currently no configuration file for this yet.

To create a password, run `python pwStega.py`

### Workflow

 * After running `python pwStega.py` you will have two options: Encoding or Decoding.
   * Enter 1 for encoding (create a password + grab an image)
     * You will be asked a series of questions consisting of:
       * `What site/app is this password for?`
         * This will be the name of the file and will overwrite any existing files with this name
         * Be careful not to overwrite your passwords if you already have a file created.
       * `What username are you using for this site?`
         * This will get encoded into the image along with the password
       * `Do you want to regenerate a different password?`
         * This generates a new password for this creation
       * `Input the starting coordinates for the data: `
         * This will be used to determine where in the image your username/password combo will be encoded. It is required to decode as well 
         * This allows user's to have dynamic "salts" across their images thus making the decode function more robust and not the same for everyone
         * Recommended to stick to one that you'll remember, as forgetting this information for a given image will mean you have to brute-force the password or reset it.
       * After that, an image will be saved in the /passwords/ folder (not configurable atm) with your credentials tucked away in the data.
   * Enter 2 for decoding (retrieve your username and password combo from an image)
     * You will need your encoding coordinate to retrieve info easily.