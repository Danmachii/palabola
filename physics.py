import math
import pygame
from config import TANAH_Y
from entities.pemain import Pemain
from entities.bola import Bola


def tabrakan_pemain(p1: Pemain, p2: Pemain) -> None:
    selisih_x = p2.x - p1.x
    selisih_y = p2.y - p1.y
    jarak = math.hypot(selisih_x, selisih_y)
    jarak_minimal = p1.radius + p2.radius

    if 0 < jarak < jarak_minimal:
        tumpang_tindih = (jarak_minimal - jarak) * 0.5
        arah_x = selisih_x / jarak
        p1.x -= arah_x * tumpang_tindih
        p2.x += arah_x * tumpang_tindih


def tabrakan_pemain_dengan_bola(pemain: Pemain, bola: Bola) -> None:
    if pemain.sedang_menendang:
        kotak_tendang = pemain.hitbox_tendang()
        kotak_bola = pygame.Rect(
            bola.x - bola.radius,
            bola.y - bola.radius,
            bola.radius * 2,
            bola.radius * 2,
        )
        if kotak_tendang.colliderect(kotak_bola):
            arah_hadap = 1 if pemain.menghadap_kanan else -1
            bola.kecepatan_x = arah_hadap * 15.5
            bola.kecepatan_y = -10.5
            pemain.sedang_menendang = False
            return

    selisih_x = bola.x - pemain.x
    selisih_y = bola.y - pemain.y
    jarak = math.hypot(selisih_x, selisih_y)
    jarak_minimal = bola.radius + pemain.radius

    if jarak < jarak_minimal:
        if jarak == 0:
            selisih_x, selisih_y, jarak = 0.0, -1.0, 1.0

        arah_x = selisih_x / jarak
        arah_y = selisih_y / jarak

        # Pisahkan posisi bola agar tidak terjepit di dalam kepala pemain
        tumpang_tindih = jarak_minimal - jarak
        bola.x += arah_x * (tumpang_tindih + 1.0)
        bola.y += arah_y * (tumpang_tindih + 1.0)

        if bola.y + bola.radius > TANAH_Y:
            bola.y = TANAH_Y - bola.radius
            bola.kecepatan_y = -9.0
            bola.kecepatan_x += (1 if pemain.menghadap_kanan else -1) * 5.0

        kec_relatif_x = bola.kecepatan_x - pemain.kecepatan_x
        kec_relatif_y = bola.kecepatan_y - pemain.kecepatan_y
        kecepatan_searah_normal = kec_relatif_x * arah_x + kec_relatif_y * arah_y

        if kecepatan_searah_normal < 0:
            koefisien_pantul = 0.85
            dorongan = -(1 + koefisien_pantul) * kecepatan_searah_normal
            bola.kecepatan_x += dorongan * arah_x + (pemain.kecepatan_x * 0.35)
            bola.kecepatan_y += dorongan * arah_y + (pemain.kecepatan_y * 0.35)

            if arah_y < -0.3:
                bola.kecepatan_y = min(bola.kecepatan_y, -8.5)
