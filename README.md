# plugin.context.exportto

# Addon is no longer supported, no updates will be available, left here for archival purposes.

Export video items in Kodi Addons to library as .strm files.

Utilizes Kodi's VFS so should support any path Kodi can write to but has only been tested on local and smb://

Usage:
  Right click on a TV Show or Movie item within a video plugin, select 'Export to Library'
  A file will be written in the TV or Movie path defined in config depending on Video Type
  
    Defaults to special://home which is Kodi's data folder
   
   A convenience item was added to the context menu labeled "Update Library" which does what it says, asks Kodi to update the video library.
   
   Ensure that the paths set in config are Writeable
   
   Ensure that the paths set in config are added to Kodi as library paths with the appropriate Content set if you want Kodi to scan the exported strm files.
   
Filenames are formatted to be as safe as possible with Windows however only English titles have been tested.
  
  Characters in other character sets (languages) may break functionality,
  
File output patterns are as follows:

  TV Shows:
  
    Show Name, Season 1, Episode 1, "Episode Title" will format as TVPATH/Show.Name/Show.Name.S01E01.Episode.Title.strm
  Movies:
  
    Movie Title Released in 2002 will format as MOVIEPATH/Movie.Title.2002.strm
    
  Ampersand '&' is replaced with lowercase 'and', regex used to remove Non-Alphanumeric characters.
  
  Spaces are replaced with periods.
  
  These are set to help reduce invalid characters for some operating systems and increase the scan detection chance by Kodi
  
This project is made available to the public as a courtesy to help the community, there is no warranty implied or otherwise, as with anything
  you download from the internet, you take responsibility for your own actions.
