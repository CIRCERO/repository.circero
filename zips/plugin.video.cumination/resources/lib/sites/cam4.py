'''
    Cumination
    Copyright (C) 2016 Whitecream

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import os
import sqlite3
import json
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('cam4', '[COLOR yellow]Cam4[/COLOR]', 'https://www.cam4.com', 'cam4.gif', 'cam4', True)
IOS_UA = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML%2C like Gecko) Mobile/15E148'}


@site.register(default_mode=True)
def Main():
    female = True if utils.addon.getSetting("chatfemale") == "true" else False
    male = True if utils.addon.getSetting("chatmale") == "true" else False
    couple = True if utils.addon.getSetting("chatcouple") == "true" else False
    trans = True if utils.addon.getSetting("chattrans") == "true" else False
    site.add_dir('[COLOR red]Refresh Cam4 images[/COLOR]', '', 'clean_database', '', Folder=False)
    if female:
        site.add_dir('[COLOR yellow]Females[/COLOR]', '&gender=female&broadcastType=female_group&broadcastType=solo&broadcastType=male_female_group', 'List', '', 1)
    if couple:
        site.add_dir('[COLOR yellow]Couples[/COLOR]', '&broadcastType=male_group&broadcastType=female_group&broadcastType=male_female_group', 'List', '', 1)
    if male:
        site.add_dir('[COLOR yellow]Males[/COLOR]', '&gender=male&broadcastType=male_group&broadcastType=solo', 'List', '', 1)
    if trans:
        site.add_dir('[COLOR yellow]Transsexual[/COLOR]', '&gender=shemale', 'List', '', 1)
    utils.eod()


@site.register(clean_mode=True)
def clean_database(showdialog=True):
    conn = sqlite3.connect(utils.TRANSLATEPATH("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".cam4s.com")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try:
                    os.remove(utils.TRANSLATEPATH("special://thumbnails/" + row[1]))
                except:
                    pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % ".cam4.com")
            if showdialog:
                utils.notify('Finished', 'Cam4 images cleared')
    except:
        pass


@site.register()
def List(url, page=1):
    if utils.addon.getSetting("chaturbate") == "true":
        clean_database(False)
    url = '{0}/directoryCams?directoryJson=true&online=true&url=true&orderBy=VIDEO_QUALITY&resultsPerPage=1500{1}'.format(site.url, url)
    listhtml = utils._getHtml(url, headers=IOS_UA)
    cams = json.loads(listhtml).get('users', {})
    for cam in cams:
        name = cam.get('username')
        videourl = "{0}/{1}".format(site.url, name)

        age = cam.get('age')
        if age:
            name = '{0} [COLOR deeppink][{1}][/COLOR]'.format(name, age)
        if cam.get('hdStream'):
            name = '{0} [COLOR limegreen][HD][/COLOR]'.format(name)
        img = cam.get('snapshotImageLink')
        if not img:
            img = cam.get('defaultImageLink')

        subject = ''
        if cam.get('viewers'):
            subject += 'Viewers: {}[CR]'.format(cam.get('viewers'))
        if cam.get('resolution'):
            subject += 'Resolution: {}[CR]'.format(cam.get('resolution'))
        if cam.get('sexPreference'):
            subject += '[CR]Sexual Preference: {}[CR]'.format(cam.get('sexPreference'))
        if cam.get('statusMessage'):
            subject += '[CR]{}[CR][CR]'.format(cam.get('statusMessage').encode('utf8') if utils.PY2 else cam.get('statusMessage'))
        if cam.get('showTags'):
            for tag in cam.get('showTags'):
                subject += '{}, '.format(tag)
            subject = subject[:-2]

        site.add_download_link(name, videourl, 'Playvid', img, subject, noDownload=True)

    utils.eod()


@site.register()
def Playvid(url, name):
    playmode = int(utils.addon.getSetting('chatplay'))
    camhtml = utils._getHtml(url, headers=IOS_UA)

    if playmode == 0:
        m3u8stream = re.search(r"hlsUrl:\s*'([^']+)", camhtml)
        if m3u8stream:
            videourl = '{0}|User-Agent={1}'.format(m3u8stream.group(1), IOS_UA['User-Agent'])
        else:
            utils.notify('Oh oh', 'Couldn\'t find a playable webcam link')
            return

    elif playmode == 1:
        data = re.search(r"flashData:\s*(.*?}),", camhtml)
        if data:
            data = json.loads(data.group(1))
            swfurl = data.get('playerUrl')
            data = data.get('flashVars')
            streamserver = data.get('videoAppUrl')
            modelname = data.get('videoPlayUrl')
            videourl = "{0} swfUrl={1} pageUrl={2} conn=S:null conn=S: conn=S:{3} playpath={3}".format(streamserver, swfurl, url, modelname)
        else:
            utils.notify('Oh oh', 'Couldn\'t find a playable webcam link')
            return

    vp = utils.VideoPlayer(name)
    vp.play_from_direct_link(videourl)
