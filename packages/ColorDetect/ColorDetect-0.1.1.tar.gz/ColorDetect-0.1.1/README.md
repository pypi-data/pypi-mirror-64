# color-detect


![Python](https://img.shields.io/badge/Python-3.7-green)
![Release](https://img.shields.io/github/v/release/MarvinKweyu/ColorRecognition?include_prereleases)
[![CircleCI](https://circleci.com/gh/MarvinKweyu/ColorDetect.svg?style=svg)](https://circleci.com/gh/MarvinKweyu/ColorDetect)
![Downloads](https://img.shields.io/github/downloads/MarvinKweyu/ColorRecognition/total?style=flat)

ColorDetect works to identify different color candies in an image.



### Table of Contents

 [ Basic Usage](#Setup)
 
 [ Download](#Download)

 [Contributions](#Contributions)

 [License](#License)

### Basic Usage
```bash
from colordetect import ColorDetect


user_image = ColorDetect(<path_to_image>)
user_image.get_color_count()
user_image.save_picture(<storage_path>,<image_name>)

```

Resultant image is stored in the string `storage_path` of choice with the `image_name` which will default to the current location and **out.jpg** respectively by default.


 *A sample output.*


![Sample image](./images/out.jpg)


#### Tests
To run tests:
```bash
pytest tests --image ./tests/test_files/image2.jpg
```


### Download
Get the latest release from the [release page](https://github.com/MarvinKweyu/ColorDetect/releases)


### Contributions

Contributions are welcome.
Do remember to take a look at the project [contribution guidelines](./CONTRIBUTING.md)


#### ToDo

- [ ]  Allow color count in videos.
