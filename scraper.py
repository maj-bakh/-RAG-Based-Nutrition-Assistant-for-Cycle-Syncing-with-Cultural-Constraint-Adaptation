from apify_client import ApifyClient
import requests
import os

# Liste des profils à cibler
profiles = ["manskis_wellness", "soul.body.mindd"]

MAX_POSTS = 5  # Maximum 5 photos par profil

def download_image(url, filepath):
    """Télécharger une image depuis une URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=60, headers=headers)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"   Erreur téléchargement image: {e}")
        return False

def save_caption(caption, filepath):
    """Sauvegarder la description dans un fichier .txt"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(caption if caption else "")

def scrape_instagram_data(usernames):
    api_token = os.getenv("APIFY_TOKEN")
    if not api_token:
        print("Erreur : définissez la variable d'environnement APIFY_TOKEN avant le scraping.")
        return

    client = ApifyClient(api_token)
    for username in usernames:
        print(f"\n--- Scraping : {username} ---")
        
        # Créer le dossier pour le profil
        os.makedirs(username, exist_ok=True)
        
        try:
            # Configuration avec directUrls - format correct pour apify/instagram-scraper
            run_input = {
                "directUrls": [f"https://www.instagram.com/{username}/"],
                "resultsType": "posts",
                "resultsLimit": MAX_POSTS * 2,
                "searchType": "user",
                "searchLimit": 1,
            }
            
            print(f"   Lancement du scraper Apify...")
            run = client.actor("apify/instagram-scraper").call(
                run_input=run_input,
                timeout_secs=180
            )
            
            # Récupérer les résultats
            dataset = client.dataset(run["defaultDatasetId"])
            items = list(dataset.iterate_items())
            print(f"   Posts reçus: {len(items)}")
            
            if items:
                print(f"   Exemple de clés: {list(items[0].keys())[:10]}")
            
            photo_count = 0
            for item in items:
                if photo_count >= MAX_POSTS:
                    break
                
                # Ignorer les vidéos
                if item.get("type") == "Video" or item.get("videoUrl"):
                    continue
                
                shortcode = item.get("shortCode") or item.get("id") or f"post_{photo_count}"
                caption = item.get("caption") or ""
                image_url = item.get("displayUrl") or item.get("url") or item.get("imageUrl")
                
                if not image_url:
                    print(f"   Pas d'URL pour {shortcode}")
                    continue
                
                # Télécharger la photo
                image_path = os.path.join(username, f"{shortcode}.jpg")
                caption_path = os.path.join(username, f"{shortcode}.txt")
                
                if download_image(image_url, image_path):
                    save_caption(caption, caption_path)
                    photo_count += 1
                    caption_preview = caption[:80] + '...' if caption and len(caption) > 80 else caption if caption else 'Aucune'
                    print(f"[{photo_count}/{MAX_POSTS}] Photo: {shortcode}")
                    print(f"   Caption: {caption_preview}")
            
            print(f"✓ {photo_count} photos téléchargées pour {username}")
                
        except Exception as e:
            print(f"Erreur pour {username} : {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    scrape_instagram_data(profiles)