import pygame
from config import (
    LEBAR,
    TANAH_Y,
    GRAVITASI,
    LEBAR_GAWANG,
    PUTIH,
    HITAM,
    ABU_TUA,
)


class Pemain:
    def __init__(
        self,
        x: float,
        warna: tuple[int, int, int],
        warna_gelap: tuple[int, int, int],
        menghadap_kanan: bool,
        adalah_bot: bool = False,
    ) -> None:
        self.x_awal: float = x
        self.radius: int = 32
        self.x: float = x
        self.y: float = TANAH_Y - self.radius
        self.kecepatan_x: float = 0.0
        self.kecepatan_y: float = 0.0
        self.warna: tuple[int, int, int] = warna
        self.warna_gelap: tuple[int, int, int] = warna_gelap
        self.menghadap_kanan: bool = menghadap_kanan
        self.adalah_bot: bool = adalah_bot

        self.kecepatan: float = 5.8
        self.kekuatan_lompat: float = -13.2
        self.di_tanah: bool = True

        self.sedang_menendang: bool = False
        self.timer_tendang: int = 0
        self.durasi_tendang: int = 12
        self.jeda_tendang: int = 0
        self.jeda_tendang_maks: int = 24

    def reset(self) -> None:
        self.x = self.x_awal
        self.y = TANAH_Y - self.radius
        self.kecepatan_x = 0.0
        self.kecepatan_y = 0.0
        self.di_tanah = True
        self.sedang_menendang = False
        self.timer_tendang = 0
        self.jeda_tendang = 0

    def gerak_kiri(self) -> None:
        self.kecepatan_x = -self.kecepatan

    def gerak_kanan(self) -> None:
        self.kecepatan_x = self.kecepatan

    def berhenti(self) -> None:
        self.kecepatan_x = 0.0

    def lompat(self) -> None:
        if self.di_tanah:
            self.kecepatan_y = self.kekuatan_lompat
            self.di_tanah = False

    def tendang(self) -> None:
        if self.jeda_tendang == 0 and not self.sedang_menendang:
            self.sedang_menendang = True
            self.timer_tendang = self.durasi_tendang
            self.jeda_tendang = self.jeda_tendang_maks

    def update(self) -> None:
        self.kecepatan_y += GRAVITASI
        self.x += self.kecepatan_x
        self.y += self.kecepatan_y

        if self.y + self.radius >= TANAH_Y:
            self.y = TANAH_Y - self.radius
            self.kecepatan_y = 0.0
            self.di_tanah = True

        batas_kiri = LEBAR_GAWANG - 10 + self.radius
        batas_kanan = LEBAR - LEBAR_GAWANG + 10 - self.radius
        if self.x < batas_kiri:
            self.x = batas_kiri
        elif self.x > batas_kanan:
            self.x = batas_kanan

        if self.sedang_menendang:
            self.timer_tendang -= 1
            if self.timer_tendang <= 0:
                self.sedang_menendang = False

        if self.jeda_tendang > 0:
            self.jeda_tendang -= 1

    def hitbox_tendang(self) -> pygame.Rect:
        if self.menghadap_kanan:
            return pygame.Rect(self.x + 5, self.y - 5, 48, 45)
        else:
            return pygame.Rect(self.x - 53, self.y - 5, 48, 45)

    def gambar(self, layar: pygame.Surface) -> None:
        pusat_x, pusat_y = int(self.x), int(self.y)
        arah_hadap = 1 if self.menghadap_kanan else -1

        sepatu_x = pusat_x + arah_hadap * 10
        sepatu_y = pusat_y + self.radius - 6
        if self.sedang_menendang:
            sepatu_x += arah_hadap * 24
            sepatu_y -= 12
            kotak_ayunan = pygame.Rect(pusat_x - 40, pusat_y - 20, 80, 60)
            sudut_mulai = 0.0 if self.menghadap_kanan else 2.2
            sudut_akhir = 0.9 if self.menghadap_kanan else 3.14
            pygame.draw.arc(layar, PUTIH, kotak_ayunan, sudut_mulai, sudut_akhir, 3)

        kotak_sepatu = pygame.Rect(0, 0, 28, 14)
        kotak_sepatu.center = (sepatu_x, sepatu_y)
        pygame.draw.rect(layar, ABU_TUA, kotak_sepatu, border_radius=5)
        pygame.draw.rect(layar, PUTIH, kotak_sepatu, 2, border_radius=5)

        pygame.draw.circle(layar, self.warna, (pusat_x, pusat_y), self.radius)
        pygame.draw.circle(layar, self.warna_gelap, (pusat_x, pusat_y), self.radius, 3)

        pygame.draw.line(layar, PUTIH, (pusat_x - self.radius + 3, pusat_y - 10), (pusat_x + self.radius - 3, pusat_y - 10), 6)

        mata_x = pusat_x + arah_hadap * 13
        mata_y = pusat_y - 4
        pygame.draw.circle(layar, PUTIH, (mata_x, mata_y), 8)
        pygame.draw.circle(layar, HITAM, (mata_x + arah_hadap * 3, mata_y), 4)
