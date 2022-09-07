# def highlight_tile_model_zone(self, top_left_corner: Point, bottom_right_corner: Point):
#     square_size = 15
#     x_offset = 600
#     y_offset = 25
#
#     for row in range(15):
#         for col in range(16):
#             draw_x = col * square_size + x_offset
#             draw_y = row * square_size + y_offset
#
#             if top_left_corner.y <= row <= bottom_right_corner.y and bottom_right_corner.x >= col >= top_left_corner.x:
#                 pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(draw_x, draw_y, square_size, square_size), width=1)

# def draw_tile_model(self, tile_map: {}):
#     square_size = 15
#     x_offset = 600
#     y_offset = 25
#
#     for row in range(15):
#         for col in range(16):
#             pos = (row, col)
#             current_tile = tile_map[pos]
#             draw_x = col * square_size + x_offset
#             draw_y = row * square_size + y_offset
#
#             self.draw_square_from_tile(current_tile, draw_x, draw_y, square_size)
#
# def draw_minimal_tile_model(self, tile_map: {}, mario_location: Point, right_view, back_view, up_view, down_view):
#     square_size = 20
#     x_offset = 500
#     y_offset = 225
#
#     for row in range(mario_location.y - up_view, mario_location.y + down_view + 1):
#         for col in range(mario_location.x - back_view, mario_location.x + right_view + 1):
#
#             # if within model matrix
#             if (0 <= row < 15) and (0 <= col < 16):
#                 pos = (row, col)
#                 current_tile = tile_map[pos]
#                 draw_x = col * square_size + x_offset
#                 draw_y = row * square_size + y_offset
#
#                 self.draw_square_from_tile(current_tile, draw_x, draw_y, square_size)
#
#     def highlight_minimal_tile_model(self, mario_location: Point, right_view, back_view, up_view, down_view):
#         square_size = 15
#         x_offset = 600
#         y_offset = 25
#
#         for row in range(mario_location.y - up_view, mario_location.y + down_view + 1):
#             for col in range(mario_location.x - back_view, mario_location.x + right_view + 1):
#
#                 if (0 <= row < 15) and (0 <= col < 16):
#                     draw_x = col * square_size + x_offset
#                     draw_y = row * square_size + y_offset
#
#                     pygame.draw.rect(self.window, (30, 144, 255), pygame.Rect(draw_x, draw_y, square_size, square_size), width=1)