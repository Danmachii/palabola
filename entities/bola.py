from __future__ import annotations
import math
import random
import pygame
from typing import TYPE_CHECKING
from config import (
    LEBAR,
    TANAH_Y,
    GRAVITASI_BOLA,
    PANTUL_BOLA,
    GESEKAN_UDARA,
    GESEKAN_TANAH,
    RADIUS_TIANG,
    PUTIH,
    HITAM,
)

if TYPE_CHECKING:
    from .gawang import Gawang


class Bola:
    def __init__(self) -> None:
        self.radius: int = 20
        self.x: float = 0.0
        self.y: float = 0.0
        self.kecepatan_x: float = 0.0
        self.kecepatan_y: float = 0.0
        self.reset()

    def reset(self) -> None:
        self.x = LEBAR // 2
        self.y = 160.0
        self.kecepatan_x = random.choice([-2.0, -1.0, 1.0, 2.0])
        self.kecepatan_y = 0.0

    def update(self) -> None:
        self.kecepatan_y += GRAVITASI_BOLA
        self.kecepatan_x *= GESEKAN_UDARA
        self.x += self.kecepatan_x
        self.y += self.kecepatan_y

        if self.y + self.radius >= TANAH_Y:
            self.y = TANAH_Y - self.radius
            self.kecepatan_y = -self.kecepatan_y * PANTUL_BOLA
            self.kecepatan_x *= GESEKAN_TANAH
            if abs(self.kecepatan_y) < 1.2:
                self.kecepatan_y = 0.0

        if self.y - self.radius <= 0:
            self.y = float(self.radius)
            self.kecepatan_y = -self.kecepatan_y * PANTUL_BOLA

        if self.x - self.radius <= 0:
            self.x = float(self.radius)
            self.kecepatan_x = -self.kecepatan_x * PANTUL_BOLA
        elif self.x + self.radius >= LEBAR:
            self.x = float(LEBAR - self.radius)
            self.kecepatan_x = -self.kecepatan_x * PANTUL_BOLA

        kecepatan_maks = 19.0
        laju = math.hypot(self.kecepatan_x, self.kecepatan_y)
        if laju > kecepatan_maks:
            skala = kecepatan_maks / laju
            self.kecepatan_x *= skala
            self.kecepatan_y *= skala

    def cek_tabrakan_gawang(self, gawang: Gawang) -> bool:
        selisih_x = self.x - gawang.tiang_x
        selisih_y = self.y - gawang.tiang_y
        jarak = math.hypot(selisih_x, selisih_y)
        jarak_minimal = self.radius + RADIUS_TIANG

        # Pantulan melingkar di ujung tiang
        if 0 < jarak < jarak_minimal:
            arah_x = selisih_x / jarak
            arah_y = selisih_y / jarak
            tumpang_tindih = jarak_minimal - jarak
            self.x += arah_x * tumpang_tindih
            self.y += arah_y * tumpang_tindih

            proyeksi = self.kecepatan_x * arah_x + self.kecepatan_y * arah_y
            if proyeksi < 0:
                self.kecepatan_x = (self.kecepatan_x - 2 * proyeksi * arah_x) * PANTUL_BOLA
                self.kecepatan_y = (self.kecepatan_y - 2 * proyeksi * arah_y) * PANTUL_BOLA

        # Pantulan di atap mistar gawang
        di_atas_gawang = (self.x < gawang.tiang_x) if gawang.di_kiri else (self.x > gawang.tiang_x)
        if di_atas_gawang and abs(self.y - gawang.tiang_y) < self.radius + 4:
            if self.kecepatan_y > 0 and self.y < gawang.tiang_y:
                self.y = gawang.tiang_y - self.radius - 4
                self.kecepatan_y = -self.kecepatan_y * PANTUL_BOLA
            elif self.kecepatan_y < 0 and self.y > gawang.tiang_y:
                self.y = gawang.tiang_y + self.radius + 4
                self.kecepatan_y = -self.kecepatan_y * PANTUL_BOLA

        # Cek bola melewati garis gawang
        if self.y > gawang.y + RADIUS_TIANG:
            if gawang.di_kiri and self.x - self.radius < gawang.tiang_x - 10:
                return True
            elif not gawang.di_kiri and self.x + self.radius > gawang.tiang_x + 10:
                return True

        return False

    def gambar(self, layar: pygame.Surface) -> None:
        pusat_x, pusat_y = int(self.x), int(self.y)
        pygame.draw.circle(layar, PUTIH, (pusat_x, pusat_y), self.radius)

        sudut_awal = self.x * 0.05
        titik_dalam = []
        for i in range(5):
            sudut = sudut_awal + i * (2 * math.pi / 5)
            titik_x = pusat_x + math.cos(sudut) * (self.radius * 0.42)
            titik_y = pusat_y + math.sin(sudut) * (self.radius * 0.42)
            titik_dalam.append((titik_x, titik_y))

            tepi_x = pusat_x + math.cos(sudut) * self.radius
            tepi_y = pusat_y + math.sin(sudut) * self.radius
            pygame.draw.line(layar, HITAM, (titik_x, titik_y), (tepi_x, tepi_y), 2)

        pygame.draw.polygon(layar, HITAM, titik_dalam)
        pygame.draw.circle(layar, HITAM, (pusat_x, pusat_y), self.radius, 2)
