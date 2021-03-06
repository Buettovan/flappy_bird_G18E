import pygame as pg
import random as rnd


def zeichne_kachel(pos):
  x, y = pos[0]*raster+rand, pos[1]*raster+rand
  br = hö = raster - rand
  pg.draw.rect(screen, farben[brett[pos]], (x, y, br, hö))
  if brett[pos] == 0:
    return
  zeichne_text(str(brett[pos]), raster//2, (x+br//2, y+hö//2), (255, 255, 255))


def zeichne_text(text, font_size, pos, farbe):
  t = pg.font.SysFont('Arial', font_size).render(text, False, farbe)
  t_rect = t.get_rect(center=pos)
  screen.blit(t, t_rect)


def setze_neue_2(board):
  freie_felder = [pos for pos in board if board[pos] == 0]
  if not freie_felder:
    return False
  pos = rnd.choice(freie_felder)
  board[pos] = 2
  return True


def verschiebe(key, board, score):
  x_delta, y_delta = richtungen[key]
  while True:
    change = False
    for (x, y), wert in board.items():
      zu_pos = (x+x_delta, y+y_delta)
      if zu_pos not in board or wert == 0:
        continue
      if board[zu_pos] == 0 or board[zu_pos] == wert:
        change = True
        board[(x, y)] = 0
        if board[zu_pos] == 0:
          board[zu_pos] = wert
        else:
          board[zu_pos] = wert * 2
          score += wert * 2
    if not change:
      return score


def monte_carlo(anz):
  erg = []
  for r in range(4):
    summe = 0
    for i in range(anz):
      b = brett.copy()
      neuer_score = verschiebe(keys[r], b, score)
      setze_neue_2(b)
      while True:
        neuer_score = verschiebe(rnd.choice(keys), b, neuer_score)
        if not setze_neue_2(b):
          break
      summe += neuer_score
    erg.append([summe, r])
  return keys[sorted(erg)[-1][1]]


pg.init()
raster = 150
rand = raster // 8
brett = {(x, y): 0 for x in range(4) for y in range(4)}
richtungen = {pg.K_DOWN: (0, 1), pg.K_UP: (
    0, -1), pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0)}
keys = [k for k in richtungen]
farben = {0: '#CDC0B4', 2: '#EEE4DA', 4: '#EDE0C8', 8: '#EDE0C8', 16: '#F59563',
          32: '#F67C60', 64: '#F65E3B', 128: '#EDCF73', 256: '#EDCC62',
          512: '#EDC850', 1024: '#EDC850', 2048: '#EDC22D', 4096: '#000000', 8192: '#000000'}
score = 0
screen = pg.display.set_mode((raster*4+rand, raster*4+rand))

weitermachen = True
clock = pg.time.Clock()
setze_neue_2(brett)
spielstatus = True

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key in richtungen:
      score = verschiebe(ereignis.key, brett, score)
      setze_neue_2(brett)
  screen.fill('#BBADA0')
  for pos in brett:
    zeichne_kachel(pos)
  # hier spielt die KI!!!!!
  if spielstatus:
    score = verschiebe(monte_carlo(10), brett, score)
    if not setze_neue_2(brett):
      spielstatus = False
  pg.display.flip()

pg.quit()
