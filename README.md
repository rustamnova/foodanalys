# foodanalys
Food analysis for composition
🧠 Product Ingredient Analyzer Bot
A Telegram bot that helps you understand what's inside your food. Just send a photo of the product's ingredient list or a text/voice message, and the bot will analyze it for:

⚠️ Harmful additives

🧬 Potential allergens

🧪 Dangerous substances

🌱 Diet compatibility (vegan, keto, gluten-free, diabetic, etc.)

🚀 Features
✅ Photo analysis with GPT-4 Vision
✅ Voice input support (WIP)
✅ Detailed breakdown for each ingredient
✅ Quick checks with inline buttons

🛠 Example Bot Commands & Buttons
After uploading an ingredient list, users can tap:

🔍 Analyze Ingredients
General breakdown with short explanations.

⚠️ Check for Allergens
Detects common allergens like lactose, gluten, nuts, soy.

🧪 Check for Harmful Additives
Finds E-numbers, colorants, trans fats, preservatives.

🧬 Check for Carcinogens
Based on IARC and other regulatory sources.

🌱 Diet Compatibility
Vegan? Keto? Diabetic? We’ll tell you if it fits.

💊 Food Additives (E-numbers)
Detailed breakdown of E120, E621, etc.

🧠 Health Impact
Effects on the gut, nervous system, hormones, etc.

🧯 Flavor Enhancers
Detects glutamate, artificial flavorings.

📜 Full Ingredient Rating
Each item marked with a color-based health score.

🧩 Example Use Case
User sends a photo:
“Cookie ingredients: flour, sugar, palm oil, E471, flavorings.”

Bot responds with:

🟡 Flour – Neutral

🟢 Sugar – Okay in moderation

🔴 Palm oil – Avoid (high in saturated fats)

🔴 E471 – May contain trans fats

🟠 Flavorings – Possible synthetic additives

📦 Tech Stack
Python 3.10+

aiogram 3.x

OpenAI GPT-4 Turbo Vision

python-dotenv

📸 How It Works
You send a photo of an ingredient list.

Bot sends it to GPT-4 Vision.

Bot responds with a smart analysis of ingredients.

🔒 Environment Setup
Create a .env file with your tokens:

BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key

Install dependencies:

pip install -r requirements.txt
💬 Voice Input (Coming Soon)
Soon, you’ll be able to say:

"I bought some crackers. Ingredients: wheat, sugar, palm oil, E621, coloring agents."

And the bot will turn this into:

"Analyze the following ingredients: wheat, sugar, palm oil, E621, coloring agents. Identify allergens, harmful additives, and provide a summary for each."

🙌 Thanks for checking this project!
Feel free to contribute or suggest new features 🧃
