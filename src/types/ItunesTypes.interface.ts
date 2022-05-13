export interface ItunesTypes {
  resultCount?: number;
  results?: Result[];
}

export interface Result {
  wrapperType: string;
  collectionType: string;
  artistId: number;
  amgArtistId?: number;
  artistName: string;
  collectionName: string;
  collectionCensoredName: string;
  artistViewUrl: string;
  collectionViewUrl: string;
  artworkUrl60: string;
  artworkUrl1100: string;
  collectionPrice: number;
  collectionExlicitness: string;
  contentAdvisoryRating?: string;
  trackCount: number;
  copyright: string;
  country: string;
  currency: number;
  releaseDate: string;
  primaryGenreName: string;
}
