from ai import *
from dog import *
from sheep import *
from map import *
import random as rand
import config
import copy
import pygame as pygame


class Simulation:

    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
        pg.display.set_caption("Zaganianie")
        map = Map(self.screen, pg.time.get_ticks())

        # Dogs INIT
        dog_collection = DogCollection(config.FENCE_CENTER)

        dog_sprites = []

        for d in dog_collection.dogs:
            dog_sprites.append(pg.sprite.RenderPlain(d))

        # Sheep INIT
        sheeps_collection = SheepCollection(self.screen)
        sheeps = sheeps_collection.get_sheep_new_list(GEN_SIZE)

        # Ai INIT
        ai_collection = AiCollection(dog_collection.dogs, sheeps, self.screen)

        while True:  # Game loop

            self.clock = pg.time.Clock()
            start_time = pg.time.get_ticks()
            config.SCORE = 0

            while True:  # Generation loop

                self.clock.tick(60)

                nxt_gen = False
                new_gen = False

                # EVENTS
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            nxt_gen = True
                        if event.key == pygame.K_p:
                            nxt_gen = True
                            new_gen = True

                if nxt_gen or float((pg.time.get_ticks() - start_time) / 1000) > config.GEN_TIME:
                    break

                keys = pg.key.get_pressed()

                if keys[pg.K_n]:
                    if config.GEN_TIME > 1:
                        config.GEN_TIME -= 1
                elif keys[pg.K_m]:
                    config.GEN_TIME += 1
                elif keys[pg.K_s]:
                    config.SHOW = True
                elif keys[pg.K_d]:
                    config.SHOW = False

                # Dog ACTION
                for ai in ai_collection.ais:
                    ai.move_dog1()
                    ai.update()

                for dog_sprite in dog_sprites:
                    dog_sprite.update()

                for dog in dog_collection.dogs:
                    dog.angle_speed = 0

                map.draw()  # map DRAW

                # Sheep DRAW + MOVE
                i = 0
                for sheep in sheeps:
                    sheep.moving(dog_collection.dogs[i])  # Sheep ACTION
                    i += 1
                    if config.SHOW:
                        sheep.draw()  # Sheep DRAW
                    else:
                        if i < NUM_TO_SHOW:
                            sheep.draw()  # Sheep DRAW

                # Dog DRAW
                if config.SHOW:
                    for dog in dog_collection.dogs:
                        pg.draw.circle(self.screen, (255, 255, 0), dog.position, dog.herding_range, 1)
                    for dog_sprite in dog_sprites:
                        dog_sprite.draw(self.screen)
                else:
                    for dog in dog_collection.dogs:
                        pg.draw.circle(self.screen, (255, 255, 0), dog.position, dog.herding_range, 1)
                        if dog_collection.dogs.index(dog) >= NUM_TO_SHOW:
                            break
                    for dog_sprite in dog_sprites:
                        dog_sprite.draw(self.screen)
                        if dog_sprites.index(dog_sprite) >= NUM_TO_SHOW:
                            break

                pg.display.flip()

            # Dogs INIT
            dog_collection = DogCollection(config.FENCE_CENTER)

            # Sheeps INIT
            if new_gen:
                sheeps = sheeps_collection.get_sheep_new_list(GEN_SIZE)
            else:
                sheeps = sheeps_collection.get_sheep_copy_list(GEN_SIZE)

            # Ai INIT
            ai_collection.evolve_population(dog_collection.dogs, sheeps)

            # Dogs next
            dog_sprites = []

            for d in dog_collection.dogs:
                dog_sprites.append(pg.sprite.RenderPlain(d))


if __name__ == '__main__':
    Simulation()
    pg.quit()
