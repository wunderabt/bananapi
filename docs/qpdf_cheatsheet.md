# qpdf cheat sheet

## Appending

Append pdfs to an existing PDF

```bash
qpdf --empty --pages "$@" -- $1.tmp && mv $1.tmp $1
```

## Book scan

On scanners with an automatic document feeder double sided documents can often only be scanned single sided. I tend to scan the odd pages 1, 3, 5, .. in the first go, and scan the even pages in reverse order .., 6, 4, 2.
To get the document back in order here's my recipe:

### append pages

In case the feeder can't take all pages in one go, append all the odd pages:

```bash
qpdf --empty --pages ub.pdf ub0001.pdf ub0002.pdf ub0003.pdf -- book_ascending_pages.pdf
```

the same for the reverse ordered pages

```bash
qpdf --empty --pages ub0004.pdf ub0005.pdf ub0006.pdf ub0007.pdf -- book_descending_pages.pdf
```

### reverse order

Correct page order for the reverse scanned batch

```bash
qpdf book_descending_pages.pdf --pages . z-1 -- book_ascending_pages_2.pdf
```

### correct orientation

On this particular book, the cover page was A4, the following pages had 2x A5 pages each, rotated 90°. Rotate all pages back except for the cover page.

```bash
qpdf book_ascending_pages.pdf --rotate=90:2-z -- book_ascending_pages_odd.pdf
qpdf book_ascending_pages_2.pdf --rotate=90:2-z -- book_ascending_pages_even.pdf
```

### splice odd and even pages

```bash
qpdf --collate --empty --pages book_ascending_pages_odd.pdf book_ascending_pages_even.pdf -- book.pdf
```
(*Note*: you probably can combine all of the above into a single collate command)

### OCR

```bash
ocrmypdf -l eng book.pdf book_ocr.pdf
```

### reduce size / resolution

on less important documents that are just read on the screen I reduce the pdf size

```bash
gs -q \
   -dNOPAUSE \
   -dBATCH \
   -dSAFER \
   -dPDFA=2 \
   -dPDFACompatibilityPolicy=1 \
   -dSimulateOverprint=true \
   -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.3 \
   -dPDFSETTINGS=/ebook \
   -dEmbedAllFonts=true \
   -dSubsetFonts=true \
   -dAutoRotatePages=/None \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=150 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=150 \
   -dMonoImageDownsampleType=/Bicubic \
   -dMonoImageResolution=150 \
   -sOutputFile=output.pdf \
   input.pdf
```
