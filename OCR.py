import easyocr
import os
import glob


# Initialiser le lecteur OCR avec l'anglais et l'arabe
reader = easyocr.Reader(['en', 'ar'], gpu=False)

# Dossiers contenant les images
image_folders = ['soul.body.mindd']

# Extensions d'images supportées
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']


def get_y_position(result):
    """Retourne la position Y moyenne d'un résultat OCR"""
    bbox = result[0]
    return (bbox[0][1] + bbox[2][1]) / 2


def get_x_position(result):
    """Retourne la position X du coin gauche d'un résultat OCR"""
    bbox = result[0]
    return bbox[0][0]


def process_image(image_path, output_dir, post_num, description_num):
    """Traite une image et sauvegarde le texte extrait"""
    try:
        # Lire le texte de l'image
        results = reader.readtext(image_path)
        
        if not results:
            print(f"  Aucun texte trouvé dans: {image_path}")
            return
        
        # Trier d'abord par Y, puis par X
        sorted_results = sorted(results, key=lambda r: (get_y_position(r), get_x_position(r)))
        
        # Grouper les éléments sur la même ligne (Y similaire)
        lines = []
        current_line = []
        current_y = None
        y_tolerance = 25
        
        for result in sorted_results:
            y_pos = get_y_position(result)
            
            if current_y is None:
                current_y = y_pos
                current_line.append(result)
            elif abs(y_pos - current_y) <= y_tolerance:
                current_line.append(result)
            else:
                if current_line:
                    current_line.sort(key=get_x_position)
                    lines.append(current_line)
                current_line = [result]
                current_y = y_pos
        
        if current_line:
            current_line.sort(key=get_x_position)
            lines.append(current_line)
        
        # Créer le fichier de sortie avec numérotation post_X_description_Y
        output_file = os.path.join(output_dir, f"post_{post_num}_description_{description_num}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                line_text = ' '.join([result[1] for result in line])
                f.write(f"{line_text}\n")
        
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
            # Extraire le timestamp (tout avant _1.jpg, _2.jpg, etc. ou .jpg)
            if '_' in filename and filename.split('_')[-1][0].isdigit():
                # Format: 2024-06-12_21-58-22_UTC_1.jpg
                parts = filename.rsplit('_', 1)
                timestamp = parts[0]
            else:
                # Format: 2025-08-09_10-55-20_UTC.jpg (image unique)
                timestamp = os.path.splitext(filename)[0]
            
            if timestamp not in posts:
                posts[timestamp] = []
            posts[timestamp].append(image_path)
        
        # Trier les posts par date
        sorted_posts = sorted(posts.items())
        
        print(f"Nombre de posts trouvés: {len(sorted_posts)}")
        
        # Traiter chaque post
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
