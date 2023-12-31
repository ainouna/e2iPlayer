# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.comaddon import progress, VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.lib.util import Quote, cUtil
import re

SITE_IDENTIFIER = 'mesfilms'
SITE_NAME = 'Mes Films'
SITE_DESC = 'Mes Films - Films en streaming HD'

URL_MAIN = 'https://mesfilms.site/'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'

URL_SEARCH = (URL_MAIN + '?s=', 'showSearchResult')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'evaluations/?get=movies', 'showMovies')
MOVIE_CLASS = (URL_MAIN + 'films-classiques/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
# MOVIE_LIST = (True, 'showList')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASS[1], 'Films Classiques', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    # ne fonctionne plus sur le site
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + Quote(sSearchText)
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/'])
    liste.append(['Action & aventure', URL_MAIN + 'genre/action-adventure/'])
    liste.append(['Animation', URL_MAIN + 'genre/animation/'])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/'])
    liste.append(['Comédie', URL_MAIN + 'genre/comedie/'])
    liste.append(['Crime', URL_MAIN + 'genre/crime/'])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'genre/drame/'])
    liste.append(['Etranger', URL_MAIN + 'genre/etranger/'])
    liste.append(['Familial', URL_MAIN + 'genre/familial/'])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'genre/histoire/'])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/'])
    liste.append(['Musique', URL_MAIN + 'genre/musique/'])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/'])
    liste.append(['News', URL_MAIN + 'genre/news/'])
    liste.append(['Policier', URL_MAIN + 'genre/policier/'])
    liste.append(['Reality', URL_MAIN + 'genre/reality/'])
    liste.append(['Romance', URL_MAIN + 'genre/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'genre/science-fiction/'])
    liste.append(['Science Fiction & Fantastique', URL_MAIN + 'genre/science-fiction-fantastique/'])
    liste.append(['Soap', URL_MAIN + 'genre/soap/'])
    liste.append(['Talk', URL_MAIN + 'genre/talk/'])
    liste.append(['Téléfilm', URL_MAIN + 'genre/telefilm/'])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/'])
    liste.append(['War & Politics', URL_MAIN + 'genre/war-politics/'])
    liste.append(['Western', URL_MAIN + 'genre/western/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showList():
    oGui = cGui()

    liste = []
    liste.append(['09', URL_MAIN + '?letter=true&s=title-09'])
    liste.append(['A', URL_MAIN + '?letter=true&s=title-a'])
    liste.append(['B', URL_MAIN + '?letter=true&s=title-b'])
    liste.append(['C', URL_MAIN + '?letter=true&s=title-c'])
    liste.append(['D', URL_MAIN + '?letter=true&s=title-d'])
    liste.append(['E', URL_MAIN + '?letter=true&s=title-e'])
    liste.append(['F', URL_MAIN + '?letter=true&s=title-f'])
    liste.append(['G', URL_MAIN + '?letter=true&s=title-g'])
    liste.append(['H', URL_MAIN + '?letter=true&s=title-h'])
    liste.append(['I', URL_MAIN + '?letter=true&s=title-i'])
    liste.append(['J', URL_MAIN + '?letter=true&s=title-j'])
    liste.append(['K', URL_MAIN + '?letter=true&s=title-k'])
    liste.append(['L', URL_MAIN + '?letter=true&s=title-l'])
    liste.append(['M', URL_MAIN + '?letter=true&s=title-m'])
    liste.append(['N', URL_MAIN + '?letter=true&s=title-n'])
    liste.append(['O', URL_MAIN + '?letter=true&s=title-o'])
    liste.append(['P', URL_MAIN + '?letter=true&s=title-p'])
    liste.append(['Q', URL_MAIN + '?letter=true&s=title-q'])
    liste.append(['R', URL_MAIN + '?letter=true&s=title-r'])
    liste.append(['S', URL_MAIN + '?letter=true&s=title-s'])
    liste.append(['T', URL_MAIN + '?letter=true&s=title-t'])
    liste.append(['U', URL_MAIN + '?letter=true&s=title-u'])
    liste.append(['V', URL_MAIN + '?letter=true&s=title-v'])
    liste.append(['W', URL_MAIN + '?letter=true&s=title-w'])
    liste.append(['X', URL_MAIN + '?letter=true&s=title-x'])
    liste.append(['Y', URL_MAIN + '?letter=true&s=title-y'])
    liste.append(['Z', URL_MAIN + '?letter=true&s=title-z'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1963, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchResult(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="thumbnail animation-2".+?href="([^"]+)".+?img src="([^"]+)" alt="([^"]+)".+?class="year">([^<]+)<.+?<p>(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = re.sub('/w\d+', '/w342', aEntry[1], 1)  # meilleure qualité
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDesc = aEntry[4]

            # Filtrer les résultats
            if sSearch and total > 5:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)  # permet à addMovie d'afficher l'année dans le détail

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="poster"><img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)<a href="([^"]+).+?<span>([^<]+).+?(<div class="texto">(.*?)<|<\/article)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = re.sub('/w\d+', '/w342', aEntry[0], 1)  # ameliore la qualité
            sTitle = aEntry[1]
            sQual = aEntry[2]
            sUrl2 = aEntry[3]
            sYear = aEntry[4]
            sDesc = ''  # cas ou la sdesc n'est pas presente
            if aEntry[6]:
                sDesc = aEntry[6]
            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="pagination"><span>Page.+?de ([^<]+).+?href="([^"]+)" ><span class="icon-chevron-right"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = 'property="og:description" content="(.+?)" /><meta property='
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = 'data-post="([^"]+)" data-nume="([^"]+)">\s*.+?\s*<span class="title">([^<]+)</span>\s*<span class="server">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sPost = aEntry[0]
            sNume = aEntry[1]
            sQual = aEntry[2]
            sHost = re.sub('\.\w+', '', aEntry[3]).capitalize()
            if 'Youtube' in sHost:
                continue
            
            sTitle = ('%s [%s] [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sPost', sPost)
            oOutputParameterHandler.addParameter('sNume', sNume)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sPost = oInputParameterHandler.getValue('sPost')
    sNume = oInputParameterHandler.getValue('sNume')

    # trouve la vraie url
    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.request()
    sUrl2 = oRequestHandler.getRealUrl() + 'wp-admin/admin-ajax.php'

    oRequestHandler = cRequestHandler(sUrl2)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    oRequestHandler.addParameters('action', 'doo_player_ajax')
    oRequestHandler.addParameters('post', sPost)
    oRequestHandler.addParameters('nume', sNume)
    sHtmlContent = oRequestHandler.request()

    sPattern = "<iframe.+?src=[',\"]([^'\"]+)[',\"]"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
