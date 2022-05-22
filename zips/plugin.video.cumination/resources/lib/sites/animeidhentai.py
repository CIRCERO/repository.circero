'''
    Cumination
    Copyright (C) 2018 Whitecream

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


site = AdultSite("animeid", "[COLOR yellow]Animeid Hentai[/COLOR]", "https://animeidhentai.com", "ah.gif", "animeid")


@site.register(default_mode=True)
def animeidhentai_main():
    site.add_dir('[COLOR yellow]Uncensored[/COLOR]', '{0}/hentai/on-uncensored/'.format(site.url), 'animeidhentai_list', site.img_cat)
    site.add_dir('[COLOR yellow]Previews[/COLOR]', '{0}/genre/preview/'.format(site.url), 'animeidhentai_list', site.img_cat)
    site.add_dir('[COLOR yellow]Trending[/COLOR]', '{0}/trending/'.format(site.url), 'animeidhentai_list', site.img_cat)
    site.add_dir('[COLOR yellow]Search[/COLOR]', '{0}/?s='.format(site.url), 'animeidhentai_search', site.img_search)
    animeidhentai_list('{0}/genre/2020/'.format(site.url))


@site.register()
def animeidhentai_list(url):
    listhtml = utils.getHtml(url)
    match = re.compile(r'<article.+?title">([^<]+).+?meta">(.+?)</div.+?src="([^"]+).+?href="([^"]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for name, other, img, video in match:
        if 'uncensored' in other.lower() or 'uncensored' in name.lower():
            name = name.replace('Uncensored', '') + " [COLOR yellow][I]Uncensored[/I][/COLOR]"
        site.add_download_link(utils.cleantext(name), video, 'animeidhentai_play', img, name)

    next_page = re.compile(r'href="([^"\s]+)"\s*class="next', re.DOTALL | re.IGNORECASE).search(listhtml)
    if next_page:
        site.add_dir('Next Page', next_page.group(1), 'animeidhentai_list', site.img_next)

    utils.eod()


@site.register()
def animeidhentai_search(url, keyword=None):
    if not keyword:
        site.search_dir(url, 'animeidhentai_search')
    else:
        title = keyword.replace(' ', '+')
        url += title
        animeidhentai_list(url)


@site.register()
def animeidhentai_play(url, name, download=None):
    vp = utils.VideoPlayer(name, download)
    vp.progress.update(25, "[CR]Loading video page[CR]")
    videopage = utils.getHtml(url, '')
    r = re.compile(r'<iframe\s*src="([^"]+)', re.DOTALL | re.IGNORECASE).search(videopage)
    if r:
        vp.play_from_link_to_resolve(r.group(1))
    else:
        vp.progress.close()
        return
