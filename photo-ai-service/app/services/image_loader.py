import requests
import cv2
import numpy as np

from app.config import logger, IMAGE_DOWNLOAD_TIMEOUT


def load_image_from_url(url: str) -> np.ndarray | None:
    """
    Downloads an image from a URL and decodes it into an OpenCV image.

    Returns:
    - np.ndarray (BGR image) on success
    - None on failure
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; BlockBuzzPhotoAI/1.0)"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=IMAGE_DOWNLOAD_TIMEOUT
        )

        response.raise_for_status()

        image_bytes = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if image is None:
            logger.warning(f"OpenCV failed to decode image from URL: {url}")
            return None

        return image

    except requests.exceptions.Timeout:
        logger.warning(f"Timeout while downloading image: {url}")
        return None

    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to download image: {url} | error={str(e)}")
        return None

    except Exception:
        logger.exception(f"Unexpected error loading image: {url}")
        return None
