# 🧠 What was The Inspiration Behind ReTain?
Our central vision for the creation of ReTain can be summarized in the following statement, "Sustainability != inconvenience, but rather possibilities." The carbon impact of creating a new article of clothing, furniture, or other household material is catastrophic to the environment. This is why we decided to create an application which would not only strive to promote reusability, but it would do so without inconveniencing the everyday consumer.

# 💻 What is ReTain?
ReTain is a web-based application which uses computer vision to identify any object placed in front of the camera, along with key characteristics regarding the item to suggest used alternatives from leading second-hand marketplaces Kijiji and eBay. It allows the user to utilize sustainable practices by reusing items along with purchasing the item at a discounted price. The primary usage of ReTain is at malls, where if a consumer is inclined towards purchasing an item, they have the capability to simply scan the item and get suggested used alternatives.

![image](https://user-images.githubusercontent.com/58268240/197909766-2d7fcc46-e089-4111-a1b6-6e177162ba78.png)

# 🔧 How did we build it?
The web-application back-end is created using Python Django. This handles communication between the image obtained from the front-end using jQuery, and the Google Vision API which processes the image and provides keywords. Once the user takes an image in the application, that image has its background deleted using the Removal.ai API. This allows for much more accuracy in the keyword extraction. The background-deleted image is then processed using the Google Cloud Vision API, which returns keywords regarding the item. Then, Python requests are used to search for the keywords in eBay and Kijiji.

# ⚙️ What Technologies Did We Use?
- Python
- Django
- Google Cloud Vision API
- Removal.ai API
- HTML/CSS/JS
