# Ethnicity Mapping and Error Handling Improvements

## Sorunlar

1. Etnik köken eşleştirme sorunları
   - Bazı ülke kodları için etnik köken eşleşmeleri eksik
   - Tekil/çoğul etnik köken isimleri arasında tutarsızlıklar (European/Europeans, Scandinavian/Scandinavians)
   - None etnik köken değerleri uygun şekilde işlenmiyor

2. XML oluşturma hataları
   - None değerleri profile_manager.py'deki XML oluşturma sürecinde hatalara yol açıyor
   - `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'` hatası

## Çözümler

### mapper.py İyileştirmeleri

1. **Kapsamlı Ülke-Etnik Köken Eşleştirmesi**
   - Tüm yaygın ülke kodları için etnik köken eşleştirmeleri eklendi
   - Bu, eşleştirme eksikliği nedeniyle atlanan oyuncu sayısını azaltacak

2. **Etnik Köken İsim Standardizasyonu**
   - Tekil/çoğul form eşleştirmeleri eklendi (European -> Europeans)
   - Eski etnik köken isimleri yeni klasör adlarına eşleştirildi

3. **None ve Hata İşleme**
   - None değerleri için varsayılan "Europeans" fallback mekanizması eklendi
   - Seçilen etnik köken için yüz kalmadığında alternatif stratejiler eklendi

### profile_manager.py İyileştirmeleri

1. **Güvenli None İşleme**
   - None etnik köken ve resim değerleri için koruma eklendi
   - Hatalı durumlar uygun şekilde loglanıyor ve atlanıyor

## Faydaları

1. Daha fazla oyuncu başarıyla eşleştirilebiliyor
2. None değerleri artık programın çökmesine neden olmuyor
3. Eskimiş/farklı etnik köken isimleri düzgün şekilde işleniyor
4. Kapsamlı ülke-etnik köken eşleştirmeleri ile daha fazla ülke kodu destekleniyor
5. Hata durumunda daha iyi log bilgileri
