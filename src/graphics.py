def display_map(screen, config, level, player):
    tiles = level.map.tiles
    tile_legend = level.map.legend
    for map_y in range(0, screen.map_display_height):
        for map_x in range(0, screen.map_display_width):
            x_offset, y_offset = screen.camera.get_offset(level, player)
            current_index = level.map.get_index(
                map_x - x_offset, map_y - y_offset
            )
            image = tile_legend.get(unicode(tiles[current_index]), '')
            screen.draw_tile(image, (map_x, map_y))


def display_player(screen, config, level, player):
    screen.draw_tile_relative(
        config.player_image, (player.x, player.y), level, player
    )


def display_monsters(screen, config, level, player):
    for monster in level.monsters:
        screen.draw_tile_relative(monster.image, (monster.x, monster.y), level, player)


def display_items(screen, config, level, player):
    for item_coords in level.item_coordinates:
        item = next((x for x in level.items if x.id == item_coords['id']), None)
        screen.draw_tile_relative(
            item.image, item_coords['coordinates'], level, player
        )


def display_player_items(screen, config, level, player):
    screen.draw_text(
        config.score_font, 'Inventory:', (0, 420), 'black'
    )
    for index, item in enumerate(player.items):
        # Position each item from left to right with respect to ordering and
        # on the bottom tile, adjusted by 8 for some padding
        x = index * screen.tile_width
        y = screen.height - screen.tile_height - 8
        screen.draw(item.image, (x, y))


def draw_popup(screen, config, level, player, strings):
    # Create the black surface for the popup area to go onto
    char_width = config.popup_box['char_width']
    char_height = config.popup_box['char_height']
    x_margin, y_margin = 10, 10
    surface_width = 10 * char_width + x_margin * 2
    surface_height = 25 * char_height + y_margin * 2
    message_surface = screen.get_surface(surface_width, surface_height)
    box_x, box_y = config.popup_box['x'], config.popup_box['y']
    for index, string in enumerate(strings):
        screen.draw_text(
            config.score_font, string,
            (x_margin, y_margin + index * 20), surface=message_surface
        )
        screen.draw(message_surface, (box_x, box_y))


def draw_splash(screen, config, image):
    width = screen.width
    height = screen.height
    message_surface = screen.get_surface(width, height)
    origin = (0, 0)
    if image:
        screen.draw(image, origin, surface=message_surface)
    screen.draw(message_surface, origin)


def render(game_data, questions, level, player):
    game_state, screen, config = game_data.state, game_data.screen, game_data.config
    with screen.display_cycle():
        display_map(screen, config, level, player)
        display_items(screen, config, level, player)
        display_monsters(screen, config, level, player)
        display_player(screen, config, level, player)
        display_player_items(screen, config, level, player)
        if game_state.is_state('question'):
            draw_popup(
                screen, config, level, player,
                questions.get_question_display()
            )
        if game_state.is_state('splash'):
            draw_splash(screen, config, config.splash_image)
        if game_state.is_state('endscreen'):
            draw_splash(screen, config, config.endscreen_image)
        if game_state.is_state('item'):
            draw_popup(screen, config, level, player, player.current_item.message)
        if game_state.is_state('info'):
            draw_popup(screen, config, level, player, [
                'Honey Badger got you! You lost all of your items', '',
                'Press <Enter> to return'
            ])
