# Astral star map 2
Refactored version of its predecessor.

Renders around a million stars from the GAIA database through ecliptic or galactic cordinates, into a large high quality image.

Planning to implement panaroma projections to fix previous issues.
Planning to add UI.
Added cordinate axis, config class, cordinate selection, etc.

## Required resources
Requires atleast the `render\static\data\binaries\all_stars` turtle binary file.
Is too big for my current github plan, may be downloaded form google drive [here](https://drive.google.com/file/d/17sYW8ccLNKOs35wMnL6D3INtvtmAKITI/view?usp=sharing).

## Sample

mple image files (32k google drive)
![Ra Dec system (celestial)](https://drive.google.com/file/d/1ucUdvCSDz5O7Onc_7dyFeHvNmEsUnVDm/view?usp=sharing)
![Galactic system](https://drive.google.com/file/d/1w-9C3yD5aeLCFIQeoaAdqsovtH0L4Cmb/view?usp=sharing)



High quality render + (RA DEC system)
![](sample/sample1.png)

Simple render + (galactic cordinate system)
![](sample/sample2.png)


At 32k quality:
Simple render ~10 min.
High qualtiy ~1 hour with single thread, ~10 min with multiprocessing. 
Note heavily subj to system specifications and config settings. 

Change config settings in `support/configsys.pt`.

