import pygame
from config import TANAH_Y, TINGGI_GAWANG, LEBAR_GAWANG, RADIUS_TIANG, PUTIH, ABU


class Gawang:
    def __init__(self, x: int, di_kiri: bool) -> None:
        self.x: int = x
        self.y: int = TANAH_Y - TINGGI_GAWANG
        self.lebar: int = LEBAR_GAWANG
        self.tinggi: int = TINGGI_GAWANG
        self.di_kiri: bool = di_kiri

        if self.di_kiri:
            self.tiang_x: int = self.x + self.lebar
        else:
            self.tiang_x: int = self.x
        self.tiang_y: int = self.y

    def gambar(self, layar: pygame.Surface) -> None:
        warna_jaring = (210, 210, 210)
        for i in range(0, self.lebar + 1, 12):
            pygame.draw.line(layar, warna_jaring, (self.x + i, self.y), (self.x + i, TANAH_Y), 1)
        for j in range(0, self.tinggi + 1, 12):
            pygame.draw.line(layar, warna_jaring, (self.x, self.y + j), (self.x + self.lebar, self.y + j), 1)

        kerangka = pygame.Rect(self.x, self.y, self.lebar, self.tinggi)
        pygame.draw.rect(layar, PUTIH, kerangka, 4)

        pygame.draw.circle(layar, PUTIH, (self.tiang_x, self.tiang_y), RADIUS_TIANG)
        pygame.draw.circle(layar, ABU, (self.tiang_x, self.tiang_y), RADIUS_TIANG, 2)
