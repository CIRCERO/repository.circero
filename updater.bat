@echo off

Echo .svn>exclude.txt
Echo .git>>exclude.txt
Echo %1\media>>exclude.txt
Echo %1\themes>>exclude.txt

md BUILD\%1\media\

ECHO ----------------------------------------
Echo Building main skin XBT
ECHO ----------------------------------------

START /B /WAIT TexturePacker -dupecheck -input %1\media -output \%1\media\Textures.xbt

ECHO ----------------------------------------
Echo Finished building main skin XBT
if exist %1\themes (
    Echo Building theme skin XBT Files
    ECHO ----------------------------------------
    for /f "tokens=*" %%f in ('dir /b/ad %1\themes') do START /B /WAIT \TexturePacker -dupecheck -input %1\themes\%%f -output \%1\media\%%f.xbt
    Echo Finished Building theme skin XBT Files
)

ECHO ----------------------------------------
Echo Copying other files
ECHO ----------------------------------------

for /f "tokens=*" %%c in ('dir /b/ad %1') do xcopy "%1\%%c" "BUILD\%1\%%c" /Q /S /I /Y /EXCLUDE:exclude.txt
for /f "tokens=*" %%c in ('dir /b/a-d %1') do copy %1\%%c "BUILD\%1\%%c"

del exclude.txt

FOR /F "skip=1 Tokens=1 Delims== " %%V IN ('FIND "    version=" "BUILD\%1\addon.xml"') DO SET Version=%%~V

ECHO ----------------------------------------
ECHO Current skin version is %Version%
ECHO ----------------------------------------

cd BUILD
        /zips -r -q %1-%Version%.zip %1

ECHO ----------------------------------------
ECHO Moving files to repository
ECHO ----------------------------------------

if exist "zips\%1\" rmdir "zips\%1\" /S /Q
md "zips\%1\"
copy "%1-%Version%.zip" "zips\%1\"
copy "%1\fanart.jpg" "zips\%1\fanart.jpg"
copy "%1\icon.png" "zips\%1\icon.png"
copy "%1\addon.xml" "zips\%1\addon.xml"
copy "%1\changelog.txt" "zips\%1\changelog-%Version%.txt"

ECHO ----------------------------------------
ECHO Removing BUILD folder
ECHO ----------------------------------------

cd ..
rmdir BUILD /S /Q

ECHO ----------------------------------------
ECHO Generating addons.xml and addons.xml.md5
ECHO ----------------------------------------

F:
cd 
python /kevng/repository.circero/_repo_xml_generator.py

pause