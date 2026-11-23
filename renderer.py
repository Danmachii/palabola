from __future__ import annotations
import math
import pygame
from typing import TYPE_CHECKING
from config import (
    LEBAR,
    TINGGI,
    TANAH_Y,
    PUTIH,
    HITAM,
    LANGIT_ATAS,
    LANGIT_BAWAH,
    RUMPUT,
    RUMPUT_GARIS,
    WARNA_TANAH,
    BIRU_P1,
    MERAH_P2,
    EMAS,
    ABU,
    ABU_TUA,
)

if TYPE_CHECKING:
    from game import Game


class Renderer:
    def __init__(self, layar: pygame.Surface) -> None:
        self.layar: pygame.Surface = layar
        self.font_besar: pygame.font.Font = pygame.font.SysFont("impact", 72)
        self.font_sedang: pygame.font.Font = pygame.font.SysFont("trebuchetms", 34, bold=True)
        self.font_kecil: pygame.font.Font = pygame.font.SysFont("consolas", 18, bold=True)

    def gambar_latar(self) -> None:
        self.layar.fill(LANGIT_ATAS)
        pygame.draw.rect(self.layar, LANGIT_BAWAH, (0, 180, LEBAR, TANAH_Y - 180))

        pygame.draw.rect(self.layar, (35, 45, 65), (0, 320, LEBAR, 180))
        for baris in range(345, 490, 28):
            for kolom in range(30, LEBAR - 20, 25):
                warna_penonton = (70, 85, 110) if (baris + kolom) % 2 == 0 else (55, 70, 95)
                pygame.draw.circle(self.layar, warna_penonton, (kolom, baris), 9)

        pygame.draw.rect(self.layar, (200, 160, 40), (0, TANAH_Y - 35, LEBAR, 35))
        pygame.draw.line(self.layar, PUTIH, (0, TANAH_Y - 35), (LEBAR, TANAH_Y - 35), 3)

        pygame.draw.rect(self.layar, RUMPUT, (0, TANAH_Y, LEBAR, TINGGI - TANAH_Y))
        for i in range(0, LEBAR, 100):
            pygame.draw.rect(self.layar, RUMPUT_GARIS, (i, TANAH_Y, 50, TINGGI - TANAH_Y))

        pygame.draw.rect(self.layar, WARNA_TANAH, (0, TINGGI - 25, LEBAR, 25))
        pygame.draw.line(self.layar, PUTIH, (0, TANAH_Y), (LEBAR, TANAH_Y), 4)
        pygame.draw.circle(self.layar, PUTIH, (LEBAR // 2, TANAH_Y), 50, 3)

    def gambar_ui(self, game: Game) -> None:
        kotak_skor = pygame.Rect(LEBAR // 2 - 170, 15, 340, 68)
        pygame.draw.rect(self.layar, ABU_TUA, kotak_skor, border_radius=12)
        pygame.draw.rect(self.layar, PUTIH, kotak_skor, 3, border_radius=12)

        teks_skor_p1 = self.font_sedang.render(str(game.skor_p1), True, BIRU_P1)
        self.layar.blit(teks_skor_p1, (LEBAR // 2 - 115 - teks_skor_p1.get_width() // 2, 28))

        teks_skor_p2 = self.font_sedang.render(str(game.skor_p2), True, MERAH_P2)
        self.layar.blit(teks_skor_p2, (LEBAR // 2 + 115 - teks_skor_p2.get_width() // 2, 28))

        waktu = math.ceil(game.sisa_waktu)
        warna_waktu = EMAS if waktu > 10 else MERAH_P2
        teks_waktu = self.font_sedang.render(f"{waktu:02d}", True, warna_waktu)
        self.layar.blit(teks_waktu, (LEBAR // 2 - teks_waktu.get_width() // 2, 28))

        mode_teks = "BOT (AI)" if game.p2.adalah_bot else "MANUAL"
        info_teks = f"P1: W,A,S,D (S=Tendang) | P2 [{mode_teks}]: Panah (Bawah=Tendang) | [TAB] Toggle AI"
        teks_info = self.font_kecil.render(info_teks, True, PUTIH)
        self.layar.blit(teks_info, (LEBAR // 2 - teks_info.get_width() // 2, TINGGI - 22))

        if game.status == "GOL":
            teks_gol = self.font_besar.render("GOOOAAALLL!", True, EMAS)
            teks_bayangan = self.font_besar.render("GOOOAAALLL!", True, HITAM)
            gol_x = LEBAR // 2 - teks_gol.get_width() // 2
            gol_y = TINGGI // 2 - 90
            self.layar.blit(teks_bayangan, (gol_x + 4, gol_y + 4))
            self.layar.blit(teks_gol, (gol_x, gol_y))

            teks_sub = self.font_sedang.render(f"Dicetak oleh {game.pencetak_terakhir}", True, PUTIH)
            self.layar.blit(teks_sub, (LEBAR // 2 - teks_sub.get_width() // 2, gol_y + 80))

        elif game.status == "SELESAI":
            lapisan_gelap = pygame.Surface((LEBAR, TINGGI), pygame.SRCALPHA)
            lapisan_gelap.fill((0, 0, 0, 185))
            self.layar.blit(lapisan_gelap, (0, 0))

            teks_selesai = self.font_besar.render("WAKTU HABIS!", True, PUTIH)
            self.layar.blit(teks_selesai, (LEBAR // 2 - teks_selesai.get_width() // 2, TINGGI // 2 - 120))

            if game.skor_p1 > game.skor_p2:
                teks_pemenang, warna_pemenang = "PLAYER 1 (BIRU) MENANG!", BIRU_P1
            elif game.skor_p2 > game.skor_p1:
                teks_pemenang, warna_pemenang = "PLAYER 2 (MERAH) MENANG!", MERAH_P2
            else:
                teks_pemenang, warna_pemenang = "PERTANDINGAN SERI (DRAW)!", EMAS

            teks_menang = self.font_sedang.render(teks_pemenang, True, warna_pemenang)
            self.layar.blit(teks_menang, (LEBAR // 2 - teks_menang.get_width() // 2, TINGGI // 2 - 25))

            teks_ulang = self.font_kecil.render("Tekan tombol [ R ] untuk Main Lagi", True, ABU)
            self.layar.blit(teks_ulang, (LEBAR // 2 - teks_ulang.get_width() // 2, TINGGI // 2 + 45))
