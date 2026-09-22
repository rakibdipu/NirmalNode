import os
from PIL import Image

fig_dir = r'C:\Users\ASUS\Downloads\capstone 3.2\thesis_src\nirmalnode_thesis\figures'

print("=== OPTIMIZING FIGURES FOR SUPER-FAST OVERLEAF COMPILATION ===")
for f in sorted(os.listdir(fig_dir)):
    fp = os.path.join(fig_dir, f)
    if not (f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')):
        continue
    
    orig_sz = os.path.getsize(fp)
    with Image.open(fp) as im:
        w, h = im.size
        fmt = im.format
        mode = im.mode
        
        # Max width 1400px (crystal sharp for A4 page width of ~6 inches)
        max_w = 1400
        if w > max_w:
            new_w = max_w
            new_h = int(h * (max_w / w))
            im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        else:
            im_resized = im.copy()
            new_w, new_h = w, h
            
        # Save optimized
        if f.endswith('.png'):
            # Convert RGBA to RGB with white background if needed, or keep PNG with clean compression
            if mode == 'RGBA':
                bg = Image.new('RGB', im_resized.size, (255, 255, 255))
                bg.paste(im_resized, mask=im_resized.split()[3])
                bg.save(fp, format='PNG', optimize=True)
            else:
                im_resized.save(fp, format='PNG', optimize=True)
        elif f.endswith('.jpg') or f.endswith('.jpeg'):
            if mode != 'RGB':
                im_resized = im_resized.convert('RGB')
            im_resized.save(fp, format='JPEG', quality=85, optimize=True)

    new_sz = os.path.getsize(fp)
    print(f"{f:35s} | {orig_sz/1024:6.1f} KB -> {new_sz/1024:6.1f} KB | {w}x{h} -> {new_w}x{new_h}")

print("All figures optimized!")
