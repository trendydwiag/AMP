"""
Replace ARTICLES through SONGS_NOW_PLAYING constants in demo_seed.py
with real Kabulhaden pitch-deck data.
"""
import re, pathlib

SRC = pathlib.Path('apps/core/management/commands/demo_seed.py')
text = SRC.read_text()

NEW_BLOCK = '''ARTICLES = [
    {
        'title': 'Kabulhaden Online Kembali Mengudara: Transformasi Menuju Platform Multi-Media 2026',
        'excerpt': 'Setelah rebranding awal 2026, Kabulhaden Online hadir lebih kuat dengan 14 program aktif.',
        'content': '<p>Awal tahun 2026 menjadi tonggak penting bagi Kabulhaden Online. Setelah sempat berganti-ganti nama dan lokasi studio, radio komunitas Bandung ini bertransformasi penuh menjadi "Kabulhaden Online" — sebuah platform multi-media siar digital yang tidak hanya bersuara di radio, tetapi juga hadir di YouTube, Twitch, dan TikTok.</p><p>"Ini bukan sekadar ganti nama. Ini adalah penguatan visi awal kami: menjadi episentrum suara dan energi kreatif yang menghubungkan komunitas-komunitas lokal Kota Bandung," ujar Ade Purnama, CEO Kabulhaden Online.</p><p>Bersama Kantina Kultura Network, Kabulhaden Online mengaktifkan kembali program-program yang sempat tertunda, kini beroperasi dari studio yang lebih baik. Saat ini terdapat 14 program aktif yang berjalan konsisten setiap minggunya.</p>',
        'category_name': 'Berita Redaksi',
        'tags': ['transformasi', 'rebranding', 'kabulhaden', 'bandung'],
        'status': 'PUBLISHED',
        'featured': True,
        'days_ago': 3,
    },
    {
        'title': 'Mengenal WarkopKabulhaden: Obrolan Berat yang Bikin Hidup Ringan',
        'excerpt': 'Program bincang komunitas yang dipandu Mba Arien dan Leon kini juga tayang live di YouTube.',
        'content': '<p>WarkopKabulhaden mengambil nama dari konsep warung kopi — tempat di mana obrolan berat tentang kehidupan, seni, dan budaya mengalir dengan ringan. Dipandu oleh Mba Arien (General Manager) dan Leon (CTO), program ini hadir setiap Senin, Rabu, dan Jumat pukul 15.00\u201317.00 WIB, juga Sabtu.</p><p>"Konsep kami sederhana: ngobrol yang berat-berat, biar hidup terasa ringan. Kami percaya bahwa topik-topik besar bisa dibicarakan dengan cara yang mengundang banyak orang untuk ikut berpikir," kata Mba Arien.</p>',
        'category_name': 'Program',
        'tags': ['warkop', 'komunitas', 'bandung', 'talkshow'],
        'status': 'PUBLISHED',
        'featured': True,
        'days_ago': 7,
    },
    {
        'title': 'Suburban Noise: Punk & SKA Hidup di Udara Kabulhaden Setiap Rabu',
        'excerpt': 'Aan dan Buux Frederiksen bawa energi underground Bandung ke seluruh pendengar streaming.',
        'content': '<p>Setiap Rabu pukul 18.00\u201320.00 WIB, Kabulhaden Online berguncang dengan energi punk dan SKA dari Suburban Noise. Dipandu Aan dan Buux Frederiksen \u2014 dua nama besar di scene underground Bandung \u2014 program ini adalah rumah bagi musik yang selama ini hidup di bawah radar mainstream.</p><p>Suburban Noise juga tersedia di TikTok Kabulhaden. Program ini adalah contoh sempurna dari model Community Based Kabulhaden Online: inisiatif murni dari komunitas.</p>',
        'category_name': 'Musik',
        'tags': ['punk', 'ska', 'underground', 'bandung', 'komunitas'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 12,
    },
    {
        'title': "Flight \'92: Terbang ke Era 90-an Bersama AdeMuir Setiap Selasa",
        'excerpt': "Ade Purnama (founder Kabulhaden) host-i perjalanan nostalgia musikal ke dekade terbaik.",
        'content': "<p>Flight \'92 tayang setiap Selasa pukul 20.00\u201322.00 WIB, dipandu langsung oleh Ade Purnama alias AdeMuir \u2014 founder sekaligus CEO Kabulhaden Online, musisi dari band Pure Saturday.</p><p>\"Tahun 90-an adalah dekade di mana musik benar-benar berbicara. Britpop, grunge, alternative \u2014 semua punya kedalaman yang tak lekang oleh waktu,\" ujar Ade Purnama. Bersama co-host Anggicau, program ini memadukan playlist cerdas dengan storytelling personal yang hangat.</p>",
        'category_name': 'Musik',
        'tags': ['90s', 'alternative', 'nostalgia', 'britpop', 'grunge'],
        'status': 'PUBLISHED',
        'featured': True,
        'days_ago': 18,
    },
    {
        'title': 'Kabulhaden Online: 10 Tahun Mengudara dari Jalan Multatuli Bandung',
        'excerpt': 'Dari server radio cast gratisan di 2016 ke platform multi-media 2026 — perjalanan satu dekade.',
        'content': '<p>Agustus 2016. Dari sebuah ruangan di Jalan Multatuli No. 5, Kota Bandung, Ade Purnama alias Ade Muir \u2014 musisi dari band Pure Saturday \u2014 mulai menyiarkan radio streaming pribadi menggunakan server radio cast gratisan.</p><p>Dari sana, Kabulhaden Online tumbuh: paid server, domain sendiri, lalu pada 2017 kolaborasi dengan Dinas Pariwisata Kota Bandung melalui Bandung Creative Hub (BCH). Nama "Kabulhaden" berasal dari cerita wayang golek Alm. Asep Sunandar Sunarya tentang tokoh dari Belanda yang disebut "Tuan Kabulhaden".</p>',
        'category_name': 'Berita Redaksi',
        'tags': ['sejarah', 'bandung', 'komunitas', 'milestone'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 25,
    },
    {
        'title': 'Sound of Heavy & CadasPersada: Dua Wajah Metal di Kabulhaden Online',
        'excerpt': 'PanjiOxen dan ArizMetalGodz bawa scene metal Bandung ke udara setiap Selasa.',
        'content': '<p>Komunitas metal Bandung sudah lama dikenal sebagai salah satu yang terkuat di Indonesia. Kabulhaden Online memberikan ruang bagi komunitas ini melalui Sound of Heavy (16.00\u201318.00 WIB) dan CadasPersada (18.00\u201319.00 WIB) setiap Selasa.</p><p>Keduanya dipandu PanjiOxen dan ArizMetalGodz. "Metal bukan genre, metal adalah gaya hidup. Kami di sini untuk menjaga api itu tetap menyala," kata PanjiOxen.</p>',
        'category_name': 'Musik',
        'tags': ['metal', 'rock', 'bandung', 'komunitas', 'underground'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 32,
    },
    {
        'title': 'Visi Kabulhaden Online: Episentrum Suara Kreatif Kota Bandung',
        'excerpt': 'Tiga misi yang memandu setiap program dan keputusan Kabulhaden Online.',
        'content': '<p>Visi Kabulhaden Online: "Terdapat episentrum suara dan energi kreatif yang menghubungkan, menginspirasi, serta menggerakkan berbagai komunitas lokal kota Bandung untuk lebih banyak lagi menghasilkan karya-karya kreatif."</p><p><strong>Misi 01</strong> \u2014 Katalisator Kolaborasi Komunitas: membangun jembatan antar-komunitas kreatif di Bandung (seni rupa, musik, literatur, desain, teknologi).<br><strong>Misi 02</strong> \u2014 Media edukasi, sosialisasi &amp; informasi dengan pemberdayaan karya industri kreatif.<br><strong>Misi 03</strong> \u2014 Pemanfaatan media integratif: audio konvensional PLUS digital interaktif (YouTube, Twitch, TikTok).</p>',
        'category_name': 'Berita Redaksi',
        'tags': ['visi', 'misi', 'komunitas', 'bandung', 'kreatif'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 40,
    },
    {
        'title': 'Kabulhaden Online Bergabung dengan Bandung Creative Hub sejak 2017',
        'excerpt': 'Kolaborasi dengan Dinas Pariwisata Kota Bandung membuka babak baru pertumbuhan komunitas.',
        'content': '<p>Salah satu momen paling pivotal dalam sejarah Kabulhaden Online terjadi pada 2017, ketika radio komunitas ini mendapat kesempatan bekerja sama dengan Dinas Pariwisata (Dispar) Kota Bandung melalui program Bandung Creative Hub (BCH).</p><p>Dalam program tersebut, Kabulhaden menjadi pelaksana kegiatan kreatif Kota Bandung untuk unit Penyiaran Radio. Ini membuka dukungan komunitas yang lebih luas: peralatan siaran, penyiar bertalenta dari komunitas musik, dan lahirnya program-program baru.</p>',
        'category_name': 'Komunitas',
        'tags': ['bandung-creative-hub', 'dispar', 'kolaborasi', 'bandung'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 50,
    },
    {
        'title': 'Tim Inti Kabulhaden Online: Ade Purnama, Leon, dan Mba Arien',
        'excerpt': 'Tiga orang di balik visi dan operasional platform multi-media Bandung ini.',
        'content': '<p><strong>Ade Purnama \u2014 CEO.</strong> Founder Kabulhaden Online, musisi Pure Saturday, host Flight \'92 setiap Selasa malam.</p><p><strong>Leon \u2014 CTO.</strong> Otak teknis Kabulhaden Online, co-host WarkopKabulhaden bersama Mba Arien.</p><p><strong>Mba Arien \u2014 General Manager.</strong> Wajah paling dikenal Kabulhaden Online, co-host WarkopKabulhaden, jantung operasional komunitas platform ini.</p>',
        'category_name': 'Profil',
        'tags': ['tim', 'profil', 'ceo', 'bandung', 'kabulhaden'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 60,
    },
    {
        'title': 'General Lifestyle vs Community Based: Dua Model Program Kabulhaden',
        'excerpt': 'Memahami dua jenis konten yang membentuk ekosistem siaran Kabulhaden Online.',
        'content': '<p><strong>General Lifestyle</strong> \u2014 kebanyakan program pada cloud dengan AutoDj pada program dengan tema kesamaan jenis musik. Contoh: IndIeDieu, Popmix 9020, Motown/Soul, JP City Pop. Berjalan otomatis dengan playlist terprogram.</p><p><strong>Community Based</strong> \u2014 inisiasi program dari komunitas dengan model siaran mandiri. Contoh: WarkopKabulhaden, Suburban Noise, Sound of Heavy, Flight \'92, Corner Table. Ini adalah jiwa Kabulhaden Online \u2014 otentik dan didorong oleh cinta komunitas.</p>',
        'category_name': 'Program',
        'tags': ['program', 'general-lifestyle', 'community-based', 'siaran'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 70,
    },
    {
        'title': 'SvArtSound: Portal Black Metal Skandinavia di Bandung',
        'excerpt': 'KokoRaven hadirkan Mayhem, Darkthrone, dan scene extreme metal global setiap Minggu malam.',
        'content': '<p>SvArtSound adalah program paling niche di Kabulhaden Online \u2014 dan justru itulah kekuatannya. Setiap Minggu pukul 19.00\u201321.00 WIB, KokoRaven membuka portal ke dunia Black Metal Skandinavia dan Extreme Metal global.</p><p>Mayhem, Burzum, Darkthrone, Emperor \u2014 nama-nama legendaris mengalun melalui udara Kabulhaden. "Black Metal adalah pengalaman total \u2014 filosofis, estetis, musikal," kata KokoRaven. SvArtSound adalah bukti bahwa Kabulhaden memberi ruang untuk semua genre.</p>',
        'category_name': 'Musik',
        'tags': ['black-metal', 'extreme-metal', 'skandinavia', 'underground'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 14,
    },
    {
        'title': 'Rumpies Daddies Podcast: Suara Kehidupan Kreatif Bandung',
        'excerpt': 'Podcast mingguan Kabulhaden Online tentang musik, komunitas, dan industri kreatif.',
        'content': '<p>Rumpies Daddies Podcast hadir setiap Senin malam pukul 20.00\u201322.00 WIB sebagai ruang refleksi dan obrolan mendalam tentang kehidupan kreatif Bandung. Setiap episode menghadirkan perspektif segar tentang musik, seni, dan industri budaya dari orang-orang yang benar-benar hidup di dalamnya.</p><p>Tidak ada naskah, tidak ada pertanyaan yang disiapkan \u2014 murni obrolan yang jujur dan mengalir. Program ini menjadi jembatan antara Kabulhaden Online dan ekosistem kreatif Bandung yang lebih luas.</p>',
        'category_name': 'Program',
        'tags': ['podcast', 'komunitas', 'bandung', 'kreatif'],
        'status': 'PUBLISHED',
        'featured': False,
        'days_ago': 5,
    },
]

ARTICLE_CATEGORIES = [
    'Berita Redaksi', 'Pengumuman', 'Komunitas', 'Gaya Hidup',
    'Musik', 'Program', 'Profil', 'Budaya & Seni',
    'Teknologi', 'Bisnis & Ekonomi',
]

PODCASTS = [
    {
        'title': 'Rumpies Daddies Podcast',
        'description': (
            'Podcast mingguan Kabulhaden Online tentang kehidupan, musik, komunitas kreatif, '
            'dan industri seni budaya Bandung. Format obrolan santai yang jujur dan mengalir '
            'tanpa naskah \u2014 murni perspektif dari pelaku kreatif langsung.'
        ),
        'short_description': 'Obrolan santai tentang kehidupan kreatif Bandung.',
        'category': 'NEWS',
        'episodes': [
            ('Membangun Komunitas Musik di Era Digital \u2014 Tantangan dan Peluang', 52),
            ('Pure Saturday dan Perjalanan Indie Indonesia: Obrolan dengan Ade Purnama', 68),
            ('Bandung Sebagai Ibu Kota Kreatif: Fakta atau Mitos?', 45),
            ('Dari Garage Band ke Radio: Cerita Musisi Bandung yang Jadi Penyiar', 58),
            ('Scene Underground Bandung 2026: Punk, Metal, Indie \u2014 Masih Hidup?', 63),
        ],
    },
    {
        'title': 'Corner Table Sessions',
        'description': (
            'Rekaman audio dari program live Corner Table \u2014 sesi musik live yang direkam '
            'langsung dari studio Kabulhaden Online. Setiap episode adalah pertunjukan '
            'intimate dari musisi-musisi pilihan komunitas Bandung.'
        ),
        'short_description': 'Live music sessions dari studio Kabulhaden Online.',
        'category': 'ENTERTAINMENT',
        'episodes': [
            ('Corner Table #12 \u2014 Trio Jazz Bandung: Malam yang Tak Terlupakan', 75),
            ('Corner Table #11 \u2014 Acoustic Folk Night dengan Komunitas Literasi', 68),
            ('Corner Table #10 \u2014 Experimental Sound Art dari Seniman Visual Bandung', 82),
            ('Corner Table #09 \u2014 Singer-Songwriter Showcase: Empat Suara Baru', 71),
        ],
    },
    {
        'title': 'Suara Komunitas Bandung',
        'description': (
            'Serial podcast dokumenter yang merekam suara-suara dari berbagai komunitas '
            'kreatif Kota Bandung. Dari komunitas musik, seni rupa, literatur, desain, '
            'hingga teknologi \u2014 semua punya cerita yang layak didengar.'
        ),
        'short_description': 'Dokumenter audio komunitas-komunitas kreatif Kota Bandung.',
        'category': 'NEWS',
        'episodes': [
            ('Komunitas Seni Rupa Bandung: Melukis Kota dengan Warna Sendiri', 55),
            ('Bandung Zine Fest: Kenapa Zine Masih Relevan di 2026?', 42),
            ('Komunitas Skateboard Bandung: Lebih dari Sekadar Olahraga', 38),
            ('Street Food Culture Bandung: UMKM Kuliner yang Bertahan', 47),
            ('Komunitas Game Developer Bandung: Startup Kecil, Mimpi Besar', 61),
            ('Sanggar Tari Kontemporer di Tengah Kota: Bergerak Melawan Arus', 50),
        ],
    },
]

SPONSORS = [
    {
        'name': 'Kantina Kultura Network',
        'partner_type': 'partner',
        'tier': 'platinum',
        'description': (
            'Mitra strategis utama Kabulhaden Online. Jaringan ruang kreatif Bandung yang '
            'bersama Kabulhaden mengaktifkan kembali program-program siaran komunitas di 2026.'
        ),
        'website': 'https://kabulhaden.online',
        'contact_email': 'host@kabulhaden.online',
    },
    {
        'name': 'Dinas Pariwisata Kota Bandung',
        'partner_type': 'partner',
        'tier': 'gold',
        'description': (
            'Mitra pemerintah Kabulhaden Online sejak 2017 melalui program Bandung Creative Hub (BCH). '
            'Mendukung Kabulhaden sebagai unit penyiaran radio dalam ekosistem kreatif kota.'
        ),
        'website': 'https://pariwisata.bandung.go.id',
        'contact_email': 'dispar@bandung.go.id',
    },
    {
        'name': 'Pure Saturday',
        'partner_type': 'partner',
        'tier': 'gold',
        'description': (
            'Band indie rock legendaris Bandung \u2014 akar dari Kabulhaden Online. '
            'Ade Purnama, frontman Pure Saturday, mendirikan Kabulhaden Online pada Agustus 2016.'
        ),
        'website': 'https://kabulhaden.online',
        'contact_email': 'host@kabulhaden.online',
    },
    {
        'name': 'Bandung Creative Hub',
        'partner_type': 'sponsor',
        'tier': 'silver',
        'description': (
            'Program ekosistem kreatif Kota Bandung yang menjadi inkubator perkembangan '
            'Kabulhaden Online sejak 2017.'
        ),
        'website': 'https://bandungcreativehub.id',
        'contact_email': 'info@bandungcreativehub.id',
    },
    {
        'name': 'Komunitas Musik Bandung',
        'partner_type': 'sponsor',
        'tier': 'silver',
        'description': (
            'Jaringan komunitas musik Bandung yang mengirimkan penyiar-penyiar bertalenta '
            'ke Kabulhaden Online \u2014 dari scene indie, punk, metal, hingga jazz.'
        ),
        'website': 'https://kabulhaden.online',
        'contact_email': 'host@kabulhaden.online',
    },
]

ADVERTISEMENTS = [
    {
        'title': 'Kabulhaden Online \u2014 Hear You Here!',
        'ad_type': 'banner',
        'link_url': 'https://kabulhaden.online',
        'impressions': 18500,
        'clicks': 920,
        'active': True,
    },
    {
        'title': 'WarkopKabulhaden Live di YouTube \u2014 Senin, Rabu, Jumat 15.00 WIB',
        'ad_type': 'banner',
        'link_url': 'https://youtube.com/@kabulhaden',
        'impressions': 12300,
        'clicks': 580,
        'active': True,
    },
    {
        'title': 'Suburban Noise \u2014 Punk & SKA Rabu 18.00 WIB',
        'ad_type': 'sidebar',
        'link_url': 'https://kabulhaden.online',
        'impressions': 7800,
        'clicks': 310,
        'active': True,
    },
    {
        'title': "Flight \'92 \u2014 Nostalgia 90s Selasa 20.00 WIB",
        'ad_type': 'banner',
        'link_url': 'https://kabulhaden.online',
        'impressions': 9500,
        'clicks': 445,
        'active': True,
    },
    {
        'title': 'Bandung Creative Hub \u2014 Ruang untuk Komunitas Kreatif',
        'ad_type': 'sidebar',
        'link_url': 'https://bandungcreativehub.id',
        'impressions': 5200,
        'clicks': 190,
        'active': True,
    },
]

# Songs from real genres played on Kabulhaden (indie, punk, 90s alt, metal, pop, motown)
SONGS_NOW_PLAYING = [
    # Indie Indonesia (Pure Saturday\\'s world)
    ('Tentang Seseorang', 'Pure Saturday'),
    ('Mesin Waktu', 'Pure Saturday'),
    ('Seperti Selalu', 'Mocca'),
    ('Di Udara', 'Efek Rumah Kaca'),
    # 90s Alt / Flight \\'92 era
    ('Common People', 'Pulp'),
    ('Fake Plastic Trees', 'Radiohead'),
    ('Wonderwall', 'Oasis'),
    ('Come As You Are', 'Nirvana'),
    # Punk / Suburban Noise
    ('Should I Stay or Should I Go', 'The Clash'),
    ('Anarchy in the UK', 'Sex Pistols'),
    # Metal / Sound of Heavy
    ('Black', 'Metallica'),
    ('War Pigs', 'Black Sabbath'),
    # Pop / Popmosphere & general
    ('Yang Terdalam', 'Project Pop'),
    ('Gajah', 'Tulus'),
    ('Kangen', 'Dewa 19'),
    # Motown / General Lifestyle
    ("Ain\\'t No Mountain High Enough", 'Marvin Gaye & Tammi Terrell'),
    ('What\\'s Going On', 'Marvin Gaye'),
    # SKA
    ('A Message to You Rudy', 'The Specials'),
    ('One Step Beyond', 'Madness'),
]
'''

# Replace from ARTICLES to end of SONGS_NOW_PLAYING block
pattern = r'(?s)ARTICLES = \[.*?SONGS_NOW_PLAYING = \[.*?\]\n'
new_text = re.sub(pattern, NEW_BLOCK, text)

if new_text == text:
    print("ERROR: pattern not found — no replacement made")
else:
    SRC.write_text(new_text)
    print("OK: replaced ARTICLES..SONGS_NOW_PLAYING")
    # verify
    updated = SRC.read_text()
    idx = updated.find("SONGS_NOW_PLAYING")
    print(f"SONGS_NOW_PLAYING found at char {idx}")
    idx2 = updated.find("Pure Saturday")
    print(f"Pure Saturday found at char {idx2}")
