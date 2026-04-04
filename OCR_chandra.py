# Script OCR utilisant EasyOCR (gratuit et local)
import os
import glob
import easyocr

# Initialiser le lecteur OCR (anglais + arabe)
reader = easyocr.Reader(['en', 'ar'])

# Dossiers contenant les images
image_folders = ['soul.body.mindd']

# Extensions d'images supportées
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']

def process_image(image_path, output_dir, post_num, description_num):
    """Traite une image et sauvegarde le texte extrait"""
    try:
        # Lire le texte de l'image avec EasyOCR
        results = reader.readtext(image_path)
        
        if not results:
            print(f"  Aucun texte trouvé dans: {image_path}")
            return
        
        # Extraire le texte (results = [(bbox, text, confidence), ...])
        text = '\n'.join([r[1] for r in results])
        
        # Créer le fichier de sortie
        output_file = os.path.join(output_dir, f"post_{post_num}_description_{description_num}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"  ✓ {os.path.basename(image_path)} -> post_{post_num}_description_{description_num}.txt")
        
    except Exception as e:
        print(f"  ✗ Erreur pour {image_path}: {e}")

def main():
    """Fonction principale pour traiter toutes les images"""
    total_images = 0
    
    for folder in image_folders:
        if not os.path.exists(folder):
            print(f"Dossier non trouvé: {folder}")
            continue
        
        print(f"\n{'='*50}")
        print(f"Traitement du dossier: {folder}")
        print('='*50)
        
        # Créer le dossier de sortie pour ce compte
        output_dir = os.path.join('ocr_results', folder)
        os.makedirs(output_dir, exist_ok=True)
        
        # Trouver toutes les images
        images = []
        for ext in image_extensions:
            images.extend(glob.glob(os.path.join(folder, ext)))
        
        if not images:
            print(f"Aucune image trouvée dans {folder}")
            continue
        
        print(f"Nombre d'images trouvées: {len(images)}")
        
        # Grouper les images par post (même timestamp)
        posts = {}
        for image_path in sorted(images):
            filename = os.path.basename(image_path)
            if '_' in filename and filename.split('_')[-1][0].isdigit():
                parts = filename.rsplit('_', 1)
                timestamp = parts[0]
            else:
                timestamp = os.path.splitext(filename)[0]
            
            if timestamp not in posts:
                posts[timestamp] = []
            posts[timestamp].append(image_path)
        
        sorted_posts = sorted(posts.items())
        print(f"Nombre de posts trouvés: {len(sorted_posts)}")
        
        for post_num, (timestamp, post_images) in enumerate(sorted_posts, 1):
            print(f"\n  Post {post_num} ({timestamp}): {len(post_images)} images")
            
            for description_num, image_path in enumerate(sorted(post_images), 1):
                process_image(image_path, output_dir, post_num, description_num)
                total_images += 1
    
    print(f"\n{'='*50}")
    print(f"OCR terminé! {total_images} images traitées.")
    print(f"Résultats sauvegardés dans: ocr_results/")
    print('='*50)

if __name__ == "__main__":
    main()