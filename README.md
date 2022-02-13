# pdf4gmk

Tool that extracts a given number of pages from one / more PDF files, converts them into images and then concatenates these images into one single-page PDF file. Created for [GMKdesign](https://gmkdesign.sk/).

### Install / Build

* Install Docker (Docker Desktop on Windows / Docker package for your respective Linux distribution).

* Clone / download the contents of this repository into a folder on your PC.

* Navigate to the folder and run:

  ```sh
  docker build -t pdf4gmk .
  ```

### Usage

* On Windows, run:

  ```sh
  docker run -v "%cd%":/app/output pdf4gmk -h
  ```

* On Linux, run:

  ```sh
  docker run -v "$(pwd)":/app/output pdf4gmk -h
  ```
