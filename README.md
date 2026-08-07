ImageShield: Cyber Hygiene Toolkit
ImageShield is a modular image protection app built with Streamlit. It empowers users to sanitize, watermark, and obfuscate images before sharing — with full transparency, auditability, and downloadable logs. Designed for privacy-conscious users, researchers, and demo environments.

![ImageShield Architecture](images/imageshield_architecture.png)

Features
- CleanScan: Automatically blur detected faces to remove sensitive content
- SafeShare: Add customizable watermark and remove metadata for safe sharing
- NoiseGuard: Apply pixelation, noise, or blur filters with adjustable intensity
- Summary Panel: Displays all applied protections in session
- Log Viewer: Shows timestamped actions and allows log download
- Settings Panel:
- Auto-run toggle
- Preview toggle
- Font size and watermark position controls
- Theme selector

Sidebar Controls
- Module Selector: Clickable buttons for CleanScan, SafeShare, and NoiseGuard
- Image Upload: Accepts .jpg, .jpeg, .png formats
- Settings: Customize watermark, noise intensity, font size, and appearance
- History Controls: Clear session state and audit logs

Folder Structure
ImageShield/
├── app.py
├── log.txt               # Auto-generated after module run
├── modules/
│   ├── cleanscan.py      # Face blurring logic
│   ├── safeshare.py      # Watermark and metadata removal
│   └── noiseguard.py     # Privacy filters



Requirements
Install dependencies:
pip install streamlit pillow opencv-python pandas


Run Locally
streamlit run app.py

Then open http://localhost:8501 in your browser.

How It Works
- Select a module from the sidebar
- Upload an image
- Configure settings (e.g. watermark text, noise intensity)
- Run the module and download the protected image
- View or download the audit log

Summary Panel
After running any module, the app displays:
- Module name
- Parameters used (e.g. watermark text, noise intensity)
- Download buttons for image and log

Log Viewer
- Shows timestamped actions per module
- Auto-generates log.txt
- Downloadable as plain text
- Tabular view for auditability

Future Roadmap
- Batch image processing
- EXIF metadata viewer/remover
- PDF summary export
- Fairness-aware filters
- Encrypted log files
- Native Android version (Kivy or Flutter)

Ideal Use Cases
- Privacy-preserving image sharing
- Research demos on fairness and robustness
- Technical competitions and hackathons
- Educational tools for cyber hygiene

License
MIT License — free to use, modify, and distribute.

