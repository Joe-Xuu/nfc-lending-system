import qrcode
import os

# 1. LIFF ID get from env
YOUR_LIFF_ID = os.getenv("LIFF_ID")

if not YOUR_LIFF_ID:
    YOUR_LIFF_ID = input("LIFF_ID Not Found, go check your .env file, or just input it here:")

# 2.  random id
CONTAINER_ID = input("Enter the target container ID:")

# 3. URL
target_url = f"https://liff.line.me/{YOUR_LIFF_ID}?containerId={CONTAINER_ID}"

print(f"generating QR code, target URL: {target_url}")

# 4. generate qrcode
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)
qr.add_data(target_url)
qr.make(fit=True)

img = qr.make_image(fill='black', back_color='white')

# save as png
img.save(f"{CONTAINER_ID}.png")
print(f"QR code saved as {CONTAINER_ID}.png")

# show it if possible
import os
os.system(f"open {CONTAINER_ID}.png")