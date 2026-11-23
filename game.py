import sys
import pygame
from config import LEBAR, TINGGI, FPS, BIRU_P1, BIRU_TUA, MERAH_P2, MERAH_TUA, LEBAR_GAWANG
from entities import Gawang, Pemain, Bola, BotAI
from physics import tabrakan_pemain, tabrakan_pemain_dengan_bola
from renderer import Renderer


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.layar: pygame.Surface = pygame.display.set_mode((LEBAR, TINGGI))
        pygame.display.set_caption("Head Soccer 2D - Pygame (Tekan TAB untuk Toggle AI)")
        self.jam: pygame.time.Clock = pygame.time.Clock()

        self.p1: Pemain = Pemain(220, BIRU_P1, BIRU_TUA, menghadap_kanan=True, adalah_bot=False)
        self.p2: Pemain = Pemain(LEBAR - 220, MERAH_P2, MERAH_TUA, menghadap_kanan=False, adalah_bot=True)
        self.bot_ai: BotAI = BotAI(self.p2)
        self.bola: Bola = Bola()
        self.gawang_kiri: Gawang = Gawang(0, di_kiri=True)
        self.gawang_kanan: Gawang = Gawang(LEBAR - LEBAR_GAWANG, di_kiri=False)
        self.renderer: Renderer = Renderer(self.layar)

        self.skor_p1: int = 0
        self.skor_p2: int = 0
        self.sisa_waktu: float = 60.0
        self.status: str = "MAIN"
        self.timer_jeda_gol: float = 0.0
        self.pencetak_terakhir: str = ""

        self.mulai_ulang()

    def mulai_ulang(self) -> None:
        self.skor_p1 = 0
        self.skor_p2 = 0
        self.sisa_waktu = 60.0
        self.status = "MAIN"
        self.timer_jeda_gol = 0.0
        self.pencetak_terakhir = ""
        self.p1.reset()
        self.p2.reset()
        self.bola.reset()

    def proses_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.p2.adalah_bot = not self.p2.adalah_bot

                if self.status == "MAIN":
                    if event.key == pygame.K_w:
                        self.p1.lompat()
                    if event.key == pygame.K_s:
                        self.p1.tendang()

                    if not self.p2.adalah_bot:
                        if event.key == pygame.K_UP:
                            self.p2.lompat()
                        if event.key == pygame.K_DOWN:
                            self.p2.tendang()

                elif self.status == "SELESAI":
                    if event.key == pygame.K_r:
                        self.mulai_ulang()

        if self.status == "MAIN":
            tombol = pygame.key.get_pressed()

            self.p1.berhenti()
            if tombol[pygame.K_a]:
                self.p1.gerak_kiri()
            if tombol[pygame.K_d]:
                self.p1.gerak_kanan()

            if not self.p2.adalah_bot:
                self.p2.berhenti()
                if tombol[pygame.K_LEFT]:
                    self.p2.gerak_kiri()
                if tombol[pygame.K_RIGHT]:
                    self.p2.gerak_kanan()
            else:
                self.bot_ai.update(self.bola)

    def update(self, selisih_waktu: float) -> None:
        if self.status == "MAIN":
            self.sisa_waktu -= selisih_waktu
            if self.sisa_waktu <= 0:
                self.sisa_waktu = 0.0
                self.status = "SELESAI"
                return

            self.p1.update()
            self.p2.update()
            tabrakan_pemain(self.p1, self.p2)

            self.bola.update()
            tabrakan_pemain_dengan_bola(self.p1, self.bola)
            tabrakan_pemain_dengan_bola(self.p2, self.bola)

            if self.bola.cek_tabrakan_gawang(self.gawang_kiri):
                self.skor_p2 += 1
                self.pencetak_terakhir = "PLAYER 2 (MERAH)"
                self.status = "GOL"
                self.timer_jeda_gol = 1.5

            elif self.bola.cek_tabrakan_gawang(self.gawang_kanan):
                self.skor_p1 += 1
                self.pencetak_terakhir = "PLAYER 1 (BIRU)"
                self.status = "GOL"
                self.timer_jeda_gol = 1.5

        elif self.status == "GOL":
            self.bola.update()
            self.timer_jeda_gol -= selisih_waktu
            if self.timer_jeda_gol <= 0:
                self.p1.reset()
                self.p2.reset()
                self.bola.reset()
                self.status = "MAIN"

    def jalankan(self) -> None:
        while True:
            selisih_waktu = self.jam.tick(FPS) / 1000
            self.proses_input()
            self.update(selisih_waktu)

            self.renderer.gambar_latar()
            self.p1.gambar(self.layar)
            self.p2.gambar(self.layar)
            self.bola.gambar(self.layar)
            self.gawang_kiri.gambar(self.layar)
            self.gawang_kanan.gambar(self.layar)
            self.renderer.gambar_ui(self)

            pygame.display.flip()
