# Sentio.ai Otomatik Test ve Öğrenme Sistemi
import requests
import json
import time
from datetime import datetime
import csv
import os

class SentioAutoTester:
    def __init__(self, render_url):
        self.render_url = render_url
        self.test_results = []
        self.performance_history = []
        
    def load_test_dataset(self):
        """Genişletilmiş test veri seti - 20 metin (10 insan + 10 AI)"""
        return {
            # === İNSAN METİNLERİ (Hedef: %0-30) ===
            "INSAN_01": {
                "text": "Dün akşam annemle telefonda konuştum. Nasılsın diye sordu, iyiyim anne dedim ama aslında çok yorgundum. Bu hafta işte proje sunumu vardı, heyecanlıydım.",
                "expected": "human",
                "category": "günlük_konuşma"
            },
            "INSAN_02": {
                "text": "Sabah erken kalktım, kahvaltımı yaptım. Parkta yürürken yaşlı bir amca ile karşılaştım. Merhaba dedi, ben de günaydın dedim. Güzel bir gündü.",
                "expected": "human", 
                "category": "günlük_deneyim"
            },
            "INSAN_03": {
                "text": "Üniversiteye başladığımda çok zorlandım. Özellikle matematik dersleri beni çok uğraştırdı. Ama çalıştım, çabaladım ve sonunda başardım. Şimdi mezun oldum.",
                "expected": "human",
                "category": "kişisel_hikaye"
            },
            "INSAN_04": {
                "text": "İstanbul trafiği gerçekten çok kötü. Sabah işe giderken 2 saat yolda kaldım. Artık toplu taşıma kullanmaya karar verdim. Metro çok daha hızlı.",
                "expected": "human",
                "category": "günlük_şikayet"
            },
            "INSAN_05": {
                "text": "Tez yazma süreci gerçekten zor geçti. Kaynak bulmakta zorlandım, danışmanımla çok toplantı yaptık. Bazen pes etmek istedim ama sonunda bitirdim.",
                "expected": "human",
                "category": "akademik_deneyim"
            },
            "INSAN_06": {
                "text": "Köydeki dedem çok hasta. Geçen hafta ziyarete gittim. Eski hikayeler anlattı, çocukluğumuzu hatırlattı. Bu anları çok özlüyorum.",
                "expected": "human",
                "category": "duygusal"
            },
            "INSAN_07": {
                "text": "Yeni işe başladığım ilk gün çok heyecanlıydım. Meslektaşlarım çok yardımsever çıktı. Patronum da anlayışlı birisi. Sanırım burada mutlu olacağım.",
                "expected": "human",
                "category": "iş_deneyimi"
            },
            "INSAN_08": {
                "text": "Geçen yaz tatilde Antalya'ya gittik. Deniz muhteşemdi, güneş çok güzeldi. Otel de fena değildi. Çocuklar çok eğlendi, biz de dinlendik.",
                "expected": "human",
                "category": "tatil_anısı"
            },
            "INSAN_09": {
                "text": "Bu kitabı okurken çok etkilendim. Karakterlerin yaşadıkları beni derinden etkiledi. Son sayfada ağladım. Herkese tavsiye ederim.",
                "expected": "human", 
                "category": "kitap_yorumu"
            },
            "INSAN_10": {
                "text": "Spor salonuna gitmeye başladım. İlk başta çok zorlandım, nefesim kesiliyordu. Ama şimdi alıştım, kendimi çok daha fit hissediyorum.",
                "expected": "human",
                "category": "spor_deneyimi"
            },
            
            # === AI METİNLERİ (Hedef: %70-100) ===
            "AI_01": {
                "text": "Bu bağlamda, eğitim sisteminin modernizasyonu kapsamında teknolojik entegrasyonun sistematik yaklaşımla gerçekleştirilmesi gerekmektedir. Söz konusu süreç, nitelikli insan gücünün yetiştirilmesi noktasında optimize edilmiş çözümler sunmaktadır.",
                "expected": "ai",
                "category": "akademik_kalıp"
            },
            "AI_02": {
                "text": "Araştırma kapsamında, veri analizi süreçlerinin sistematik bir şekilde yürütülmesi önem arz etmektedir. Bu çerçevede, metodolojik yaklaşımların entegrasyonu çalışmanın geçerliliği açısından kritik rol oynamaktadır.",
                "expected": "ai",
                "category": "araştırma_jargonu"
            },
            "AI_03": {
                "text": "Dolayısıyla, söz konusu analiz çerçevesinin optimize edilmesi, kapsamlı sonuçların elde edilmesini sağlayacaktır. Bu doğrultuda atılacak adımlar, bilimsel çalışmanın etkinliğini artıracaktır.",
                "expected": "ai",
                "category": "sonuç_kalıpları"
            },
            "AI_04": {
                "text": "Nitekim, teknolojik gelişmelerin eğitim süreçlerine entegrasyonu, öğrenme deneyimlerinin iyileştirilmesi açısından önemli fırsatlar sunmaktadır. Bu kapsamda gerçekleştirilecek uygulamalar, eğitimsel verimliliği optimize edecektir.",
                "expected": "ai",
                "category": "teknoloji_akademik"
            },
            "AI_05": {
                "text": "Sonuç olarak, sistematik yaklaşımların benimsenmesi, proje yönetimi süreçlerinin etkinliğinin artırılması noktasında kritik önem taşımaktadır. Bu çerçevede yapılacak düzenlemeler, organizasyonel performansı geliştirecektir.",
                "expected": "ai",
                "category": "yönetim_jargonu"
            },
            "AI_06": {
                "text": "Bu bağlamda, sürdürülebilir kalkınma hedefleri çerçevesinde yürütülecek projeler, toplumsal refah seviyesinin yükseltilmesi açısından önemli katkılar sağlayacaktır. Dolayısıyla, söz konusu inisiyatiflerin desteklenmesi gerekmektedir.",
                "expected": "ai",
                "category": "kalkınma_söylemi"
            },
            "AI_07": {
                "text": "Kapsamlı bir şekilde değerlendirildiğinde, inovasyon süreçlerinin desteklenmesi, rekabet gücünün artırılması noktasında stratejik önem arz etmektedir. Bu doğrultuda geliştirilen politikalar, ekonomik büyümeyi destekleyecektir.",
                "expected": "ai",
                "category": "ekonomi_akademik"
            },
            "AI_08": {
                "text": "Nitekim, dijital dönüşüm süreçlerinin etkin yönetimi, organizasyonel çevikliğin artırılması açısından kritik rol oynamaktadır. Bu kapsamda hayata geçirilecek uygulamalar, operasyonel verimliliği optimize edecektir.",
                "expected": "ai",
                "category": "dijital_jargon"
            },
            "AI_09": {
                "text": "Bu çerçevede, kalite yönetim sistemlerinin entegrasyonu, süreç iyileştirme faaliyetlerinin sistematik bir yaklaşımla yürütülmesini sağlamaktadır. Dolayısıyla, söz konusu sistemlerin optimize edilmesi gerekmektedir.",
                "expected": "ai",
                "category": "kalite_sistemi"
            },
            "AI_10": {
                "text": "Sonuç olarak, paydaş analizi çerçevesinde geliştirilen stratejiler, proje başarısının artırılması noktasında önemli katkılar sunmaktadır. Bu bağlamda, sistematik yaklaşımların benimsenmesi kritik önem taşımaktadır.",
                "expected": "ai", 
                "category": "strateji_akademik"
            }
        }
        
    def run_single_test(self, test_id, test_data):
        """Tek test çalıştır"""
        try:
            response = requests.post(
                f"{self.render_url}/analyze",
                json={"text": test_data["text"]},
                timeout=60 # Timeout süresini 60 saniyeye çıkardık
            )
            
            if response.status_code == 200:
                result = response.json()
                score = result.get('overall_score', 0)
                score_percent = int(score * 100)
                
                # Başarı değerlendirmesi
                expected = test_data["expected"]
                if expected == "human":
                    success = score_percent <= 30  # İnsan metni için başarı kriteri
                    expected_range = "0-30%"
                else:  # ai
                    success = score_percent >= 70  # AI metni için başarı kriteri  
                    expected_range = "70-100%"
                
                test_result = {
                    "test_id": test_id,
                    "expected": expected,
                    "category": test_data["category"],
                    "actual_score": score_percent,
                    "expected_range": expected_range,
                    "success": success,
                    "comment": result.get('comment', ''),
                    "timestamp": datetime.now().isoformat(),
                    "text_preview": test_data["text"][:50] + "..."
                }
                
                return test_result
                
            else:
                return {
                    "test_id": test_id,
                    "error": f"API Error: {response.status_code}",
                    "success": False
                }
                
        except requests.exceptions.ReadTimeout:
            return {
                "test_id": test_id,
                "error": "Read Timeout - Sunucu uyanamadı veya çok yavaş.",
                "success": False
            }
        except Exception as e:
            return {
                "test_id": test_id,
                "error": str(e),
                "success": False
            }
    
    def run_full_test_suite(self):
        """Tam test paketini çalıştır"""
        print("🚀 SENTİO.AI OTOMATİK TEST SİSTEMİ BAŞLIYOR")
        print("=" * 70)
        
        dataset = self.load_test_dataset()
        results = []
        
        # Her testi çalıştır
        for test_id, test_data in dataset.items():
            print(f"🧪 Test: {test_id} ({test_data['expected'].upper()}) - {test_data['category']}")
            result = self.run_single_test(test_id, test_data)
            results.append(result)
            
            if result.get("success") is not None:
                status = "✅ BAŞARILI" if result["success"] else "❌ BAŞARISIZ"
                score = result.get("actual_score", "N/A")
                expected = result.get("expected_range", "N/A")
                print(f"    Skor: %{score} (Beklenen: {expected}) - {status}")
            else:
                print(f"    ❌ HATA: {result.get('error', 'Bilinmeyen hata')}")
            
            time.sleep(1)  # Rate limiting
        
        self.test_results = results
        return self.analyze_results(results)
    
    def analyze_results(self, results):
        """Sonuçları analiz et ve rapor oluştur"""
        print(f"\n{'=' * 70}")
        print("📊 DETAYLI ANALİZ RAPORU")
        print("=" * 70)
        
        # Başarılı testleri ayır
        successful_tests = [r for r in results if r.get("success") == True]
        failed_tests = [r for r in results if r.get("success") == False]
        error_tests = [r for r in results if "error" in r]
        
        # Genel istatistikler
        total_tests = len(results)
        success_rate = len(successful_tests) / total_tests * 100 if total_tests > 0 else 0
        
        print(f"📈 GENEL BAŞARI ORANI: %{success_rate:.1f} ({len(successful_tests)}/{total_tests})")
        
        # İnsan vs AI başarı oranları
        human_tests = [r for r in results if r.get("expected") == "human"]
        ai_tests = [r for r in results if r.get("expected") == "ai"]
        
        human_success = len([r for r in human_tests if r.get("success") == True])
        ai_success = len([r for r in ai_tests if r.get("success") == True])
        
        if len(human_tests) > 0:
            print(f"👤 İNSAN METİNLERİ: %{human_success/len(human_tests)*100:.1f} ({human_success}/{len(human_tests)})")
        if len(ai_tests) > 0:
            print(f"🤖 AI METİNLERİ: %{ai_success/len(ai_tests)*100:.1f} ({ai_success}/{len(ai_tests)})")
        
        # Başarısız testleri analiz et
        if failed_tests:
            print(f"\n❌ BAŞARISIZ TESTLER ({len(failed_tests)} adet):")
            for test in failed_tests:
                expected = test.get("expected", "N/A")
                actual = test.get("actual_score", "N/A")
                print(f"    • {test['test_id']}: Beklenen {expected}, Aldığı %{actual}")
        
        # Kritik sorunları tespit et
        critical_issues = []
        
        # İnsan metinleri yüksek skor alıyorsa
        high_scoring_humans = [r for r in human_tests if r.get("actual_score", 0) > 50]
        if high_scoring_humans:
            critical_issues.append(f"🚨 {len(high_scoring_humans)} insan metni >%50 skor aldı")
        
        # AI metinleri düşük skor alıyorsa  
        low_scoring_ais = [r for r in ai_tests if r.get("actual_score", 100) < 50]
        if low_scoring_ais:
            critical_issues.append(f"🚨 {len(low_scoring_ais)} AI metni <%50 skor aldı")
        
        if critical_issues:
            print(f"\n🚨 KRİTİK SORUNLAR:")
            for issue in critical_issues:
                print(f"    {issue}")
        
        # Öneriler
        print(f"\n💡 ÖNERİLER:")
        if success_rate < 70:
            print("    • Prompt'u daha agresif hale getirin")
            print("    • Türkçe akademik kalıpları güçlendirin")
        if len(human_tests) > 0 and human_success < len(human_tests) * 0.8:
            print("    • İnsan tespiti zayıf - günlük dil özelliklerini vurgulayın")
        if len(ai_tests) > 0 and ai_success < len(ai_tests) * 0.8:
            print("    • AI tespiti zayıf - akademik jargon tespitini güçlendirin")
        
        # CSV raporu kaydet
        self.save_csv_report(results)
        
        return {
            "success_rate": success_rate,
            "human_success_rate": human_success/len(human_tests)*100 if len(human_tests) > 0 else 0,
            "ai_success_rate": ai_success/len(ai_tests)*100 if len(ai_tests) > 0 else 0,
            "critical_issues": critical_issues,
            "failed_tests": failed_tests
        }
    
    def save_csv_report(self, results):
        """Sonuçları CSV dosyasına kaydet"""
        filename = f"sentio_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['test_id', 'expected', 'category', 'actual_score', 'expected_range', 'success', 'comment', 'timestamp', 'text_preview', 'error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        print(f"\n📁 Detaylı rapor kaydedildi: {filename}")
    
    def suggest_prompt_improvements(self, failed_tests):
        """Başarısız testlere göre prompt iyileştirme önerileri"""
        print(f"\n🔧 PROMPT İYİLEŞTİRME ÖNERİLERİ:")
        
        # İnsan metinleri yüksek skor alıyorsa
        human_failures = [t for t in failed_tests if t.get("expected") == "human"]
        if human_failures:
            print("    📝 İnsan metni tespiti için:")
            print("      - Günlük konuşma dilini daha güçlü vurgula")
            print("      - Kişisel deneyim ve duygu ifadelerini prirotize et")
            print("      - Akademik olmayan kelime kullanımını bonus ver")
        
        # AI metinleri düşük skor alıyorsa
        ai_failures = [t for t in failed_tests if t.get("expected") == "ai"]
        if ai_failures:
            print("    🤖 AI metni tespiti için:")
            print("      - Akademik kalıp tespitini daha agresif yap")
            print("      - 'Bu bağlamda', 'kapsamlı' gibi ifadeleri daha sert cezalandır")
            print("      - Pasif cümle yapılarını daha güçlü tespit et")

# KULLANIM ÖRNEĞİ
if __name__ == "__main__":
    RENDER_URL = "https://sentio-ai-backend.onrender.com"
    
    tester = SentioAutoTester(RENDER_URL)
    
    # Sunucu durumu kontrol et ve uyandır
    try:
        print("⏰ Sunucu uyandırılıyor... (Bu işlem 30-60 saniye sürebilir)")
        response = requests.get(RENDER_URL, timeout=60) # Uyandırma için 60 saniye bekle
        if response.status_code == 200:
            print("✅ Sunucu aktif - Otomatik test başlıyor...\n")
            
            # Tam test paketini çalıştır
            analysis_result = tester.run_full_test_suite()
            
            # Başarısız testlere göre öneriler
            if analysis_result["failed_tests"]:
                tester.suggest_prompt_improvements(analysis_result["failed_tests"])
            
            print(f"\n🎯 HEDEF KONTROLÜ:")
            print(f"    • Genel başarı: %{analysis_result['success_rate']:.1f} (Hedef: >%80)")
            print(f"    • İnsan tespiti: %{analysis_result['human_success_rate']:.1f} (Hedef: >%80)")  
            print(f"    • AI tespiti: %{analysis_result['ai_success_rate']:.1f} (Hedef: >%80)")
            
        else:
            print(f"❌ Sunucu erişim hatası: {response.status_code}")
    except requests.exceptions.ReadTimeout:
        print("❌ Sunucu bağlantı hatası: Zaman aşımına uğradı. Sunucu hala uyanıyor olabilir. Lütfen birkaç dakika sonra tekrar deneyin.")
    except Exception as e:
        print(f"❌ Sunucu bağlantı hatası: {e}")
