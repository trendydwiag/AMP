"""
demo_seed — create a complete, realistic demo environment for Kabulhaden Online.

Usage:
    python manage.py demo_seed            # seed (idempotent)
    python manage.py demo_seed --reset    # wipe demo data then re-seed
    python manage.py demo_seed --quiet    # minimal output
"""

import random
from datetime import timedelta, time, date

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

# ── models ──────────────────────────────────────────────────────────────────
from apps.users.models import User, UserProfile
from apps.platform.models import Partner
from apps.broadcast.models import (
    Program, Episode, Schedule, Host, HostMember,
    BroadcastSession, Announcement,
)
from apps.news.models import Article, Category, Tag
from apps.podcast.models import Podcast, PodcastEpisode
from apps.sponsor.models import Partner as SponsorPartner, Advertisement
from apps.radio.models import (
    RadioStation, RadioProvider,
    NowPlayingCache, ListenerStatistic, StreamHealth, LiveSession,
)
from apps.content.models import Author
from apps.settings.models import (
    SiteSettings, AppearanceSettings, SocialMediaSettings,
    SEOSettings, NotificationSettings,
)
from apps.media_manager.models import MediaFile, Folder


# ── helpers ─────────────────────────────────────────────────────────────────
def ago(days=0, hours=0, minutes=0):
    return timezone.now() - timedelta(days=days, hours=hours, minutes=minutes)


def rand_date_in_last(days):
    return ago(days=random.randint(1, days))


def uslug(text, suffix=''):
    base = slugify(text)
    return f'{base}-{suffix}' if suffix else base


# ── content pools ────────────────────────────────────────────────────────────
# All program, host, and schedule data taken directly from the Kabulhaden Online
# pitch deck presented on 25 Juli 2026 by Ade Purnama (CEO).
PROGRAM_DATA = [
    # index 0
    {
        'title': 'Warung Kopi Kabulhaden',
        'category': 'talkshow',
        'short_description': 'Ngobrol yang berat-berat biar hidup terasa ringan — bersama Arien & Leon.',
        'full_description': (
            'WarkopKabulhaden adalah program bincang-bincang santai yang mengangkat topik-topik '
            'berat seputar kehidupan, seni, budaya, dan isu sosial dengan cara yang ringan dan '
            'penuh humor. Dipandu oleh Mba Arien (General Manager Kabulhaden Online) dan Leon '
            '(CTO), program ini menjadi ruang suara bagi komunitas kreatif Bandung. '
            'Juga ditayangkan secara live di YouTube Kabulhaden.'
        ),
        'genre': 'Talk Show / Community',
        'target_audience': 'Komunitas kreatif, usia 20–45',
        'featured': True,
    },
    # index 1
    {
        'title': 'Suburban Noise',
        'category': 'music',
        'short_description': 'Punk & SKA setiap Rabu bersama Aan & Buux Frederiksen.',
        'full_description': (
            'Suburban Noise adalah program musik live yang merayakan genre Punk dan SKA '
            'dengan energi mentah dan otentik. Dipandu oleh Aan dan Buux Frederiksen, dua '
            'tokoh scene punk Bandung, program ini menjadi rumah bagi para pencinta musik '
            'underground lokal dan internasional. Siaran langsung juga tersedia di TikTok '
            'Kabulhaden.'
        ),
        'genre': 'Punk / SKA',
        'target_audience': 'Komunitas punk, indie, underground',
        'featured': True,
    },
    # index 2
    {
        'title': 'Corner Table',
        'category': 'music',
        'short_description': 'Live set musical seminggu sekali bersama Ugenx & Gordo.',
        'full_description': (
            'Corner Table adalah program live musical performance yang menghadirkan musisi-musisi '
            'pilihan untuk tampil secara langsung di studio Kabulhaden Online. Dengan konsep '
            '"meja pojok" yang intim dan dekat, program ini merayakan keberagaman genre musik '
            'dari jazz, folk, indie, hingga eksperimental. Ditayangkan secara AudioVisual '
            'melalui YouTube dan Twitch.'
        ),
        'genre': 'Live Music / Various',
        'target_audience': 'Pecinta musik live, usia 18–40',
        'featured': True,
    },
    # index 3
    {
        'title': 'Popmosphere',
        'category': 'music',
        'short_description': 'Pop terbaik dari seluruh dunia setiap Sabtu bersama Imang & Anggicau.',
        'full_description': (
            'Popmosphere adalah program musik pop yang mengkurasi lagu-lagu pop terbaik dari '
            'Indonesia dan mancanegara. Dipandu Imang dan Anggicau dengan gaya yang fresh dan '
            'energik, program ini merayakan budaya pop kontemporer sambil tetap memberi ruang '
            'bagi artis-artis lokal Bandung untuk dikenal lebih luas.'
        ),
        'genre': 'Pop',
        'target_audience': 'Penggemar pop, usia 17–35',
        'featured': False,
    },
    # index 4
    {
        'title': 'Sound of Heavy',
        'category': 'music',
        'short_description': 'Metal dan hard rock setiap Selasa bersama PanjiOxen & ArizMetalGodz.',
        'full_description': (
            'Sound of Heavy adalah program yang mengangkat musik metal, hard rock, dan aliran '
            'berat lainnya yang hidup di bawah radar mainstream. PanjiOxen dan ArizMetalGodz '
            'adalah dua metalhead sejati yang membawa pendengar menyelami dunia musik extreme '
            'Indonesia dan internasional. Salah satu program Community Based terkuat di '
            'Kabulhaden Online.'
        ),
        'genre': 'Metal / Hard Rock',
        'target_audience': 'Komunitas metal dan hard rock',
        'featured': False,
    },
    # index 5
    {
        'title': 'CadasPersada',
        'category': 'music',
        'short_description': 'Indonesian Classic Rock at its best — bersama PanjiOxen & ArizMetalGodz.',
        'full_description': (
            'CadasPersada adalah program yang mendedikasikan satu jam setiap Selasa malam untuk '
            'merayakan warisan musik rock klasik Indonesia. Dari God Bless, Godbless, Gigi, '
            'hingga band-band rock Bandung legendaris, program ini menjaga agar flame of classic '
            'Indonesian rock tetap menyala.'
        ),
        'genre': 'Indonesian Classic Rock',
        'target_audience': 'Pecinta rock klasik Indonesia, usia 30+',
        'featured': False,
    },
    # index 6
    {
        'title': 'SvArtSound',
        'category': 'music',
        'short_description': 'Scandinavian & Extreme Metal setiap Minggu bersama KokoRaven.',
        'full_description': (
            'SvArtSound adalah program niche yang mengeksplorasi dunia Black Metal Skandinavia '
            'dan musik extreme global. Dipandu KokoRaven dengan pengetahuan mendalam tentang '
            'genre ini, program ini adalah surga bagi para penggemar Mayhem, Burzum, Darkthrone, '
            'dan scene extreme metal Indonesia.'
        ),
        'genre': 'Black Metal / Extreme Metal',
        'target_audience': 'Komunitas extreme metal',
        'featured': False,
    },
    # index 7
    {
        'title': "Flight '92",
        'category': 'music',
        'short_description': "Terbang ke era 90-an bersama AdeMuir & Anggicau setiap Selasa malam.",
        'full_description': (
            "Flight '92 adalah perjalanan nostalgia ke era musik 90-an yang penuh kenangan. "
            'AdeMuir (alias Ade Purnama, founder Kabulhaden Online) dan Anggicau membawa pendengar '
            'terbang kembali ke masa-masa Britpop, grunge, alternative rock, dan pop 90-an yang '
            'membentuk generasi. Program ini memadukan playlist cerdas dengan storytelling yang '
            'personal dan hangat.'
        ),
        'genre': "90s Music / Alternative",
        'target_audience': "Generasi 90-an, usia 28–45",
        'featured': True,
    },
    # index 8
    {
        'title': 'PoomPoom Radio',
        'category': 'music',
        'short_description': 'Lima jam musik non-stop setiap Kamis bersama PRTX, Opank & Nisu.',
        'full_description': (
            'PoomPoom Radio adalah program marathon musik yang mengudara selama lima jam penuh '
            'setiap Kamis siang. Dipandu tiga host yang energik — PRTX, Opank, dan Nisu — '
            'program ini memadukan musik dance, electronic, dan pop dengan interaksi aktif '
            'bersama pendengar via WhatsApp dan media sosial.'
        ),
        'genre': 'Dance / Electronic / Pop',
        'target_audience': 'Pendengar muda, usia 18–35',
        'featured': False,
    },
    # index 9
    {
        'title': 'After School Rawk',
        'category': 'music',
        'short_description': 'Rock dan alternative setiap Kamis sore bersama Ugenx & Gordo.',
        'full_description': (
            'After School Rawk hadir setiap Kamis sore sebagai pelepas penat setelah hari yang '
            'panjang. Ugenx dan Gordo mengkurasi playlist rock, alternative, dan indie terbaik '
            'sambil berinteraksi langsung dengan pendengar. Energi program ini selalu tinggi '
            'dan penuh semangat seperti anak muda yang baru pulang sekolah.'
        ),
        'genre': 'Rock / Alternative / Indie',
        'target_audience': 'Pencinta rock dan alternative, usia 17–35',
        'featured': False,
    },
    # index 10
    {
        'title': 'Kang Yan',
        'category': 'music',
        'short_description': 'Program musik mingguan dengan pilihan lagu terkurasi.',
        'full_description': (
            'Kang Yan adalah program musik mingguan yang menghadirkan kurasi lagu-lagu terpilih '
            'dari berbagai genre dan era. Program ini memiliki karakter yang kuat dan pendengar '
            'setia yang mengikuti setiap episodenya secara rutin setiap Senin dan Kamis.'
        ),
        'genre': 'Various / Curated',
        'target_audience': 'Umum',
        'featured': False,
    },
    # index 11
    {
        'title': 'Nada Siang',
        'category': 'music',
        'short_description': 'Teman makan siang dengan musik-musik pilihan setiap Senin & Kamis.',
        'full_description': (
            'Nada Siang adalah program musik siang yang menemani waktu istirahat makan siang '
            'pendengar Kabulhaden Online. Playlist yang diputar selalu ringan, mengalir, dan '
            'cocok sebagai teman beristirahat di tengah hari yang sibuk.'
        ),
        'genre': 'Easy Listening / Various',
        'target_audience': 'Umum, usia 20–50',
        'featured': False,
    },
    # index 12
    {
        'title': 'Rumpies Daddies Podcast',
        'category': 'talkshow',
        'short_description': 'Podcast mingguan tentang kehidupan, musik, dan dunia kreatif Bandung.',
        'full_description': (
            'Rumpies Daddies Podcast adalah program podcast mingguan yang mengangkat cerita-cerita '
            'dari komunitas kreatif Bandung. Dengan format obrolan santai namun substansial, '
            'setiap episode menghadirkan perspektif menarik tentang kehidupan, seni, musik, '
            'dan industri kreatif dari sudut pandang para pelakunya langsung.'
        ),
        'genre': 'Podcast / Talk',
        'target_audience': 'Komunitas kreatif dan profesional muda',
        'featured': False,
    },
    # index 13
    {
        'title': 'IndIeDieu',
        'category': 'music',
        'short_description': 'Indie Indonesia dan dunia — playlist otomatis setiap pagi hari kerja.',
        'full_description': (
            'IndIeDieu adalah program playlist otomatis (Playlist Run) yang memutar musik indie '
            'Indonesia dan internasional terbaik setiap pagi hari kerja. Tanpa host, murni musik '
            '— dipilih dengan cermat untuk menemani rutinitas pagi pendengar Kabulhaden Online. '
            'Program General Lifestyle yang paling banyak didengar secara pasif.'
        ),
        'genre': 'Indie / Alternative',
        'target_audience': 'Pekerja dan pelajar, usia 20–40',
        'featured': False,
    },
]

SCHEDULE_DATA = [
    # (program_index, day, start, end)
    # Source: Jadwal Program Harian Radio Kabulhaden (pitch deck p.7 + p.8)
    # 0 = WarkopKabulhaden
    (0, 'MON', '15:00', '17:00'),
    (0, 'WED', '15:00', '17:00'),
    (0, 'FRI', '15:00', '17:00'),
    (0, 'SAT', '15:00', '17:00'),  # Warkop Kabulhaden also Sat
    # 1 = Suburban Noise
    (1, 'WED', '18:00', '20:00'),
    # 2 = Corner Table
    (2, 'THU', '19:00', '21:00'),
    (2, 'SUN', '19:00', '21:00'),
    # 3 = Popmosphere
    (3, 'SAT', '13:00', '15:00'),
    # 4 = Sound of Heavy
    (4, 'TUE', '16:00', '18:00'),
    # 5 = CadasPersada
    (5, 'TUE', '18:00', '19:00'),
    # 6 = SvArtSound
    (6, 'SUN', '19:00', '21:00'),
    # 7 = Flight '92
    (7, 'TUE', '20:00', '22:00'),
    # 8 = PoomPoom Radio
    (8, 'THU', '13:00', '18:00'),
    (8, 'WED', '22:00', '23:00'),
    # 9 = After School Rawk
    (9, 'THU', '19:00', '21:00'),
    (9, 'FRI', '19:00', '21:00'),
    # 10 = Kang Yan
    (10, 'MON', '10:00', '12:00'),
    (10, 'THU', '10:00', '12:00'),
    # 11 = Nada Siang
    (11, 'MON', '13:00', '15:00'),
    (11, 'THU', '13:00', '15:00'),
    # 12 = Rumpies Daddies Podcast
    (12, 'MON', '20:00', '22:00'),
    # 13 = IndIeDieu (playlist run, Mon–Fri 09:00–10:00)
    (13, 'MON', '09:00', '10:00'),
    (13, 'TUE', '09:00', '10:00'),
    (13, 'WED', '09:00', '10:00'),
    (13, 'THU', '09:00', '10:00'),
    (13, 'FRI', '09:00', '10:00'),
]

HOST_DATA = [
    # Real hosts from Kabulhaden Online pitch deck (p.8, p.9)
    {
        'full_name': 'Arien',
        'stage_name': 'Mba Arien',
        'nickname': 'Arien',
        'biography': (
            'General Manager Kabulhaden Online dan co-host WarkopKabulhaden. '
            'Salah satu wajah paling dikenal di Kabulhaden Online, Mba Arien memadukan '
            'kepemimpinan organisasi dengan kehadiran on-air yang hangat dan dekat dengan komunitas.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'Leon',
        'stage_name': 'Leon',
        'nickname': 'Leon',
        'biography': (
            'CTO Kabulhaden Online sekaligus co-host WarkopKabulhaden. '
            'Leon bertanggung jawab atas seluruh infrastruktur teknis platform streaming '
            'Kabulhaden Online, sambil tetap aktif di depan mikrofon bersama Mba Arien.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'Aan Frederiksen',
        'stage_name': 'Aan',
        'nickname': 'Aan',
        'biography': (
            'Host Suburban Noise dan tokoh scene punk Bandung. '
            'Aan adalah salah satu wajah terkuat komunitas punk dan SKA di Kota Bandung, '
            'membawa energi dan pengetahuan mendalam tentang musik underground ke udara Kabulhaden.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'Buux Frederiksen',
        'stage_name': 'Buux',
        'nickname': 'Buux',
        'biography': (
            'Co-host Suburban Noise dan musisi punk aktif di Bandung. '
            'Bersama Aan, Buux membentuk duo yang menjadikan Suburban Noise salah satu '
            'program paling ditunggu pendengar metal dan punk Kabulhaden Online.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'PanjiOxen',
        'stage_name': 'PanjiOxen',
        'nickname': 'Panji',
        'biography': (
            'Host Sound of Heavy dan CadasPersada, metalhead sejati dari Bandung. '
            'PanjiOxen adalah jangkar komunitas metal Bandung di Kabulhaden Online, '
            'menghadirkan wawasan mendalam tentang musik berat Indonesia dan dunia.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'KokoRaven',
        'stage_name': 'KokoRaven',
        'nickname': 'Koko',
        'biography': (
            'Host SvArtSound dan pakar Black Metal & Extreme Metal di Kabulhaden Online. '
            'KokoRaven membawa pendengar ke dunia musik extreme Skandinavia dan global '
            'setiap Minggu malam dengan kedalaman kuratorinya yang tak tertandingi.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'Ugenx',
        'stage_name': 'Ugenx',
        'nickname': 'Ugenx',
        'biography': (
            'Co-host Corner Table dan After School Rawk di Kabulhaden Online. '
            'Ugenx adalah salah satu musisi dan presenter paling serbaguna di Kabulhaden, '
            'nyaman di berbagai genre dari live music hingga rock alternative.'
        ),
        'instagram': '@kabulhaden',
    },
    {
        'full_name': 'AdeMuir',
        'stage_name': 'AdeMuir',
        'nickname': 'Ade Muir',
        'biography': (
            "Host Flight '92 dan founder Kabulhaden Online. "
            "Ade Purnama alias Ade Muir adalah musisi band Pure Saturday yang mendirikan "
            "Kabulhaden Online pada Agustus 2016 di Jalan Multatuli No. 5 Bandung. "
            "Sebagai CEO, ia menjaga visi platform sambil tetap aktif on-air setiap Selasa."
        ),
        'instagram': '@kabulhaden',
    },
]

ARTICLES = [
    {
        'title': 'Kabulhaden Online Kembali Mengudara: Transformasi Menuju Platform Multi-Media 2026',
        'excerpt': 'Setelah rebranding awal 2026, Kabulhaden Online hadir lebih kuat dengan 14 program aktif.',
        'content': (
            '<p>Awal tahun 2026 menjadi tonggak penting bagi Kabulhaden Online. '
            'Setelah sempat berganti-ganti nama dan lokasi studio, radio komunitas Bandung ini '
            'bertransformasi penuh menjadi Kabulhaden Online — sebuah platform multi-media '
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
            '<p>WarkopKabulhaden mengambil nama dari konsep warung kopi — tempat di mana '
            'obrolan berat tentang kehidupan, seni, dan budaya mengalir dengan ringan. Dipandu '
            'oleh Mba Arien (General Manager) dan Leon (CTO), program ini hadir setiap Senin, '
            'Rabu, dan Jumat pukul 15.00–17.00 WIB, juga Sabtu.</p>'
            '<p>Konsep kami sederhana: ngobrol yang berat-berat, biar hidup terasa ringan. '
            'Program ini adalah Community Based — inisiatif langsung dari komunitas, '
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
            '<p>Setiap Rabu pukul 18.00–20.00 WIB, Kabulhaden Online berguncang dengan '
            'energi punk dan SKA dari Suburban Noise. Dipandu Aan dan Buux Frederiksen — '
            'dua nama besar di scene underground Bandung — program ini adalah rumah bagi '
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
            "<p>Flight '92 tayang setiap Selasa pukul 20.00–22.00 WIB, dipandu langsung "
            'oleh Ade Purnama alias AdeMuir — founder sekaligus CEO Kabulhaden Online, '
            'musisi dari band Pure Saturday.</p>'
            '<p>Tahun 90-an adalah dekade di mana musik benar-benar berbicara. Britpop, '
            'grunge, alternative — semua punya kedalaman yang tak lekang oleh waktu. '
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
        'excerpt': 'Dari server radio cast gratisan di 2016 ke platform multi-media 2026 — perjalanan satu dekade.',
        'content': (
            '<p>Agustus 2016. Dari sebuah ruangan di Jalan Multatuli No. 5, Kota Bandung, '
            'Ade Purnama alias Ade Muir — musisi dari band Pure Saturday — mulai '
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
            'Heavy (16.00–18.00 WIB) dan CadasPersada (18.00–19.00 WIB) setiap Selasa.</p>'
            '<p>Sound of Heavy mengangkat metal, hard rock, dan aliran berat lainnya. '
            'CadasPersada merayakan warisan rock klasik Indonesia. Keduanya dipandu PanjiOxen '
            'dan ArizMetalGodz. Metal bukan genre, metal adalah gaya hidup — kami di sini '
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
            '<p><strong>Misi 01</strong> — Katalisator Kolaborasi Komunitas: membangun '
            'jembatan antar-komunitas kreatif di Bandung (seni rupa, musik, literatur, desain, '
            'teknologi).<br>'
            '<strong>Misi 02</strong> — Media edukasi, sosialisasi dan informasi dengan '
            'pemberdayaan karya industri kreatif.<br>'
            '<strong>Misi 03</strong> — Pemanfaatan media integratif: audio konvensional '
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
            '<p><strong>Ade Purnama — CEO.</strong> Founder Kabulhaden Online. Musisi '
            "dari band Pure Saturday yang memulai Kabulhaden Online pada Agustus 2016. Host "
            "Flight '92 setiap Selasa malam.</p>"
            '<p><strong>Leon — CTO.</strong> Otak teknis Kabulhaden Online, memastikan '
            'stream tetap hidup dan server berjalan. Co-host WarkopKabulhaden bersama Mba Arien.</p>'
            '<p><strong>Mba Arien — General Manager.</strong> Wajah paling dikenal '
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
            '<p><strong>General Lifestyle</strong> — program pada cloud dengan AutoDj '
            'pada tema kesamaan jenis musik. Contoh: IndIeDieu, Popmix 9020, Motown/Soul, '
            'JP City Pop. Berjalan otomatis dengan playlist terprogram.</p>'
            '<p><strong>Community Based</strong> — inisiasi program dari komunitas '
            'dengan model siaran mandiri. Contoh: WarkopKabulhaden, Suburban Noise, Sound of '
            "Heavy, Flight '92, Corner Table. Ini adalah jiwa Kabulhaden Online — "
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
            '<p>SvArtSound adalah program paling niche di Kabulhaden Online — dan justru '
            'itulah kekuatannya. Setiap Minggu pukul 19.00–21.00 WIB, KokoRaven membuka '
            'portal ke dunia Black Metal Skandinavia dan Extreme Metal global.</p>'
            '<p>Mayhem, Burzum, Darkthrone, Emperor — nama-nama legendaris mengalun '
            'melalui udara Kabulhaden. Black Metal adalah pengalaman total — filosofis, '
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
            '<p>Rumpies Daddies Podcast hadir setiap Senin malam pukul 20.00–22.00 WIB '
            'sebagai ruang obrolan mendalam tentang kehidupan kreatif Bandung. Setiap episode '
            'menghadirkan perspektif segar tentang musik, seni, dan industri budaya dari '
            'orang-orang yang benar-benar hidup di dalamnya.</p>'
            '<p>Tidak ada naskah, tidak ada pertanyaan yang disiapkan — murni obrolan '
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
            'tanpa naskah — murni perspektif dari pelaku kreatif langsung.'
        ),
        'short_description': 'Obrolan santai tentang kehidupan kreatif Bandung.',
        'category': 'NEWS',
        'episodes': [
            ('Membangun Komunitas Musik di Era Digital — Tantangan dan Peluang', 52),
            ('Pure Saturday dan Perjalanan Indie Indonesia: Obrolan dengan Ade Purnama', 68),
            ('Bandung Sebagai Ibu Kota Kreatif: Fakta atau Mitos?', 45),
            ('Dari Garage Band ke Radio: Cerita Musisi Bandung yang Jadi Penyiar', 58),
            ('Scene Underground Bandung 2026: Punk, Metal, Indie — Masih Hidup?', 63),
        ],
    },
    {
        'title': 'Corner Table Sessions',
        'description': (
            'Rekaman audio dari program live Corner Table — sesi musik live yang direkam '
            'langsung dari studio Kabulhaden Online. Setiap episode adalah pertunjukan '
            'intimate dari musisi-musisi pilihan komunitas Bandung.'
        ),
        'short_description': 'Live music sessions dari studio Kabulhaden Online.',
        'category': 'ENTERTAINMENT',
        'episodes': [
            ('Corner Table #12 — Trio Jazz Bandung: Malam yang Tak Terlupakan', 75),
            ('Corner Table #11 — Acoustic Folk Night dengan Komunitas Literasi', 68),
            ('Corner Table #10 — Experimental Sound Art dari Seniman Visual Bandung', 82),
            ('Corner Table #09 — Singer-Songwriter Showcase: Empat Suara Baru', 71),
        ],
    },
    {
        'title': 'Suara Komunitas Bandung',
        'description': (
            'Serial podcast dokumenter yang merekam suara-suara dari berbagai komunitas '
            'kreatif Kota Bandung. Dari komunitas musik, seni rupa, literatur, desain, '
            'hingga teknologi — semua punya cerita yang layak didengar.'
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
            'Band indie rock legendaris Bandung — akar dari Kabulhaden Online. '
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
            'ke Kabulhaden Online — dari scene indie, punk, metal, hingga jazz.'
        ),
        'website': 'https://kabulhaden.online',
        'contact_email': 'host@kabulhaden.online',
    },
]

ADVERTISEMENTS = [
    {
        'title': 'Kabulhaden Online — Hear You Here!',
        'ad_type': 'banner',
        'link_url': 'https://kabulhaden.online',
        'impressions': 18500,
        'clicks': 920,
        'active': True,
    },
    {
        'title': 'WarkopKabulhaden Live di YouTube — Senin, Rabu, Jumat 15.00 WIB',
        'ad_type': 'banner',
        'link_url': 'https://youtube.com/@kabulhaden',
        'impressions': 12300,
        'clicks': 580,
        'active': True,
    },
    {
        'title': 'Suburban Noise — Punk & SKA Rabu 18.00 WIB',
        'ad_type': 'sidebar',
        'link_url': 'https://kabulhaden.online',
        'impressions': 7800,
        'clicks': 310,
        'active': True,
    },
    {
        'title': "Flight '92 — Nostalgia 90s Selasa 20.00 WIB",
        'ad_type': 'banner',
        'link_url': 'https://kabulhaden.online',
        'impressions': 9500,
        'clicks': 445,
        'active': True,
    },
    {
        'title': 'Bandung Creative Hub — Ruang untuk Komunitas Kreatif',
        'ad_type': 'sidebar',
        'link_url': 'https://bandungcreativehub.id',
        'impressions': 5200,
        'clicks': 190,
        'active': True,
    },
]

# Songs from real genres played on Kabulhaden (indie, punk, 90s alt, metal, pop, motown)
SONGS_NOW_PLAYING = [
    # Indie Indonesia (Pure Saturday\'s world)
    ('Tentang Seseorang', 'Pure Saturday'),
    ('Mesin Waktu', 'Pure Saturday'),
    ('Seperti Selalu', 'Mocca'),
    ('Di Udara', 'Efek Rumah Kaca'),
    # 90s Alt / Flight \'92 era
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
    ("Ain\'t No Mountain High Enough", 'Marvin Gaye & Tammi Terrell'),
    ('What\'s Going On', 'Marvin Gaye'),
    # SKA
    ('A Message to You Rudy', 'The Specials'),
    ('One Step Beyond', 'Madness'),
]

NOW = timezone.now()


class Command(BaseCommand):
    help = 'Seed realistic demo data for Kabulhaden Online'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing demo data before seeding',
        )
        parser.add_argument(
            '--quiet',
            action='store_true',
            help='Suppress verbose output',
        )

    def log(self, msg, style=None):
        if not self._quiet:
            if style:
                self.stdout.write(style(msg))
            else:
                self.stdout.write(msg)

    def ok(self, msg):
        self.log(f'  ✓ {msg}', self.style.SUCCESS)

    def section(self, msg):
        self.log(f'\n── {msg} ──', self.style.MIGRATE_HEADING)

    def handle(self, *args, **options):
        self._quiet = options.get('quiet', False)
        self._reset = options.get('reset', False)

        self.log('\n🎙  Kabulhaden Online — Demo Seed', self.style.MIGRATE_HEADING)
        self.log('=' * 45)

        if self._reset:
            self._reset_demo_data()

        self._seed_partner()
        self._seed_users()
        self._seed_settings()
        self._seed_radio()
        self._seed_media_folders()
        self._seed_authors_hosts()
        self._seed_programs_schedules()
        self._seed_categories_tags()
        self._seed_articles()
        self._seed_podcasts()
        self._seed_sponsors()
        self._seed_analytics()
        self._seed_announcements()
        self._seed_audit_logs()

        self.log('\n' + '=' * 45)
        self.log('🎉  Demo seed complete!', self.style.SUCCESS)
        self.log('\nLogin credentials:')
        self.log('  superadmin / DemoAdmin2024!  (Super User)')
        self.log('  admin      / DemoAdmin2024!  (Administrator)')
        self.log('  editor     / DemoEditor2024! (Editor)')
        self.log('  viewer     / DemoViewer2024! (Viewer)')

    # ── reset ────────────────────────────────────────────────────────────────
    def _reset_demo_data(self):
        self.section('Resetting demo data')
        # Detach protected FK references before deleting users
        Partner.objects.filter(
            owner__username__in=['superadmin', 'editor', 'viewer']
        ).update(owner=None)

        ListenerStatistic.objects.all().delete()
        StreamHealth.objects.all().delete()
        NowPlayingCache.objects.all().delete()
        LiveSession.objects.all().delete()
        PodcastEpisode.objects.all().delete()
        Podcast.objects.all().delete()
        Episode.objects.all().delete()
        Schedule.objects.all().delete()
        BroadcastSession.objects.all().delete()
        HostMember.objects.all().delete()
        Program.objects.all().delete()
        Host.objects.all().delete()
        Article.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Advertisement.objects.all().delete()
        SponsorPartner.objects.all().delete()
        RadioProvider.objects.all().delete()
        RadioStation.objects.all().delete()
        Author.objects.all().delete()
        Folder.objects.all().delete()
        Announcement.objects.all().delete()
        User.objects.filter(username__in=['superadmin', 'editor', 'viewer']).delete()
        self.ok('Demo data cleared')

    # ── partner ──────────────────────────────────────────────────────────────
    def _seed_partner(self):
        self.section('Partner')
        partner, created = Partner.objects.get_or_create(
            slug='kabulhaden-online',
            defaults={
                'name': 'Kabulhaden Online',
                'company_name': 'PT Kabulhaden Media Digital',
                'status': 'ACTIVE',
                'tier': 'ENTERPRISE',
                'primary_color': '#8B5E3C',
                'secondary_color': '#D4A574',
                'accent_color': '#F5DEB3',
                'tagline': 'Suara Kabulhaden, Hati Nusantara',
                'description': (
                    'Kabulhaden Online adalah platform radio digital komunitas yang melayani '
                    'masyarakat Kabulhaden dengan konten berkualitas sejak 2012. '
                    'Kami berkomitmen menjadi jembatan antara informasi, budaya, dan komunitas.'
                ),
                'contact_email': 'info@kabulhaden.online',
                'contact_phone': '+62-812-3456-7890',
                'contact_website': 'https://kabulhaden.online',
                'resolution_method': 'DOMAIN',
                'primary_domain': 'kabulhaden.online',
                'max_users': 50,
                'max_storage_mb': 51200,
                'max_articles': 10000,
                'max_podcasts': 500,
                'max_episodes': 5000,
                'timezone': 'Asia/Jakarta',
                'language': 'id',
                'locale': 'id_ID',
            }
        )
        self._partner = partner
        action = 'Created' if created else 'Found'
        self.ok(f'{action} partner: {partner.name}')

    # ── users ─────────────────────────────────────────────────────────────────
    def _seed_users(self):
        self.section('Users')
        users_spec = [
            {
                # Real CEO: Ade Purnama alias AdeMuir, founder of Kabulhaden Online (pitch deck p.9)
                'username': 'superadmin',
                'email': 'host@kabulhaden.online',
                'first_name': 'Ade',
                'last_name': 'Purnama',
                'role': 'SUPERUSER',
                'password': 'DemoAdmin2024!',
                'is_staff': True,
                'is_superuser': True,
                'bio': (
                    'CEO & Founder Kabulhaden Online. Musisi dari band Pure Saturday yang memulai '
                    'Kabulhaden Online pada Agustus 2016 di Jalan Multatuli No. 5, Bandung. '
                    'Host Flight \'92 setiap Selasa malam.'
                ),
                'phone': '+62-812-0001-0001',
            },
            {
                # Real CTO: Leon (pitch deck p.9) — also co-host of WarkopKabulhaden
                'username': 'admin',
                'email': 'admin@kabulhaden.online',
                'first_name': 'Admin',
                'last_name': 'Kabulhaden',
                'role': 'ADMINISTRATOR',
                'password': 'DemoAdmin2024!',
                'is_staff': True,
                'is_superuser': True,
                'bio': 'Administrator sistem Kabulhaden Online.',
                'phone': '+62-812-0001-0002',
            },
            {
                # Real GM: Mba Arien (pitch deck p.9) — also co-host of WarkopKabulhaden
                'username': 'editor',
                'email': 'editor@kabulhaden.online',
                'first_name': 'Arien',
                'last_name': '',
                'role': 'EDITOR',
                'password': 'DemoEditor2024!',
                'is_staff': False,
                'is_superuser': False,
                'bio': (
                    'General Manager Kabulhaden Online dan co-host WarkopKabulhaden. '
                    'Wajah paling dikenal di Kabulhaden Online, memadukan kepemimpinan '
                    'organisasi dengan kehadiran on-air yang hangat.'
                ),
                'phone': '+62-812-0001-0003',
            },
            {
                'username': 'viewer',
                'email': 'viewer@kabulhaden.online',
                'first_name': 'Leon',
                'last_name': '',
                'role': 'VIEWER',
                'password': 'DemoViewer2024!',
                'is_staff': False,
                'is_superuser': False,
                'bio': (
                    'CTO Kabulhaden Online dan co-host WarkopKabulhaden. '
                    'Bertanggung jawab atas seluruh infrastruktur teknis platform streaming.'
                ),
                'phone': '+62-812-0001-0004',
            },
        ]

        self._users = {}
        for spec in users_spec:
            user, created = User.objects.get_or_create(
                username=spec['username'],
                defaults={
                    'email': spec['email'],
                    'first_name': spec['first_name'],
                    'last_name': spec['last_name'],
                    'role': spec['role'],
                    'is_staff': spec['is_staff'],
                    'is_superuser': spec['is_superuser'],
                    'is_active': True,
                }
            )
            if created:
                user.set_password(spec['password'])
                user.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': spec['bio'],
                    'phone': spec['phone'],
                }
            )
            self._users[spec['username']] = user
            action = 'Created' if created else 'Found'
            full_name = f"{user.first_name} {user.last_name}".strip() or user.username
            self.ok(f'{action} user: {full_name} ({spec["role"]})')

        # link partner owner
        if not self._partner.owner:
            self._partner.owner = self._users.get('superadmin')
            self._partner.save()

    # ── settings ──────────────────────────────────────────────────────────────
    def _seed_settings(self):
        self.section('Settings')
        site, _ = SiteSettings.objects.get_or_create(pk=1, defaults={})
        site.site_name = 'Kabulhaden Online'
        site.site_tagline = 'Hear You Here!!!'
        site.site_description = (
            'Platform multi-media siar digital berbasis teknologi internet yang memfasilitasi '
            'beragam inisiasi kegiatan penyiaran dari komunitas-komunitas kreatif yang tersebar '
            'di Kota Bandung dan sekitarnya, khususnya para praktisi seni dan budaya.'
        )
        site.site_url = 'https://kabulhaden.online'
        site.maintenance_mode = False
        site.save()
        self.ok('SiteSettings updated')

        social, _ = SocialMediaSettings.objects.get_or_create(pk=1, defaults={})
        # Real social media from pitch deck contact page
        social.facebook_url = 'https://facebook.com/kabulhaden'
        social.twitter_url = 'https://twitter.com/kabulhaden'
        social.instagram_url = 'https://instagram.com/kabulhaden'
        social.youtube_url = 'https://youtube.com/@kabulhaden'
        social.tiktok_url = 'https://tiktok.com/@kabulhaden'
        social.whatsapp_number = '+628123456789'
        social.telegram_username = 'kabulhadenonline'
        social.save()
        self.ok('SocialMediaSettings updated')

        appearance, _ = AppearanceSettings.objects.get_or_create(pk=1, defaults={})
        appearance.primary_color = '#8B5E3C'
        appearance.secondary_color = '#D4A574'
        appearance.accent_color = '#F5DEB3'
        appearance.dark_mode = False
        appearance.show_welcome_message = True
        appearance.save()
        self.ok('AppearanceSettings updated')

    # ── radio station ─────────────────────────────────────────────────────────
    def _seed_radio(self):
        self.section('Radio Station & Streaming')
        admin_user = self._users.get('admin')

        station = RadioStation.objects.filter(partner=self._partner).first()
        if not station:
            station = RadioStation.objects.create(
                station_name='Kabulhaden Online',
                station_description=(
                    'Stasiun radio digital komunitas Kabulhaden yang mengudara sejak 2012. '
                    'Menjangkau lebih dari 50.000 pendengar aktif setiap bulannya.'
                ),
                partner=self._partner,
                is_active=True,
                timezone='Asia/Jakarta',
                country='ID',
                language='id',
                genre='Variety',
                website='https://kabulhaden.online',
                default_volume=80,
                autoplay=True,
                sticky_player=True,
            )
            created = True
        else:
            station.is_active = True
            station.partner = self._partner
            station.save()
            created = False
        self._station = station
        action = 'Created' if created else 'Found/Updated'
        self.ok(f'{action} radio station: {self._station.station_name}')

        # Provider
        provider, pcreated = RadioProvider.objects.get_or_create(
            station=self._station,
            defaults={
                'provider_name': 'AzuraCast Primary',
                'provider_type': 'AZURACAST',
                'stream_url': 'https://stream.kabulhaden.online:8000/radio.mp3',
                'backup_stream_url': 'https://backup.kabulhaden.online:8000/radio.mp3',
                'api_url': 'https://stream.kabulhaden.online/api',
                'active': True,
                'timeout': 10,
            }
        )
        if not pcreated:
            provider.provider_type = 'AZURACAST'
            provider.stream_url = 'https://stream.kabulhaden.online:8000/radio.mp3'
            provider.active = True
            provider.save()
        self._provider = provider
        self.ok(f'Provider: {provider.provider_type} — {provider.stream_url}')

        # NowPlayingCache
        song, artist = random.choice(SONGS_NOW_PLAYING)
        NowPlayingCache.objects.filter(station=self._station).delete()
        NowPlayingCache.objects.create(
            station=self._station,
            provider=self._provider,
            song_title=song,
            artist=artist,
            album='Hits Indonesia',
            stream_status='ONLINE',
            duration=240,
            elapsed=73,
            started_at=ago(minutes=2),
        )
        self.ok(f'NowPlaying: {song} — {artist}')

        # StreamHealth (healthy)
        StreamHealth.objects.filter(station=self._station).delete()
        StreamHealth.objects.create(
            station=self._station,
            provider=self._provider,
            provider_status='HEALTHY',
            http_status=200,
            response_time=42,
            stream_bitrate=128,
            stream_format='MP3',
            last_checked=ago(minutes=1),
        )
        # Generate 30 days of health history
        for d in range(1, 31):
            status = random.choices(
                ['HEALTHY', 'HEALTHY', 'HEALTHY', 'DEGRADED', 'DOWN'],
                weights=[70, 70, 70, 15, 5]
            )[0]
            StreamHealth.objects.create(
                station=self._station,
                provider=self._provider,
                provider_status=status,
                http_status=200 if status != 'DOWN' else 503,
                response_time=random.randint(20, 200),
                stream_bitrate=128,
                stream_format='MP3',
                last_checked=ago(days=d, hours=random.randint(0, 23)),
            )
        self.ok('StreamHealth: HEALTHY (+ 30-day history)')

        # ListenerStatistic
        ListenerStatistic.objects.filter(station=self._station).delete()
        # Current
        ListenerStatistic.objects.create(
            station=self._station,
            current_listeners=127,
            peak_listeners=312,
            recorded_at=ago(minutes=1),
        )
        # Last 90 days
        for d in range(1, 91):
            dt = ago(days=d)
            ListenerStatistic.objects.create(
                station=self._station,
                current_listeners=random.randint(45, 280),
                peak_listeners=random.randint(150, 450),
                recorded_at=dt,
            )
        self.ok('ListenerStatistic: 127 current + 90-day history')

        # LiveSession
        LiveSession.objects.filter(station=self._station).delete()
        LiveSession.objects.create(
            station=self._station,
            program='Pagi Bersama Kabulhaden',
            host='Dewi R',
            started_at=ago(hours=1),
            listener_peak=312,
            average_listeners=187,
        )
        self.ok('LiveSession: Pagi Bersama Kabulhaden (active)')

    # ── media folders ─────────────────────────────────────────────────────────
    def _seed_media_folders(self):
        self.section('Media Folders')
        folders = [
            'Program Thumbnails', 'Artikel Berita', 'Foto Penyiar',
            'Sponsor & Iklan', 'Podcast Cover', 'Dokumen Internal',
        ]
        self._folders = {}
        for name in folders:
            f, _ = Folder.objects.get_or_create(
                name=name,
                partner=self._partner,
                defaults={'parent': None}
            )
            self._folders[name] = f
        self.ok(f'Created {len(folders)} media folders')

    # ── authors & hosts ───────────────────────────────────────────────────────
    def _seed_authors_hosts(self):
        self.section('Authors & Hosts')
        self._authors = {}
        self._hosts = {}

        author_specs = [
            ('Dewi Rahayu Putri', 'dewi-rahayu', 'dewi-rahayu@kabulhaden.online',
             'Penyiar senior dan jurnalis radio Kabulhaden Online.'),
            ('Rizky Firmansyah', 'rizky-firmansyah', 'rizky.fm@kabulhaden.online',
             'Penyiar musik dan host program pemuda.'),
            ('Siti Andini', 'siti-andini', 'siti.andini@kabulhaden.online',
             'Jurnalis dan host program berita.'),
            ('Ahmad Fauzi', 'ahmad-fauzi', 'ahmad.fauzi@kabulhaden.online',
             'Host program bisnis dan konsultan UMKM.'),
            ('Tim Redaksi', 'tim-redaksi', 'redaksi@kabulhaden.online',
             'Tim editorial Kabulhaden Online.'),
        ]
        for name, slug, email, bio in author_specs:
            a, _ = Author.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'email': email, 'bio': bio, 'active': True}
            )
            self._authors[slug] = a

        for spec in HOST_DATA:
            h, _ = Host.objects.get_or_create(
                email=f"{slugify(spec['full_name'])}@kabulhaden.online",
                defaults={
                    'full_name': spec['full_name'],
                    'stage_name': spec['stage_name'],
                    'nickname': spec['nickname'],
                    'biography': spec['biography'],
                    'instagram': spec['instagram'],
                    'active': True,
                }
            )
            self._hosts[spec['stage_name']] = h
        self.ok(f'Created {len(author_specs)} authors, {len(HOST_DATA)} hosts')

    # ── programs & schedules ──────────────────────────────────────────────────
    def _seed_programs_schedules(self):
        self.section('Programs, Episodes & Schedules')
        admin_user = self._users.get('admin')
        author = list(self._authors.values())[0]
        self._programs = []

        for idx, pdata in enumerate(PROGRAM_DATA):
            prog, _ = Program.objects.get_or_create(
                slug=uslug(pdata['title']),
                defaults={
                    'title': pdata['title'],
                    'short_description': pdata['short_description'],
                    'full_description': pdata['full_description'],
                    'category': pdata['category'],
                    'genre': pdata['genre'],
                    'target_audience': pdata['target_audience'],
                    'featured': pdata['featured'],
                    'active': True,
                    'status': 'APPROVED',
                    'content_rating': 'G',
                    'priority': 'NORMAL',
                    'content_format': 'RICH_TEXT',
                    'partner': self._partner,
                    'author': author,
                    'language': 'id',
                    'version': 1,
                }
            )
            self._programs.append(prog)

            # Assign hosts
            hosts = list(self._hosts.values())
            h = hosts[idx % len(hosts)]
            HostMember.objects.get_or_create(
                host=h, program=prog,
                defaults={'is_lead': True, 'joined_date': date(2023, 1, 1)}
            )

            # Create 5 episodes per program
            for ep_num in range(1, 6):
                ep_title = f'Episode {ep_num}: {prog.title} — Edisi Terbaru'
                ep, _ = Episode.objects.get_or_create(
                    program=prog,
                    episode_number=ep_num,
                    defaults={
                        'title': ep_title,
                        'description': (
                            f'Episode {ep_num} dari program {prog.title}. '
                            f'{prog.short_description} Menghadirkan konten segar '
                            f'dan informatif untuk pendengar setia kami.'
                        ),
                        'published': True,
                        'publish_date': ago(days=(ep_num * 7)),
                        'status': 'APPROVED',
                        'content_format': 'RICH_TEXT',
                        'partner': self._partner,
                        'version': 1,
                        'featured': ep_num == 1,
                    }
                )

        self.ok(f'Created {len(PROGRAM_DATA)} programs with 5 episodes each')

        # Schedules
        sched_count = 0
        for prog_idx, day, start_str, end_str in SCHEDULE_DATA:
            prog = self._programs[prog_idx]
            sh, sm = map(int, start_str.split(':'))
            eh, em = map(int, end_str.split(':'))
            Schedule.objects.get_or_create(
                program=prog,
                day_of_week=day,
                start_time=time(sh, sm),
                defaults={
                    'end_time': time(eh, em),
                    'active': True,
                }
            )
            sched_count += 1
        self.ok(f'Created {sched_count} schedule slots')

        # BroadcastSessions (last 30 days)
        for d in range(0, 30):
            prog = random.choice(self._programs[:4])
            BroadcastSession.objects.get_or_create(
                program=prog,
                start_datetime=ago(days=d, hours=random.randint(6, 20)),
                defaults={
                    'end_datetime': ago(days=d, hours=random.randint(6, 20)) + timedelta(hours=2),
                    'status': 'FINISHED',
                }
            )
        self.ok('Created 30 broadcast sessions')

    # ── categories & tags ─────────────────────────────────────────────────────
    def _seed_categories_tags(self):
        self.section('Categories & Tags')
        self._categories = {}
        for cat_name in ARTICLE_CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=uslug(cat_name),
                partner=self._partner,
                defaults={
                    'name': cat_name,
                    'description': f'Kategori artikel {cat_name} Kabulhaden Online.',
                    'active': True,
                }
            )
            self._categories[cat_name] = cat

        all_tags = set()
        for a in ARTICLES:
            all_tags.update(a.get('tags', []))
        self._tags = {}
        for tag_name in all_tags:
            t, _ = Tag.objects.get_or_create(
                slug=uslug(tag_name),
                partner=self._partner,
                defaults={'name': tag_name}
            )
            self._tags[tag_name] = t

        self.ok(f'Created {len(self._categories)} categories, {len(self._tags)} tags')

    # ── articles ──────────────────────────────────────────────────────────────
    def _seed_articles(self):
        self.section('Articles')
        author_keys = list(self._authors.keys())
        count = 0
        for art_data in ARTICLES:
            cat = self._categories.get(art_data['category_name'])
            author = self._authors.get(random.choice(author_keys))
            article, created = Article.objects.get_or_create(
                slug=uslug(art_data['title']),
                defaults={
                    'title': art_data['title'],
                    'excerpt': art_data['excerpt'],
                    'content': art_data['content'],
                    'category': cat,
                    'author': author,
                    'author_name': author.name if author else 'Tim Redaksi',
                    'partner': self._partner,
                    'status': art_data['status'],
                    'featured': art_data.get('featured', False),
                    'allow_comments': True,
                    'content_format': 'RICH_TEXT',
                    'version': 1,
                    'publish_date': ago(days=art_data['days_ago']),
                    'word_count': random.randint(250, 600),
                    'reading_time_minutes': random.randint(2, 5),
                    'view_count': random.randint(100, 5000),
                    'priority': 'NORMAL',
                }
            )
            if created:
                for tag_name in art_data.get('tags', []):
                    if tag_name in self._tags:
                        article.tags.add(self._tags[tag_name])
                count += 1
        self.ok(f'Created {count} articles')

    # ── podcasts ──────────────────────────────────────────────────────────────
    def _seed_podcasts(self):
        self.section('Podcasts & Episodes')
        author = list(self._authors.values())[0]
        ep_count = 0

        for pod_data in PODCASTS:
            pod, _ = Podcast.objects.get_or_create(
                slug=uslug(pod_data['title']),
                defaults={
                    'title': pod_data['title'],
                    'description': pod_data['description'],
                    'short_description': pod_data['short_description'],
                    'category': pod_data.get('category', 'ENTERTAINMENT'),
                    'partner': self._partner,
                    'author': author,
                    'author_name': author.name,
                    'language': 'id',
                    'active': True,
                    'featured': True,
                    'status': 'APPROVED',
                    'priority': 'NORMAL',
                    'content_format': 'RICH_TEXT',
                    'version': 1,
                }
            )

            for ep_num, (ep_title, duration_min) in enumerate(pod_data['episodes'], start=1):
                PodcastEpisode.objects.get_or_create(
                    podcast=pod,
                    episode_number=ep_num,
                    defaults={
                        'title': ep_title,
                        'slug': uslug(ep_title, str(ep_num)),
                        'description': (
                            f'Episode {ep_num} dari podcast {pod_data["title"]}. '
                            f'{pod_data["short_description"]} Durasi: {duration_min} menit.'
                        ),
                        'duration': duration_min * 60,
                        'season_number': 1,
                        'published': True,
                        'publish_date': ago(days=(ep_num * 14)),
                        'download_count': random.randint(200, 2000),
                        'partner': self._partner,
                        'status': 'APPROVED',
                        'content_format': 'RICH_TEXT',
                        'version': 1,
                        'audio_url': f'https://cdn.kabulhaden.online/podcast/{slugify(pod_data["title"])}/ep{ep_num}.mp3',
                    }
                )
                ep_count += 1

        self.ok(f'Created {len(PODCASTS)} podcasts with {ep_count} episodes')

    # ── sponsors ──────────────────────────────────────────────────────────────
    def _seed_sponsors(self):
        self.section('Sponsors & Advertisements')
        sp_count = 0
        for sp_data in SPONSORS:
            sp, created = SponsorPartner.objects.get_or_create(
                name=sp_data['name'],
                defaults={
                    'slug': uslug(sp_data['name']),
                    'description': sp_data['description'],
                    'partner_type': sp_data['partner_type'],
                    'tier': sp_data['tier'],
                    'website': sp_data['website'],
                    'contact_email': sp_data['contact_email'],
                    'active': True,
                    'featured': sp_data['tier'] in ('platinum', 'gold'),
                    'display_order': sp_count + 1,
                }
            )
            if created:
                sp_count += 1

        for ad_data in ADVERTISEMENTS:
            Advertisement.objects.get_or_create(
                title=ad_data['title'],
                defaults={
                    'link_url': ad_data['link_url'],
                    'ad_type': ad_data['ad_type'],
                    'impressions': ad_data['impressions'],
                    'clicks': ad_data['clicks'],
                    'active': ad_data['active'],
                    'start_date': ago(days=30),
                    'end_date': NOW + timedelta(days=60),
                    'display_order': 1,
                }
            )

        self.ok(f'Created {len(SPONSORS)} sponsors, {len(ADVERTISEMENTS)} advertisements')

    # ── analytics ─────────────────────────────────────────────────────────────
    def _seed_analytics(self):
        self.section('Analytics (listener statistics)')
        # Already seeded in _seed_radio, just log
        count = ListenerStatistic.objects.filter(station=self._station).count()
        self.ok(f'{count} listener statistic records (daily, 90-day span)')

    # ── announcements ─────────────────────────────────────────────────────────
    def _seed_announcements(self):
        self.section('Announcements')
        announcements = [
            {
                'title': 'Selamat Datang di Kabulhaden Online',
                'content': (
                    'Terima kasih telah bergabung dengan komunitas pendengar Kabulhaden Online. '
                    'Nikmati program-program berkualitas kami setiap hari!'
                ),
                'active': True,
                'days_ago': 1,
            },
            {
                'title': 'Pembaruan Jadwal Program Akhir Pekan',
                'content': (
                    'Mulai pekan ini, jadwal siaran akhir pekan mengalami penyesuaian. '
                    'Program Pagi Bersama Kabulhaden kini tayang pukul 07.00–09.00 WIB.'
                ),
                'active': True,
                'days_ago': 5,
            },
            {
                'title': 'Maintenance Server: Minggu 28 Juli, Pukul 02.00–04.00 WIB',
                'content': (
                    'Kami akan melakukan pemeliharaan sistem pada Minggu dini hari. '
                    'Siaran mungkin terganggu sementara selama periode tersebut. Mohon maaf atas ketidaknyamanannya.'
                ),
                'active': False,
                'days_ago': 10,
            },
        ]
        count = 0
        for ann in announcements:
            _, created = Announcement.objects.get_or_create(
                title=ann['title'],
                defaults={
                    'content': ann['content'],
                    'active': ann['active'],
                    'publish_start': ago(days=ann['days_ago']),
                    'publish_end': NOW + timedelta(days=30),
                }
            )
            if created:
                count += 1
        self.ok(f'Created {count} announcements')

    # ── audit logs ────────────────────────────────────────────────────────────
    def _seed_audit_logs(self):
        self.section('Audit Logs')
        admin_user = self._users.get('admin')
        editor_user = self._users.get('editor')
        if not admin_user:
            self.ok('No admin user, skipping audit logs')
            return

        # Create fake admin log entries for recent activity
        article_ct = ContentType.objects.get_for_model(Article)
        program_ct = ContentType.objects.get_for_model(Program)

        entries = [
            (admin_user, ADDITION, article_ct, 'Workshop Podcasting Gratis untuk Anak Muda Kabulhaden', 1),
            (editor_user or admin_user, ADDITION, article_ct, 'Kolaborasi Kabulhaden dengan Dinas Pariwisata', 2),
            (admin_user, CHANGE, program_ct, 'Pagi Bersama Kabulhaden — jadwal diperbarui', 3),
            (editor_user or admin_user, ADDITION, article_ct, 'Festival Musik Kabulhaden 2024', 5),
            (admin_user, CHANGE, article_ct, 'Kabulhaden Online Raih Penghargaan Radio Digital', 7),
            (admin_user, ADDITION, program_ct, 'Bisnis Lokal Kabulhaden — program baru', 10),
        ]

        for user, flag, ct, obj_repr, days in entries:
            if not LogEntry.objects.filter(object_repr=obj_repr[:200]).exists():
                LogEntry.objects.create(
                    user=user,
                    content_type=ct,
                    object_id='1',
                    object_repr=obj_repr[:200],
                    action_flag=flag,
                    change_message=f'[{{"added": {{}}}}]' if flag == ADDITION else f'[{{"changed": {{"fields": ["status"]}}}}]',
                    action_time=ago(days=days),
                )

        self.ok(f'Created {len(entries)} audit log entries')
