from __future__ import annotations
import random
from typing import TYPE_CHECKING
from config import LEBAR, TANAH_Y, GRAVITASI_BOLA, PANTUL_BOLA, LEBAR_GAWANG

if TYPE_CHECKING:
    from .pemain import Pemain
    from .bola import Bola


class BotAI:
    def __init__(self, bot: Pemain) -> None:
        self.bot: Pemain = bot

    def prediksi_bola_x(self, bola: Bola) -> float:
        prediksi_x = bola.x
        prediksi_y = bola.y
        prediksi_kec_x = bola.kecepatan_x
        prediksi_kec_y = bola.kecepatan_y

        # Simulasikan gerakan bola beberapa frame ke depan
        for _ in range(90):
            prediksi_kec_y += GRAVITASI_BOLA
            prediksi_x += prediksi_kec_x
            prediksi_y += prediksi_kec_y

            if prediksi_x < LEBAR_GAWANG + bola.radius:
                prediksi_x = LEBAR_GAWANG + bola.radius
                prediksi_kec_x = -prediksi_kec_x * PANTUL_BOLA
            elif prediksi_x > LEBAR - LEBAR_GAWANG - bola.radius:
                prediksi_x = LEBAR - LEBAR_GAWANG - bola.radius
                prediksi_kec_x = -prediksi_kec_x * PANTUL_BOLA

            if prediksi_y >= TANAH_Y - self.bot.radius:
                break
        return prediksi_x

    def update(self, bola: Bola) -> None:
        self.bot.berhenti()

        perkiraan_x = self.prediksi_bola_x(bola)
        jarak_x = bola.x - self.bot.x
        jarak_y = bola.y - self.bot.y
        posisi_bertahan_x = LEBAR - LEBAR_GAWANG - 65

        # Bot mundur ke belakang jika bola masih di wilayah kiri
        if bola.x < LEBAR * 0.45 and bola.kecepatan_x < 3:
            target_x = posisi_bertahan_x
            if abs(self.bot.x - target_x) > 12:
                if self.bot.x < target_x:
                    self.bot.gerak_kanan()
                else:
                    self.bot.gerak_kiri()
        else:
            # Berdiri di kanan titik jatuh bola agar bisa menendang ke gawang kiri
            target_x = perkiraan_x + 28
            target_x = min(max(target_x, LEBAR * 0.35), LEBAR - LEBAR_GAWANG - 25)

            # Batasi agar bot tidak bergetar saat mendekati target
            if abs(self.bot.x - target_x) > 14:
                if self.bot.x < target_x:
                    self.bot.gerak_kanan()
                else:
                    self.bot.gerak_kiri()

            if -130 < jarak_x < 45 and bola.y < TANAH_Y - 85 and bola.kecepatan_y > -4:
                if random.random() < 0.25:
                    self.bot.lompat()

            # Bola berada di belakang bot, lompat untuk menyapu bola
            if bola.x > self.bot.x + 10 and self.bot.di_tanah:
                self.bot.lompat()

        if -75 < jarak_x < 10 and abs(jarak_y) < 55:
            if random.random() < 0.45:
                self.bot.tendang()
