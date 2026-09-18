# KutayX7's VRChat Avi Scaler

![lisans](https://img.shields.io/badge/lisans-MIT-green?style=flat)
![platformlar](https://img.shields.io/badge/platformlar-Linux%7CWindows%7CAndroid%7CmacOS-blue?style=flat)
![python](https://img.shields.io/badge/python-3.12%2B-blue?style=flat)

OSC aracılığıyla VRChat'teki avatarlarınızı boyutlandırmak için bir araç.

**UYARI:** Bu %100 ücretsiz ve açık kaynaklı bir yazılımdır (FOSS). Resmi güncel depo bağlantısı: https://github.com/KutayX7/vrc-avi-scaler
Bu depodan dışında dağıtılan resmi paketler bulunmamaktadır.

| [English](/README.md) |

## Özellikler

- VRChat ile iletişim kurmak için OSC kullanır.
- Avatarınızı dünya ve VRChat tarafından izin verilen herhangi bir boyuta ölçeklendirebilirsiniz.
  * Dünya tarafından kısıtlanmadıkça, 1 cm - 10 km arası.
  * (Ancak IK ve görünüm hatalarından dolayı 20cm-100m aralığının ötesine geçilmesi önerilmez.)
- Anında veya belirli bir süre boyunca yumuşak bir şekilde boyutlandırma seçeneği.
- Üçüncü taraf ölçeklendirme sistemleriyle uyumluluk:
  * [Jackal Scaling System](https://spacejackal.gumroad.com/l/JackalScaler) ile tam uyumluluk.
  * [OpenVRCScaler](https://github.com/SkyeCA/OpenVRCScaler) ile tam uyumluluk.
  * [Mag's Scale Adjuster](https://magww.gumroad.com/l/scale) ile kısmi uyumluluk.
  * [Real Size Scale Adjuster](https://booth.pm/ja/items/8255001) (https://github.com/KutayX7/vrc-avi-scaler/issues/7)
  * [SizeOSC](https://anmeire.gumroad.com/l/sizeosc) (değerlendiriliyor)
  * (Zaman geçtikçe daha fazlası eklenecektir.)
- Windows, Linux, macOS, Android/Quest (Termux üzerinden) ve muhtemelen diğer bazı posix platformlarında çalışmalıdır.
  * Ancak şu ana kadar yalnızca Linux ve Android'de test ettim.
- İsterseniz VRChat ve bu programı ayrı cihazlarda çalıştırabilirsiniz.
  * Varsayılan olarak OSCQuery ile otomatik bağlantı.
  * VRChat Windows OSCQuery sınırlamaları için otomatik geçici çözümler içerir.
- Çeşitli komutlar, [tüm komutlar](#tüm-komutlar)a bakın.
- Çevrimdışı yerelleştirme (Offline localisation).

## Kurulum

> [!NOTE]
> Linux'a uygulanan adımların neredeyse tamamı macOS ve Android (Termux) için de geçerlidir.

### Ön Gereksinimler

* Genel olarak stabil bir internet bağlantısı.
* Bir terminal emülatörü (Neredeyse tüm masaüstü işletim sistemlerinde önceden yüklü gelir. Android/Quest'te Termux kullanabilirsiniz.)
* Python (3.12+)
  - Windows kullanıcılarının bunu manuel olarak kurması gerekir.
    - Ya [resmi Python web sitesinden](https://www.python.org/downloads/windows/) ya da [Microsoft Store'dan](https://apps.microsoft.com/detail/9pnrbtzxmb4z?ocid=webpdpshare) kurabilirsiniz.
    - Kurulum sırasında `PATH'e Ekle` (veya benzeri) seçeneğini görürseniz, bu seçeneğin işaretli olduğundan emin olun!
  - Linux'ta genellikle önceden yüklüdür. Ancak daha eski bir sürümünüz varsa, çalışıp çalışmayacağını söyleyemem. **SİSTEM PYTHON'UNUZU MANUEL OLARAK GÜNCELLEMEYİN!**
  - Termux'ta ise `pkg install python -y` komutunu çalıştırarak kurun.
  - Python'un kurulu olup olmadığını ve sürümünü şu komutları çalıştırarak kontrol edebilirsiniz:
    - `python3 --version` veya `python --version` (bunlardan en az birinin çalışması yeterli)
* Git
  - Git, programın ana işlevleri için gerekli değildir ancak önerilen kurulum yöntemi ve güncelleme betiğinin çalışması için gereklidir.
  - Windows ile önceden yüklenmiş olarak gelmez. Git'i kurmak için `winget install --id Git.Git -e --source winget` komutunu çalıştırın ardından terminalinizi yeniden başlatın.
  - Birçok linux dağıtımı git ile birlikte gelir. Ama yoksa, lütfen linux dağıtımınıza göre aşağıdaki komutları kullanın.

      - Linux Mint / Pop!_OS / Ubuntu / Kubuntu / Debian

        ```bash
        sudo apt update && sudo apt install git
        ```

      - Fedora / Nobara

        ```bash
        sudo dnf install git
        ```

      - Arch Linux / CachyOS / EndeavourOS / Manjaro / Garuda

        ```bash
        sudo pacman -S git
        ```

      - Termux

        ```bash
        pkg install git
        ```

  - Git'in kurulu olup olmadığını ve sürümünü şu komutları çalıştırarak kontrol edebilirsiniz: `git --version`

  - Eğer değişmez (immutable) bir linux dağıtımındaysanız ve git'iniz yoksa, şu an için 2 seçeneğiniz var.
    - Dağıtımınız tarafından önerilen şekilde git cli kurun.
    - Kod > ZIP İndir.
      - Bu, `.git/` dizinini içermeyeceği için güncelleme betiği işlev göremeyecektir.
      - Diğer her şey (sistem python'unuz gereksinimleri karşılıyorsa) çalışmalıdır.
      - Zip dosyasını ana dizininizdeki bir yere çıkarın, içine girin (`cd` ile) ve aşağıdaki önerilen kurulum yönteminin son adımını yapın.
      - Bu kadar!

### Önerilen Kurulum Yöntemi

1. Terminalinizi açın:
  * Windows'ta, `Win+R` tuşuna basın ve `wt` (veya `cmd`) yazıp `Enter` tuşuna basın.
  * Linux'ta, farklılık gösterebilir ancak genellikle `Ctrl+Alt+T`.
  * Android'de, Termux kullanın.
2. Depoyu klonlayın:
  * `git clone --depth 1 --no-single-branch "https://github.com/KutayX7/vrc-avi-scaler"`
    * `--depth 1`, sadece en son dosyaları (geçmişleri olmadan) indirir.
    * `--no-single-branch`, güncelleme betiğinin diğer dallara geçebilmesini sağlar.
  * Bu, mevcut dizinde (`vrc-avi-scaler` adlı bir klasör oluşturacaktır (başka bir dizine geçmediyseniz muhtemelen home/kullanıcı dizininiz) ve bu deponun `main` dalını içerecektir.
  * Daha önce bu klasöre sahipseniz (muhtemelen önceki bir sürümden dolayı), bu komut başarısız olacaktır. Bu yüzden bunu çalıştırmadan önce lütfen o klasörü silin.
3. Klonlanan dizine geçin:
  * `cd vrc-avi-scaler`
4. Kurulum betiğini çalıştırın:
  * `python3 setup.py` veya `python setup.py` veya `py setup.py` (hangisi çalışıyorsa)
  * Bir sanal ortam oluşturacaktır (zaten yoksa).
  * Ardından bağımlılıkları sanal ortama kuracaktır.
  * Linux'ta, `start.sh` dosyasını da çalıştırılabilir olarak işaretler.
  * Ayrıca bir masaüstü girişi oluşturur (mümkün ve destekleniyorsa).
    * Yalnızca masaüstü linux dağıtımlarında desteklenir, şimdilik.
    * Masaüstü girişi oluşturmayı atlamak için sonuna ` --no-desktop ` ekleyin.
  * Termux'ta ise bir Termux kısayolu oluşturacaktır. Bunu ana ekranınıza widget olarak eklemek için [Termux:Widget](https://github.com/termux/termux-widget) uygulamasını kullanabilirsiniz.

## Güncellemeler

Lütfen her güncellemeden sonra bu README'yi kontrol edin.

Eğer bunu bir paket yöneticisinden kurduysanız (topluluk tarafından bakılıyor), güncellemeleri almak için onu kullanın ve bu bölümün geri kalanını görmezden gelin.

Eğer bu yayınlardan veya ZIP olarak indirerek kurduysanız, eskisini silin ve tekrar kurun; bu bölümün geri kalanını görmezden gelin.

Önerilen kurulum yöntemini kullandıysanız, güncellemeler için otomatik bir kontrol yoktur, bu yüzden manuel güncellemeniz gerekir. Ya masaüstü girişine sağ tıklayıp `Update` (Güncelle) seçeneğini seçin VEYA güncelleme betiğini çalıştırın (`cd vrc-avi-scaler` sonra `python update.py`). Ardından talimatları izleyin (varsa).

> [!WARNING]
> Ortamınızdaki değişikliklerden (sistem güncellemeleri, python güncellemeleri, dizin değişiklikleri) sonra programı çalıştıramazsanız, masaüstü girişine sağ tıklayıp `Repair` (Onar) butonuna basın VEYA `setup.py` betiğini tekrar çalıştırın. Bunlar işe yaramazsa, `update.py` betiğini çalıştırın. Bu da işe yaramazsa, temiz bir kurulum yapın.

## Kullanım

Programı başlatmak için:
  * Windows'ta, `start_windows.bat` betiğini çalıştırın (çift tıklayabilirsiniz).
    * Kolaylık olması açısından masaüstünüze bir kısayol oluşturmayı düşünebilirsiniz.
    * Sağ tık > Gönder > Masaüstü (kısayol oluştur)
  * Linux'ta:
    * Masaüstü girişini kullanın (varsa).
    * Veya terminalinizde `start.sh` betiğini çalıştırın.
      * `cd vrc-avi-scaler` sonra `./start.sh`
      * KDE için, sağ tıklayıp `Run In Konsole` yapabilirsiniz.
    * Başka bir yolla kurduysanız ve hiçbir şey açılmıyorsa:
      * Çalıştırılabilir dosyaya bir masaüstü girişi oluşturun ve terminalde çalıştırma seçeneğinin işaretli olduğundan emin olun.
      * Bunu nasıl yapacağınız, uygulamayı nasıl kurduğunuza ve hangi masaüstü ortamını kullandığınıza bağlıdır.
  * Termux'ta:
    * Ya [Termux:Widget](https://github.com/termux/termux-widget) uygulamasını kurarak başlatma betiğini ana ekranınıza bir widget olarak ekleyin VEYA `.shortcuts/vrc-avi-scaler.sh` dosyasını çalıştırın.

VRChat'te OSC'yi etkinleştirdiğinizden emin olun! (Ya ayarlardan ya da Eylem Menüsü > Seçenekler > OSC).

> [!WARNING]
> Eğer bu programı çalıştırmadan önce VRChat'te zaten oturum açmışsanız veya OSC'yi açtıysanız, lütfen avatarınızı yeniden yükleyin (böylece avatarınız, izleme türünüz ve dünya hakkında doğru bilgileri toplayabilir).

> [!WARNING]
> OSCQuery özelliği etkin durumdayken (varsayılan), aynı ağda birden fazla VRChat örneği çalıştırmamalısınız (OSC etkinleştirilmiş). Programı garip şekillerde yanıltabilirler.

> [!TIP]
> Yumuşak ölçekleme ile ilgili sorunlar yaşıyorsanız, oyun içi FPS'nizi sınırlayın ve `fps` komutunu kullanın.
Örneğin, oyun içi FPS limitinizi 120 FPS olarak ayarladıysanız, `fps 120` komutunu kullanın. Daha sonra tekrar yazmak zorunda kalmamak için bunu kaydetmek amacıyla `save` komutunu kullanın.

> [!TIP]
> Gelişmiş yapılandırma için yapılandırma dosyasını kontrol edin. Yoksa, program çalıştığında oluşturulacaktır. Mevcut yapılandırma dosyasını açmak için `config` (uygulama içi) komutunu kullanabilirsiniz.

> [!TIP]
> Varsayılan olarak, çalışma zamanı yapılandırma değişiklikleri (`fps` gibi) otomatik kaydedilmez. Yapılandırmanın çıkışta otomatik kaydedilmesini sağlamak için `autosave` komutunu kullanabilirsiniz.

## [Sorunlar](https://github.com/KutayX7/vrc-avi-scaler/issues)

LÜTFEN GERİ BİLDİRİM VERİN! Şimdilik verebileceğiniz en büyük destek bu olacaktır. <3

Tüm yapıcı geri bildirimler kabul edilir. Hata raporları, özellik istekleri vb.
Yeni bir sorun açmadan önce lütfen resmi ana daldaki en son sürümü kullandığınızdan emin olun (uygunsa). Eğer bir hata gayriresmi bir dağıtımdan kaynaklanıyorsa, lütfen oraya rapor edin.
Aynı sorunu birden fazla kez oluşturmaktan kaçının.

Sorularınızı [Soru & Cevap](https://github.com/KutayX7/vrc-avi-scaler/discussions/categories/q-a) bölümünde sorabilirsiniz.

## [Soru & Cevap](https://github.com/KutayX7/vrc-avi-scaler/discussions/categories/q-a)

**S: Güvenli mi?**

C: Kaynak kodunu kontrol edebilirsiniz. En tehlikeli kısımlar bağımlılıklar ve güncelleme sistemidir. Ayrıca, bunu kullanmak için moderasyonla karşılaşmaktan endişe ediyorsanız, kötüye kullanmadığınız sürece VRChat'in size herhangi bir moderasyon eylemi yapması olası değildir. Bu program yasa dışı hiçbir yöntem kullanmaz.

**S: Android veya Quest 2/3'te çalışıyor mu?**

C: Evet. Ama. Android/Quest'te oynuyorsanız, uygulamayı ayrı bir cihazda (tercihen bir Windows veya Linux PC) çalıştırmanız önerilir. Aynı Wi-Fi ağı üzerindeler sürece otomatik olarak bağlanabilmelidirler. Aynı Android cihazında çalıştırmak, düzgün yapılandırılmadıkça işlevselliğin azalmasına neden olabilir.

**S: Yumuşak ölçekleme avatarımı neden tuhaf yapıyor?**

C: Muhtemelen şu VRChat hatalarıyla ilgilidir:
  * https://feedback.vrchat.com/bug-reports/p/flicker-when-changing-avatar-height
  * https://feedback.vrchat.com/bug-reports/p/jittering-view-effect-when-lerping-osc-avatar-scaling
  * (Onları hafifletmek için elimden geleni yaptım ancak deneyim mükemmel olmayabilir.)

**S: Kendim paketleyip dağıtabilir miyim?**

C: Lütfen çekinmeyin ama lütfen [orijinal depoya](https://github.com/KutayX7/vrc-avi-scaler) yönlendiren bir bağlantı koyun.
Ve deponun veya kurulum/güncelleme betiklerinde bozulabilecek değişiklikler olabileceğini unutmayın (Ana daldaki şeyleri bozmamak için elimden geleni yapacağım ama olabilir). Kullanıcıları her zaman önerilen kurulum yöntemini denemeleri konusunda bilgilendirirseniz minnettar olurum.

**S: Bir GUI planı var mı?**

C: Lütfen [issue #19](https://github.com/KutayX7/vrc-avi-scaler/issues/19) a bakınız. Ayrıca GUI'li alternatif uygulamalar mevcut. Eğer geliştiriciyseniz bunu kendi GUI projelerinizin backendi olarak kullanmaktan çekinmeyin.

**S: X ölçeklendirme sistemiyle uyumluluk var mı?**

C: Bu program uyumluluk gözetilerek tasarlanmıştır, o yüzden bunun hakkında bir sorun açın ve ben incelerim. Eğer bunu kullanan halka açık bir avatar verebilirseniz ve/veya kullandığı parametreleri belirtirseniz, daha erken ekleyebilirim.

**S: Başka OSC uygulamalarını bu programla birlikte kullanabilir miyim?**

C: Evet. Ancak başka bir OSC ölçeklendirme uygulamasıysa, kullanım sırasında herhangi bir yarış durumu (race condition) oluşmasını önlemek için `nocompat` komutunu kullanmak isteyebilirsiniz.

**Daha fazla sorunuz mu var?** [Tartışmalar](https://github.com/KutayX7/vrc-avi-scaler/discussions).

## Tüm Komutlar

- `<sayı>[birim]` Göz yüksekliğine göre boyutlandırır.
  - Geçerli örnekler: `1`, `173cm`, `2.1 m`, `200mm`, `1 mile`, `6ft`, `5000 feet`
  - Birim belirtilmezse varsayılan birim `metre`dir.
- `smooth [saniye]` Yumuşak ölçeklendirme süresini ayarlar.
  - Kısa versiyon: `s [saniye]`
  - Kaydedilmez. Varsayılan olarak devre dışıdır.
- `help` Bütün komutları gösterir.
- `exit` Uygulamadan çıkar. Otomatik kaydetme açıksa yapılandırmayı kaydeder.
  - Kısa versiyon: `q`
- `framerate <fps>` Beklenen FPS'yi ayarlar.
  - Kısa versiyon: `fps <fps>`
  - Bu aynı zamanda `frequency` değerini de sıfırlar!
- `frequency <oran>` Yumuşak ölçeklendirme adım hızını (saniyede) ayarlar.
  - Kısa versiyon: `freq <oran>`
  - Kaydedilmez.
- `clear` Ekranı temizler.
  - Kısa versiyon: `cls`
- `save` Mevcut yapılandırmayı manuel olarak kaydeder.
- `autosave` Otomatik kaydetmeyi etkinleştirir.
- `noautosave` Otomatik kaydetmeyi devre dışı bırakır.
- `configure` Yapılandırma dosyasını varsayılan metin düzenleyicinizde açar.
  - Kısa versiyon: `cfg`
  - Termux kullanıcılarının bunu düzgün çalıştırması için `~/.termux/termux-properties` içinde `allow-external-apps` özelliğini etkinleştirmesi gerekir.
- `min`/`max` Dünya tarafından belirlenen min/maks yüksekliğe göre boyutlandırır.
- `normal` Normal boyuta geri döner.
  - Kısa versiyonlar: `norm`, `base`
- `info` Avatarınız ve dünya limitleriniz hakkında çeşitli bilgiler gösterir.
  - Eğer mod (VR/masaüstü) yanlış algılanmışsa, `vr` veya `desktop` komutunu kullanın.
  - Kısa versiyon: `i`
- `vr` VR modunu seçer (VRMode'u 1 olarak hatırlar).
- `desktop` masaüstü modunu seçer (VRMode'u 0 olarak hatırlar).
  - Kısa versiyon: `nvr`
- `lock_vrmode` Mevcut VRMode'un otomatik olarak değiştirilmesini engeller.
  - Avatar/dünya değişikliklerinden sonra VR'da olmanıza rağmen masaüstü olarak algılanmaya devam ediyorsanız bunu kullanın.
  - Kısa versiyon: `lm`
- `osc_debug` OSC mesaj günlük kaydını etkinleştirir/devre dışı bırakır.
- `osc_send <adres> [parametreler]` Özel bir OSC mesajı gönderir.
  - parametreler: `<tip>[değer]`, örnekler: `i123 f0.5 T F`
  - Dizeler (`s`) desteklenmez.
  - Tam örnek: `osc_send /avatar/eyeheight f0.5`
- `nocompat` Tüm ölçeklendirme sistemi uyumluluk özelliklerini devre dışı bırakır.
  - Kısa versiyon: `pure`
  - Kaydedilmez.
- `override` Dünya limitlerini unutur.
  - Sadece bazı aksaklıkları aşmak için kullanılır. Kesin dünya limitlerini atlamayacaktır.
  - Kısa versiyon: `o`
- `instant` Yumuşak ölçeklendirmeyi devre dışı bırakır.
  - Aynı şey: `s 0`
- `delay <saniye> <komut>` Verilen komutu belirtilen süreden sonra çalıştırır.
  - Kısa version: `delay <saniye> <komut>`
- `fix_osc_client` OSC istemcisini en son algılanan VRChat adresi ve bağlantı noktasına yeniden başlatır.
  - Genellikle otomatik olarak çözüldüğü için muhtemelen bunu kullanmanız gerekmeyecektir.

> [!TIP]
> Komutları noktalı virgül (`;`) ile ayırarak tek bir satırda birden fazla komut çalıştırabilirsiniz. Bu yöntem, `delay` ile birlikte kullanıldığında, zaman ayarlı bir komut dizisi oluşturmanıza olanak tanır.

## Katkıda Bulunma (Contribution)

- Lütfen önce bir sorun açın ki insanlar aynı konuda çalışmasın.
- Lütfen acil veya basit olmadığınız sürece pull request oluşturmaktan kaçının.
- Taslak olmayan pull request'lerde bozulmaya neden olacak commit'lerden kaçının.
- Yapay zeka tarafından oluşturulan/yardımlanan kod için:
  - Siz (insan) kodun tamamını okumalı ve anlamalısınız.
  - Öncelikle kendiniz test etmeli ve *her şeyin çalıştığından* emin olmalısınız.
- Yapay zeka tarafından yapılan çeviriler, bir insan tarafından doğrulanırsa sorun değildir.
- Python kodlama kurallarına uyun (https://peps.python.org/pep-0008/).
  - Bazı durumlarda istisnalar yapılabilir.
- Bağımlılık eklemekten kaçının.
- Kötü niyetli kod/prosedür/içerik olmamalıdır.
- Ortalama kullanıcının kullanıcı deneyimi önemlidir.
- Commit'larda/PR'larda kelime oyunları yapmaktan çekinmeyin.
- Sağladığınız kod, bu depodaki aynı [lisans](/LICENSE) (MIT Lisansı) altında lisanslanacaktır.

## Yasal Uyarı (Disclaimer)
> Bu proje ne VRChat ile ne de diğer avatar ölçeklendirme sistemi yaratıcılarıyla bağlantılıdır ne de onlar tarafından onaylanmıştır (aksi belirtilmedikçe).
> Bu dosyanın çevirisinde yapay zeka (gemma4:e4b) kullanılmıştır.

