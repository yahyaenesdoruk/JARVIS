# JARVIS (Türkçe sesli asistan)

JARVIS; hem **macOS** hem de **Windows** bilgisayarlarda sesi dinleyip komut çalıştırabilen bir sesli asistandır.

- Uygulama adı: **JARVIS**
- Türkçe sesli okunuş: **"Jarvis"**

## Özellikler

- Türkçe konuşmayı dinler (`tr-TR`).
- "jarvis" uyandırma kelimesi ile çalışır.
- Sistem komutlarını işletim sistemine göre yönetir:
  - Tarayıcı açma
  - Dosya gezgini/Finder açma
  - Hesap makinesi açma
  - Ekranı kilitleme
  - Ses açma/kısma/sessize alma
- Mikrofon üzerinden sürekli döngüde çalışır.

## Kurulum

> Python 3.10+ önerilir.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
python jarvis.py
```

## Örnek Kullanım

Aşağıdaki örnek akış gibi konuşabilirsiniz:

1. "Jarvis"
2. "tarayıcı aç"
3. "hesap makinesi aç"
4. "ses kıs"
5. "çıkış"

## Notlar

- İlk çalıştırmada mikrofon izni vermeniz gerekir.
- Konuşma tanıma için internet bağlantısı gerekebilir (Google Speech API kullanılır).
- İsterseniz `COMMAND_MAP` sözlüğünü genişleterek yeni komutlar ekleyebilirsiniz.
