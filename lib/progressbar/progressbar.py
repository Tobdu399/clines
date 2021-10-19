import time
import pathlib

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


window_title        = "clines"
loading_text        = ""
current_process     = ""   # The item currently being processed
overall_progress    = 0    # The progress in per cents
current_progress    = 0
process_interrupted = False


def stop():
    global process_interrupted
    process_interrupted = True


def show():
    global loading_text, overall_progress, current_process, process_interrupted

    pygame.init()

    display      = pygame.display.set_mode((600, 250))
    clock        = pygame.time.Clock()
    elapsed_time = update_timer = loading_animation_timer = remaining_time_timer = 0

    pygame.display.set_caption(window_title)

    pygame.display.set_icon(pygame.image.load(str(pathlib.Path(__file__).resolve().parent.parent) + "/images/clines.png"))

    # -----------------------------------------------------

    display_size     = display.get_size()
    progressbar_size = (500, 20)

    starting_time    = time.time()
    time_remaining   = 0

    loading_dots     = ""

    font = pygame.font.Font(f"{pathlib.Path(__file__).resolve().parent}/lib/fonts/karmafuture.ttf", 20)

    while not process_interrupted:
        display.fill((255, 255, 255))

        # Overall Progress --------------------------------

        # Progress bar
        pygame.draw.rect(
            display, (0, 255, 0), (
                (display_size[0] / 2 - progressbar_size[0] / 2),
                (display_size[1] / 3.5 - progressbar_size[1] / 2),
                (progressbar_size[0] / 100) * overall_progress,
                progressbar_size[1]
            ), border_radius=5
        )

        # Progress bar borders
        pygame.draw.rect(
            display, (0, 0, 0), (
                (display_size[0] / 2 - progressbar_size[0]/2),
                (display_size[1] / 3.5 - progressbar_size[1]/2),
                progressbar_size[0], progressbar_size[1]
            ), width=1, border_radius=3
        )

        # Current process Progress ------------------------

        # Progress bar
        pygame.draw.rect(
            display, (0, 255, 0), (
                (display_size[0] / 2 - progressbar_size[0] / 2),
                ((display_size[1] - (display_size[1] / 3.5)) - progressbar_size[1] / 2),
                (progressbar_size[0] / 100) * current_progress,
                progressbar_size[1]
            ), border_radius=5
        )

        # Progress bar borders
        pygame.draw.rect(
            display, (0, 0, 0), (
                (display_size[0] / 2 - progressbar_size[0] / 2),
                ((display_size[1] - (display_size[1] / 3.5)) - progressbar_size[1] / 2),
                progressbar_size[0], progressbar_size[1]
            ), width=1, border_radius=3
        )

        # Overall progress bar text
        overall_progressbar_text = font.render(f"{loading_text}    {overall_progress:.1f} %", True, (0, 0, 0))
        display.blit(overall_progressbar_text, (
            (display_size[0] / 2 - progressbar_size[0] / 2) + (progressbar_size[0] - overall_progressbar_text.get_width()),
            (display_size[1] / 3.5 - progressbar_size[1] / 2) - (overall_progressbar_text.get_height() + 5),
        ))

        # Progressbar text
        progressbar_text = font.render(f"{current_progress:.1f} %", True, (0, 0, 0))
        display.blit(progressbar_text, (
            (display_size[0] / 2 - progressbar_size[0] / 2) + (progressbar_size[0] - progressbar_text.get_width()),
            ((display_size[1] - (display_size[1] / 3.5)) - (progressbar_text.get_height() + (5 + progressbar_size[1] / 2))),
        ))

        # Progressbar info text
        if overall_progress < 100:
            progressbar_info_text = font.render(f"Reading Files {loading_dots}", True, (0, 0, 0))
        else:
            progressbar_info_text = font.render(f"Done.", True, (0, 0, 0))

        display.blit(progressbar_info_text, (
            (display_size[0] / 2 - progressbar_size[0] / 2),
            (display_size[1] / 3.5 - progressbar_size[1] / 2) - (progressbar_text.get_height() + 5),
        ))

        # Current process text
        current_process_text = font.render(current_process, True, (0, 0, 0))

        display.blit(current_process_text, (
            (display_size[0] / 2 - progressbar_size[0] / 2),
            (display_size[1] - (display_size[1] / 3.5)) + (progressbar_text.get_height())
        ))

        # Time remaining text
        s = int(time_remaining)

        m = s // 60
        s = s - m*60
        h = m // 60
        m = m - h*60

        formatted_time_remaining = f"{h}h {m}m {s}s"

        time_remaining_text = font.render(formatted_time_remaining, True, (0, 0, 0))

        display.blit(time_remaining_text, (
            (display_size[0] / 2 - progressbar_size[0] / 2) + (progressbar_size[0] - time_remaining_text.get_width()),
            (display_size[1] / 3.5 - progressbar_size[1] / 2) + (time_remaining_text.get_height() + 5),
        ))

        # Update remaining time
        if 0 < overall_progress < 100:
            if int(remaining_time_timer / 1000) >= 1:
                time_remaining = ((time.time() - starting_time) / overall_progress) * (100 - overall_progress)

                remaining_time_timer = 0
        else:
            time_remaining = 0

        # Add dots to animate the loading text
        if overall_progress < 100:
            if int(loading_animation_timer / 250) >= 0.25:
                if len(loading_dots) < 3:
                    loading_dots += "."
                else:
                    loading_dots = ""

                loading_animation_timer = 0

        update_timer            += elapsed_time
        remaining_time_timer    += elapsed_time
        loading_animation_timer += elapsed_time

        # Keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                process_interrupted = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    process_interrupted = True

        pygame.display.update()
        elapsed_time = clock.tick()

    pygame.quit()


if __name__ == '__main__':
    show()
