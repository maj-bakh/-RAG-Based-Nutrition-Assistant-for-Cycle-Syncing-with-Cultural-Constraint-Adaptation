import instaloader
import time

# télécharger uniquement photo + description
L = instaloader.Instaloader(
    download_videos=False,           # Pas de vidéos
    download_video_thumbnails=False, # Pas de miniatures vidéo
    download_geotags=False,          # Pas de géotags
    download_comments=False,         # Pas de commentaires
    save_metadata=False,             # Pas de métadonnées JSON
    post_metadata_txt_pattern= '{caption}'  # Sauvegarder la description dans le fichier .txt
)

# Liste des profils à cibler
profiles = ["manskis_wellness", "soul.body.mindd"]

MAX_POSTS = 5  # Maximum 5 photos par profil

def scrape_instagram_data(usernames):
    for username in usernames:
        print(f"\n--- Scraping : {username} ---")
        
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            posts = profile.get_posts()
            
            photo_count = 0
            for post in posts:
                # Stop si on a déjà 5 photos
                if photo_count >= MAX_POSTS:
                    break
                
                # Ignorer les vidéos - on veut uniquement les photos
                if post.is_video:
                    continue
                
                # Télécharger la photo + description
                L.download_post(post, target=profile.username)
                
                photo_count += 1
                print(f"[{photo_count}/{MAX_POSTS}] Photo: {post.shortcode}")
                print(f"   Description: {post.caption if post.caption else 'Aucune'}")
                
                time.sleep(2)
            
            print(f"✓ {photo_count} photos téléchargées pour {username}")
                
        except Exception as e:
            print(f"Erreur pour {username} : {e}")

if __name__ == "__main__":
    scrape_instagram_data(profiles)