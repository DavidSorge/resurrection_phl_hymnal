# Resurrection PHL Hymnal

For this mini-project, I'm aiming to create a customized hymnal for use by small groups at my church, [Resurrection PHL](https://www.resurrectionphl.org/).

The church has a unique devotion to cultivating art and artists, and as such has an atypical musical repertoire, so a custom hymnbook makes more sense for this church than many others.

Initially, I used a web-scraper to get pdf copies of archived bulletins from the church's website, but upon request, was able to get the original archive of bulletins from the pastor.

The python scripts in this folder aid in the process of extracting the songs from the bulletins so that they can be assembled into a hymnal.

- `image_extractor.py`: creates a gif image for each page of the bulletin pdf files
- `score_extractor.py`: opens each gif, splits them on whitespace, and saves any that have four horizontal lines (as in a line of a musical score)

To do:

- [x] turn pdfs into images
- [x] open images, extract scores
- [ ] de-duplicate songs
- [ ] create physical songbook pdf
- [ ] create web-app version of songbook 