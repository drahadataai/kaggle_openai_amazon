from src.utils.tools import detect_sites_in_image
import asyncio

def test_detect_sites_in_image_with_sample_image():
    # Arrange: Use a sample image path or mock image data
    sample_image_path = "/Users/weidongliu/Projects/kaggle/z_agent/kaggle_openai_amazon/data/google_image_to_be_detected/image_1076.png"  # Update with a real test image path

    # Act: Call the function
    result = asyncio.run(detect_sites_in_image(sample_image_path))

    print("Detection Result:", result)

    # Assert: Check the result (update expected_result as appropriate)
    # expected_result = []  # Replace with expected output for your sample image
    # assert result == expected_result

if __name__ == "__main__":
    test_detect_sites_in_image_with_sample_image()