'''
    Cumination
    Copyright (C) 2021 Team Cumination

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
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('xozilla', '[COLOR yellow]Xozilla[/COLOR]', 'https://www.xozilla.com/', 'https://i.xozilla.com/images/logo.png', 'xozilla')


@site.register(default_mode=True)
def Main():
    site.add_dir('[COLOR yellow]Categories[/COLOR]', site.url + 'categories/', 'Categories', site.img_cat)
    site.add_dir('[COLOR yellow]Categories - TOP RATED[/COLOR]', site.url + 'categories/', 'CategoriesTR', site.img_cat)
    site.add_dir('[COLOR yellow]Channels[/COLOR]', site.url + 'channels/', 'Channels', site.img_cat)
    site.add_dir('[COLOR yellow]Search[/COLOR]', site.url + 'search/', 'Search', site.img_search)
    List(site.url + 'latest-updates/')
    utils.eod()


@site.register()
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile(r'<a href="([^"]+)" class="item.+?vthumb=.+?thumb="([^"]+)".+?"duration">([^<]+)</div>.+?class="title">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, duration, name in match:
        name = utils.cleantext(name)
        site.add_download_link(name, videopage, 'Playvid', img, name, duration=duration)

    nextp = re.compile(r'class="next"><a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    if nextp:
        np = re.compile(r':(\d+)">Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        if np:
            np = np[0]
        else:
            np = ''
        lp = re.compile(r':(\d+)">Last', re.DOTALL | re.IGNORECASE).findall(listhtml)
        if lp:
            lp = '/' + lp[0]
        else:
            lp = ''
        nextp = nextp[0]
        if nextp.startswith('/'):
            nextp = site.url[:-1] + nextp
        else:
            match = re.compile(r'class="next">.+?data-block-id="([^"]+)"\s+data-parameters="([^"]+)">Next<', re.DOTALL | re.IGNORECASE).findall(listhtml)
            if match:
                dbi, dp = match[0]
                dp = dp.replace(':', '=').replace(';', '&').replace('+from_albums', '')
            nextp = '{0}?mode=async&function=get_block&block_id={1}&{2}'.format(url.split('?mode')[0], dbi, dp)
        site.add_dir('Next Page ({}{})'.format(np, lp), nextp, 'List', site.img_next)
    utils.eod()


@site.register()
def Categories(url):
    try:
        cathtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('a href="([^"]+)">([^<]+)<span class="rating">', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in sorted(match, key=lambda x: x[1]):
        site.add_dir(name, catpage, 'List', '')
    utils.eod()


@site.register()
def CategoriesTR(url):
    try:
        cathtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('"item" href="([^"]+)" title="([^"]+)".+?src="([^"]+)".+?i>([^<]+)videos<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name, img, count in sorted(match, key=lambda x: x[1]):
        name = utils.cleantext(name) + "[COLOR deeppink] " + count + "[/COLOR]"
        site.add_dir(name, catpage, 'List', img)
    utils.eod()


@site.register()
def Channels(url):
    try:
        cathtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('"item" href="([^"]+)" title="([^"]+)".+?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name, img in sorted(match, key=lambda x: x[1]):
        name = utils.cleantext(name)
        site.add_dir(name, catpage, 'List', img)
    utils.eod()


@site.register()
def Playvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download, '', 'Download:.+?href="([^"]+)"')

    videopage = utils.getHtml(url, '')
    match = re.compile(r'Download:(.+?)<\/div>', re.DOTALL | re.IGNORECASE).findall(videopage)
    srcs = re.compile('href="([^"]+)".+?>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match[0])
    sources = {}
    for videourl, quality in srcs:
        if videourl:
            sources[quality] = videourl
    videourl = utils.selector('Select quality', sources, setting_valid='qualityask', sort_by=lambda x: int(x.split('x')[0]), reverse=True)
    if videourl:
        vp.play_from_direct_link(videourl)


@site.register()
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        site.search_dir(url, 'Search')
    else:
        title = keyword.replace(' ', '-')
        searchUrl = searchUrl + title + '/'
        List(searchUrl)
