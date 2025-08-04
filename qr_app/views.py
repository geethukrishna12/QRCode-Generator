from django.shortcuts import render
import qrcode
from io import BytesIO
import base64

def generate_qr_code(data: str) -> str:
    """Generate base64 QR code from given data."""
    qr_image = qrcode.make(data, box_size=5)
    qr_image_pil = qr_image.get_image()
    stream = BytesIO()
    qr_image_pil.save(stream, format='PNG')
    qr_image_data = stream.getvalue()
    return base64.b64encode(qr_image_data).decode('utf-8')

def home(request):
    context = {}
    
    if request.method == "POST":
        if "qr_text" in request.POST:
            qr_text = request.POST.get("qr_text", "").strip()
            if qr_text:
                qr_image_base64 = generate_qr_code(qr_text)
                context['qr_image_base64'] = qr_image_base64
                context['variable'] = qr_text
                context['qr_type'] = 'text'

        elif "qr_whatsapp" in request.POST:
            phone_number = request.POST.get("qr_whatsapp", "").strip()
            if phone_number:
                wa_link = f"https://wa.me/{phone_number}"
                qr_image_base64 = generate_qr_code(wa_link)
                context['qr_image_base64'] = qr_image_base64
                context['variable'] = wa_link
                context['qr_type'] = 'whatsapp'

    return render(request, 'home.html', context)
