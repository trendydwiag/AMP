"""
Replace the broken ARTICLES block in demo_seed.py with a clean version
that uses repr() for all content strings, avoiding all quoting issues.
"""
import pathlib, re

SRC = pathlib.Path('apps/core/management/commands/demo_seed.py')
text = SRC.read_text()

# Safe content strings — no inline quotes, no em-dashes in delimiters
ARTICLES_CLEAN = '''ARTICLES = [
    {
        'title': 'Kabulhaden Online Kembali Mengudara: Transformasi Menuju Platform Multi-Media 2026',
        'excerpt': 'Setelah rebranding awal 2026, Kabulhaden Online hadir lebih kuat dengan 14 program aktif.',
        'content': (
            '<p>Awal tahun 2026 menjadi tonggak penting bagi Kabulhaden Online. '
            'Setelah sempat berganti-ganti nama dan lokasi studio, radio komunitas Bandung ini '
            'bertransformasi penuh menjadi Kabulhaden Online \u2014 sebuah platform multi-media '
            'siar digital yang hadir di radio, YouTube, Twitch, dan TikTok.</p>'
            '<p>Bersama Kantina Kultura Network, Kabulhaden Online mengaktifkan kembali '
            'program-program yang sempat tertunda. Saat ini terdapat 14 program aktif yang '
            'berjalan konsisten setiap minggunya.</p>'
            '<p>Kunjungi kabulhaden.online atau ikuti IG @kabulhaden.</p>'
        ),
        'category_name': 'Berita Redaksi',
        'tags': ['transformasi', 'rebranding', 'kabulhaden', 'bandung'],
        'status': 'PUBLISHED',
        'featured': True,
        'days_ago': 3,
    },
    {
        'title': 'Mengenal WarkopKabulhaden: Obrolan Berat yang Bikin Hidup Ringan',
        'excerpt': 'Program bincang komunitas yang dipandu Mba Arien dan Leon kini juga tayang live di YouTube.',
        'content': (
            '<p>WarkopKabulhaden mengambil nama dari konsep warung kopi \u2014 tempat di mana '
            'obrolan berat tentang kehidupan, seni, dan budaya mengalir dengan ringan. Dipandu '
            'oleh Mba Arien (General Manager) dan Leon (CTO), program ini hadir setiap Senin, '
            'Rabu, dan Jumat pukul 15.00\u201317.00 WIB, juga Sabtu.</p>'
            '<p>Konsep kami sederhana: ngobrol yang berat-berat, biar hidup terasa ringan. '
            'Program ini adalah Community Based \u2014 inisiatif langsung dari komunitas, '
            'dengan model siaran mandiri.</p>'
        ),
        'category_name': 'Program',
        'tags': ['warkop', 'komunitas', 'bandung', 'talkshow'],
        'status': 'PUBLISHED',
        'featured': True,
        'days_ago': 7,
    },
    {
        'title': 'Suburban Noise: Punk & SKA Hidup di Udara Kabulhaden Setiap Rabu',
        'excerpt': 'Aan dan Buux Frederiksen bawa energi underground Bandung ke seluruh pendengar streaming.',
        'content': (
            '<p>Setiap Rabu pukul 18.00\u201320.00 WIB, Kabulhaden Online berguncang dengan '
            'energi punk dan SKA dari Suburban Noise. Dipandu Aan dan Buux Frederiksen \u2014 '
            'dua nama besar di scene underground Bandung \u2014 program ini adalah rumah bagi '
            'musik yang selama ini hidup di bawah radar mainstream.</p>'
            '<p>Suburban Noise juga tersedia di TikTok Kabulhaden. Program ini adalah contoh '
            'sempurna dari model Community Based Kabulhaden Online: inisiatif murni dari '
            'komunitas, bukan dari manajemen atas.</p>'
        ),
        'category_name': 'Musik',
        'tags': ['punk', 'ska', 'underground', 'bandung', 'komunitas'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 12,
    },
    {
        'title': "Flight '92: Terbang ke Era 90-an Bersama AdeMuir Setiap Selasa",
        'excerpt': 'Ade Purnama (founder Kabulhaden) host perjalanan nostalgia musikal ke dekade terbaik.',
        'content': (
            "<p>Flight '92 tayang setiap Selasa pukul 20.00\u201322.00 WIB, dipandu langsung "
            'oleh Ade Purnama alias AdeMuir \u2014 founder sekaligus CEO Kabulhaden Online, '
            'musisi dari band Pure Saturday.</p>'
            '<p>Tahun 90-an adalah dekade di mana musik benar-benar berbicara. Britpop, '
            'grunge, alternative \u2014 semua punya kedalaman yang tak lekang oleh waktu. '
            'Bersama co-host Anggicau, program ini memadukan playlist cerdas dengan '
            'storytelling personal yang hangat.</p>'
        ),
        'category_name': 'Musik',
        'tags': ['90s', 'alternative', 'nostalgia', 'britpop', 'grunge'],
        'status': 'PUBLISHED',
        'featured': True,
        'days_ago': 18,
    },
    {
        'title': 'Kabulhaden Online: 10 Tahun Mengudara dari Jalan Multatuli Bandung',
        'excerpt': 'Dari server radio cast gratisan di 2016 ke platform multi-media 2026 \u2014 perjalanan satu dekade.',
        'content': (
            '<p>Agustus 2016. Dari sebuah ruangan di Jalan Multatuli No. 5, Kota Bandung, '
            'Ade Purnama alias Ade Muir \u2014 musisi dari band Pure Saturday \u2014 mulai '
            'menyiarkan radio streaming pribadi menggunakan server radio cast gratisan.</p>'
            '<p>Dari sana, Kabulhaden Online tumbuh: paid server, domain sendiri, lalu pada '
            '2017 kolaborasi dengan Dinas Pariwisata Kota Bandung melalui Bandung Creative Hub '
            '(BCH). Nama Kabulhaden berasal dari cerita wayang golek Alm. Asep Sunandar Sunarya '
            'tentang tokoh dari Belanda yang disebut Tuan Kabulhaden.</p>'
        ),
        'category_name': 'Berita Redaksi',
        'tags': ['sejarah', 'bandung', 'komunitas', 'milestone'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 25,
    },
    {
        'title': 'Sound of Heavy & CadasPersada: Dua Wajah Metal di Kabulhaden Online',
        'excerpt': 'PanjiOxen dan ArizMetalGodz bawa scene metal Bandung ke udara setiap Selasa.',
        'content': (
            '<p>Komunitas metal Bandung sudah lama dikenal sebagai salah satu yang terkuat di '
            'Indonesia. Kabulhaden Online memberikan ruang bagi komunitas ini melalui Sound of '
            'Heavy (16.00\u201318.00 WIB) dan CadasPersada (18.00\u201319.00 WIB) setiap Selasa.</p>'
            '<p>Sound of Heavy mengangkat metal, hard rock, dan aliran berat lainnya. '
            'CadasPersada merayakan warisan rock klasik Indonesia. Keduanya dipandu PanjiOxen '
            'dan ArizMetalGodz. Metal bukan genre, metal adalah gaya hidup \u2014 kami di sini '
            'untuk menjaga api itu tetap menyala.</p>'
        ),
        'category_name': 'Musik',
        'tags': ['metal', 'rock', 'bandung', 'komunitas', 'underground'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 32,
    },
    {
        'title': 'Visi Kabulhaden Online: Episentrum Suara Kreatif Kota Bandung',
        'excerpt': 'Tiga misi yang memandu setiap program dan keputusan Kabulhaden Online.',
        'content': (
            '<p>Visi Kabulhaden Online: Terdapat episentrum suara dan energi kreatif yang '
            'menghubungkan, menginspirasi, serta menggerakkan berbagai komunitas lokal kota '
            'Bandung untuk lebih banyak lagi menghasilkan karya-karya kreatif.</p>'
            '<p><strong>Misi 01</strong> \u2014 Katalisator Kolaborasi Komunitas: membangun '
            'jembatan antar-komunitas kreatif di Bandung (seni rupa, musik, literatur, desain, '
            'teknologi).<br>'
            '<strong>Misi 02</strong> \u2014 Media edukasi, sosialisasi dan informasi dengan '
            'pemberdayaan karya industri kreatif.<br>'
            '<strong>Misi 03</strong> \u2014 Pemanfaatan media integratif: audio konvensional '
            'plus digital interaktif (YouTube, Twitch, TikTok).</p>'
        ),
        'category_name': 'Berita Redaksi',
        'tags': ['visi', 'misi', 'komunitas', 'bandung', 'kreatif'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 40,
    },
    {
        'title': 'Kabulhaden Online Bergabung dengan Bandung Creative Hub sejak 2017',
        'excerpt': 'Kolaborasi dengan Dinas Pariwisata Kota Bandung membuka babak baru pertumbuhan komunitas.',
        'content': (
            '<p>Pada 2017, Kabulhaden Online mendapat kesempatan bekerja sama dengan Dinas '
            'Pariwisata (Dispar) Kota Bandung melalui program Bandung Creative Hub (BCH). '
            'Kabulhaden menjadi pelaksana kegiatan kreatif Kota Bandung untuk unit Penyiaran '
            'Radio.</p>'
            '<p>Ini membuka dukungan komunitas yang lebih luas: peralatan siaran, penyiar '
            'bertalenta dari komunitas musik aktif Bandung, dan lahirnya program-program baru. '
            'Kolaborasi dengan Dispar Kota Bandung berlanjut hingga kini.</p>'
        ),
        'category_name': 'Komunitas',
        'tags': ['bandung-creative-hub', 'dispar', 'kolaborasi', 'bandung'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 50,
    },
    {
        'title': 'Tim Inti Kabulhaden Online: Ade Purnama, Leon, dan Mba Arien',
        'excerpt': 'Tiga orang di balik visi dan operasional platform multi-media Bandung ini.',
        'content': (
            '<p><strong>Ade Purnama \u2014 CEO.</strong> Founder Kabulhaden Online. Musisi '
            "dari band Pure Saturday yang memulai Kabulhaden Online pada Agustus 2016. Host "
            "Flight '92 setiap Selasa malam.</p>"
            '<p><strong>Leon \u2014 CTO.</strong> Otak teknis Kabulhaden Online, memastikan '
            'stream tetap hidup dan server berjalan. Co-host WarkopKabulhaden bersama Mba Arien.</p>'
            '<p><strong>Mba Arien \u2014 General Manager.</strong> Wajah paling dikenal '
            'Kabulhaden Online, co-host WarkopKabulhaden, jantung operasional komunitas platform.</p>'
        ),
        'category_name': 'Profil',
        'tags': ['tim', 'profil', 'ceo', 'bandung', 'kabulhaden'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 60,
    },
    {
        'title': 'General Lifestyle vs Community Based: Dua Model Program Kabulhaden',
        'excerpt': 'Memahami dua jenis konten yang membentuk ekosistem siaran Kabulhaden Online.',
        'content': (
            '<p><strong>General Lifestyle</strong> \u2014 program pada cloud dengan AutoDj '
            'pada tema kesamaan jenis musik. Contoh: IndIeDieu, Popmix 9020, Motown/Soul, '
            'JP City Pop. Berjalan otomatis dengan playlist terprogram.</p>'
            '<p><strong>Community Based</strong> \u2014 inisiasi program dari komunitas '
            'dengan model siaran mandiri. Contoh: WarkopKabulhaden, Suburban Noise, Sound of '
            "Heavy, Flight '92, Corner Table. Ini adalah jiwa Kabulhaden Online \u2014 "
            'otentik dan didorong oleh cinta komunitas.</p>'
        ),
        'category_name': 'Program',
        'tags': ['program', 'general-lifestyle', 'community-based', 'siaran'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 70,
    },
    {
        'title': 'SvArtSound: Portal Black Metal Skandinavia di Bandung',
        'excerpt': 'KokoRaven hadirkan Mayhem, Darkthrone, dan scene extreme metal global setiap Minggu malam.',
        'content': (
            '<p>SvArtSound adalah program paling niche di Kabulhaden Online \u2014 dan justru '
            'itulah kekuatannya. Setiap Minggu pukul 19.00\u201321.00 WIB, KokoRaven membuka '
            'portal ke dunia Black Metal Skandinavia dan Extreme Metal global.</p>'
            '<p>Mayhem, Burzum, Darkthrone, Emperor \u2014 nama-nama legendaris mengalun '
            'melalui udara Kabulhaden. Black Metal adalah pengalaman total \u2014 filosofis, '
            'estetis, musikal. SvArtSound adalah bukti bahwa Kabulhaden memberi ruang '
            'untuk semua genre.</p>'
        ),
        'category_name': 'Musik',
        'tags': ['black-metal', 'extreme-metal', 'skandinavia', 'underground'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 14,
    },
    {
        'title': 'Rumpies Daddies Podcast: Suara Kehidupan Kreatif Bandung',
        'excerpt': 'Podcast mingguan Kabulhaden Online tentang musik, komunitas, dan industri kreatif.',
        'content': (
            '<p>Rumpies Daddies Podcast hadir setiap Senin malam pukul 20.00\u201322.00 WIB '
            'sebagai ruang obrolan mendalam tentang kehidupan kreatif Bandung. Setiap episode '
            'menghadirkan perspektif segar tentang musik, seni, dan industri budaya dari '
            'orang-orang yang benar-benar hidup di dalamnya.</p>'
            '<p>Tidak ada naskah, tidak ada pertanyaan yang disiapkan \u2014 murni obrolan '
            'yang jujur dan mengalir. Program ini menjadi jembatan antara Kabulhaden Online '
            'dan ekosistem kreatif Bandung yang lebih luas.</p>'
        ),
        'category_name': 'Program',
        'tags': ['podcast', 'komunitas', 'bandung', 'kreatif'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 5,
    },
]
'''

# Replace the ARTICLES block
pattern = r'(?s)ARTICLES = \[.*?\]\n(?=\nARTICLE_CATEGORIES)'
new_text = re.sub(pattern, ARTICLES_CLEAN, text)

if new_text == text:
    print("ERROR: ARTICLES pattern not found")
else:
    SRC.write_text(new_text)
    print("OK: ARTICLES block replaced")
