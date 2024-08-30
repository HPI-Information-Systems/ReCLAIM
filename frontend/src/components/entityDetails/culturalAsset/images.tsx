import { CulturalAsset } from '@/lib/client';

/**
 * Returns an array of the image URLs of a cultural asset in the order: depicted_in_image, referenced_in_card_image_front, referenced_in_card_image, referenced_in_card_image_back
 * @param culturalAsset The cultural asset to get the image URLs from
 * @returns An array of URLs of the images of the cultural asset in the order to be displayed
 */
export function getCulturalAssetImageURLs(culturalAsset: CulturalAsset) {
  const urls: string[] = [];
  if (culturalAsset.depicted_in_image) {
    urls.push(...culturalAsset.depicted_in_image.map((image) => image.url));
  }
  if (culturalAsset.referenced_in_card_image_front) {
    urls.push(
      ...culturalAsset.referenced_in_card_image_front.map((image) => image.url),
    );
  }
  if (culturalAsset.referenced_in_card_image) {
    urls.push(
      ...culturalAsset.referenced_in_card_image.map((image) => image.url),
    );
  }
  if (culturalAsset.referenced_in_card_image_back) {
    urls.push(
      ...culturalAsset.referenced_in_card_image_back.map((image) => image.url),
    );
  }
  return urls;
}

/**
 * Determines whether a cultural asset has at least one images
 * @param culturalAsset The cultural asset to check for images
 * @returns True if the cultural asset has at least one image relation, false otherwise
 */
export function culturalAssetHasImages(culturalAsset: CulturalAsset) {
  return (
    (culturalAsset.depicted_in_image &&
      culturalAsset.depicted_in_image.length > 0) ||
    (culturalAsset.referenced_in_card_image &&
      culturalAsset.referenced_in_card_image.length > 0) ||
    (culturalAsset.referenced_in_card_image_front &&
      culturalAsset.referenced_in_card_image_front.length > 0) ||
    (culturalAsset.referenced_in_card_image_back &&
      culturalAsset.referenced_in_card_image_back.length > 0)
  );
}
