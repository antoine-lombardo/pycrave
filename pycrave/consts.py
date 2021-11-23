CLIENT_ID = "crave-android"
CLIENT_PASS = 'default'

BASE_HEADERS = {
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0'
}

CAPI_HEADERS = {
  'accept-encoding': 'identity',
  'connection': 'Keep-Alive',
  'user-agent': 'okhttp/4.9.0'
}

GRAPHQL_URL = 'https://www.crave.ca/space-graphql/graphql/'

HEADERS = {
  'accept': 'application/json',
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'content-type': 'application/json; charset=utf-8',
  'graphql-client-platform': 'entpay_android',
  'user-agent': 'okhttp/4.9.0'
}

SEARCH_PAYLOAD = {
  "operationName": "searchMedia",
  "variables": {
    "searchTerm": "TO FILL", # TO FILL
    "pageNumber": 0,
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "ENGLISH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH"
  },
  'query': 'query searchMedia($searchTerm: String!, $pageNumber: Int = 0, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext( maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { searchMedia(pageSize: 50, titleMatches: $searchTerm) { __typename page(page: $pageNumber) { __typename totalItemCount totalPageCount hasNextPage hasPreviousPage items { __typename ... BasicMediaPosterFragment } } } } fragment BasicMediaPosterFragment on AxisMedia { __typename id title axisId agvotCode flag { __typename title label } images(formats: [POSTER]) { __typename url } resourceCodes }'
}

MEDIA_PAYLOAD = {
  "operationName": "AxisMedia",
  "variables": {
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "ENGLISH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH",
    "id": "TO FILL", # TO FILL
    "imageFormat": [
      "THUMBNAIL",
      "THUMBNAIL_WIDE",
      "POSTER"
    ]
  },
  "query": "query AxisMedia($subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $id: ID!, $imageFormat: [ImageFormat]!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { axisMedia(id: $id) { __typename ...AxisMediaInfo seasons { __typename ...SeasonInfoFragment } promotionalContents(mode: NONE) { __typename page { __typename items { __typename ...AxisContentFragment } } } relatedCollections { __typename id axisCollectionItemCount title collection { __typename page { __typename totalItemCount items { __typename ...BasicMediaPosterFragment } } } } } } fragment AxisMediaInfo on AxisMedia { __typename ...AxisMediaBasicInfo mainContents { __typename page { __typename items { __typename ...AxisContentFragment } } } firstPlayableContent { __typename ...AxisContentFragment } featuredClip { __typename ...AxisContentFragment } normalizedRatingCodes { __typename ...NormalizedRatingCodeFragment } cast { __typename role castMembers { __typename fullName } } metadataUpgrade { __typename userIsSubscribed packageName subText languages } adUnit { __typename ... BasicAdUnitFragment } } fragment AxisMediaBasicInfo on AxisMedia { __typename id axisId title agvotCode qfrCode summary description mediaType originalSpokenLanguage mediaConstraint { __typename hasConstraintsNow } genres { __typename name } axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } images(formats: $imageFormat) { __typename ...ImageFragment } flag { __typename title label } firstAirYear ratingCodes resourceCodes heroBrandLogoId originatingNetworkLogoId } fragment AxisContentFragment on AxisContent { __typename id axisId title contentType axisMediaTitle summary description seasonNumber episodeNumber broadcastDate images(formats: $imageFormat) { __typename ...ImageFragment } axisMedia: axisMedia { __typename id axisId firstAirYear } duration durationSecs agvotCode axisPlaybackLanguages { __typename offlineDownload { __typename allowed } contentPackageId ...PlaybackLanguagesFragment } adUnit { __typename ...BasicAdUnitFragment } qfrCode ratingCodes videoPlayerDestCode originalSpokenLanguage normalizedRatingCodes { __typename ...NormalizedRatingCodeFragment } resourceCodes authConstraints { __typename ...AuthConstraintFragment } flag { __typename title label } } fragment ImageFragment on AxisImage { __typename format url } fragment PlaybackLanguagesFragment on AxisPlayback { __typename language destinationCode } fragment BasicAdUnitFragment on AxisAdUnit { __typename adultAudience heroBrand pageType product title revShare keyValue { __typename mediaType adTarget contentType pageTitle revShare subType } } fragment NormalizedRatingCodeFragment on NormalizedRatingCode { __typename language ratingCodes } fragment AuthConstraintFragment on AuthConstraint { __typename authRequired language packageName } fragment SeasonInfoFragment on AxisSeason { __typename id axisId title seasonNumber resourceCodes axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } metadataUpgrade { __typename languages packageName userIsSubscribed } images(formats: [THUMBNAIL]) { __typename url } } fragment BasicMediaPosterFragment on AxisMedia { __typename id title axisId agvotCode flag { __typename title label } images(formats: [POSTER]) { __typename url } resourceCodes }"
}

SEASON_PAYLOAD = {
  "operationName": "axisSeason",
  "variables": {
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "FRENCH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH",
    "id": "TO FILL", # TO FILL
    "imageFormat": [
      "THUMBNAIL",
      "THUMBNAIL_WIDE",
      "POSTER"
    ]
  },
  "query": "query axisSeason($subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $id: ID!, $imageFormat:[ImageFormat]!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { axisSeason(id: $id) { __typename ...SeasonsFragment } } fragment SeasonsFragment on AxisSeason { __typename ...SeasonInfoFragment episodes { __typename ...EpisodeFragment } } fragment SeasonInfoFragment on AxisSeason { __typename id axisId title seasonNumber resourceCodes axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } metadataUpgrade { __typename languages packageName userIsSubscribed } images(formats: [THUMBNAIL]) { __typename url } } fragment EpisodeFragment on AxisContent { __typename broadcastDate seasonNumber episodeNumber ...AxisContentFragment } fragment AxisContentFragment on AxisContent { __typename id axisId title contentType axisMediaTitle summary description seasonNumber episodeNumber broadcastDate images(formats: $imageFormat) { __typename ...ImageFragment } axisMedia: axisMedia { __typename id axisId firstAirYear } duration durationSecs agvotCode axisPlaybackLanguages { __typename offlineDownload { __typename allowed } contentPackageId ...PlaybackLanguagesFragment } adUnit { __typename ...BasicAdUnitFragment } qfrCode ratingCodes videoPlayerDestCode originalSpokenLanguage normalizedRatingCodes { __typename ...NormalizedRatingCodeFragment } resourceCodes authConstraints { __typename ...AuthConstraintFragment } flag { __typename title label } } fragment ImageFragment on AxisImage { __typename format url } fragment PlaybackLanguagesFragment on AxisPlayback { __typename language destinationCode } fragment BasicAdUnitFragment on AxisAdUnit { __typename adultAudience heroBrand pageType product title revShare keyValue { __typename mediaType adTarget contentType pageTitle revShare subType } } fragment NormalizedRatingCodeFragment on NormalizedRatingCode { __typename language ratingCodes } fragment AuthConstraintFragment on AuthConstraint { __typename authRequired language packageName }"
}