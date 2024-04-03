import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))


class DrawInfo:
    pygame.display.set_caption("Sorting Algorithm Visualizer")

    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 46, 139, 87
    RED = 159, 7, 64
    BLUE = 0, 0, 255
    BUTTON_GREY = 26, 26, 29
    BUTTON_ACTIVE = 159, 7, 64
    BACKGROUND_COLOR = 26, 26, 29

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('arial', 25)
    LARGE_FONT = pygame.font.SysFont('arial', 30)
    SMALL_FONT = pygame.font.SysFont('arial', 20)
    SIDE_PAD = 100
    TOP_PAD = 200

    def __init__(self, lst):
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        self.block_width = (WIDTH - self.SIDE_PAD) // len(lst)
        self.block_height = (HEIGHT - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, DrawInfo.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw(draw_info, algo_name, ascending, buttons, sliders):
    window.fill(draw_info.BACKGROUND_COLOR)

    # sets our slider labels and displays them
    size_slider_label = draw_info.SMALL_FONT.render(f"Size of the Array", 1,
                                                    draw_info.WHITE)
    speed_slider_label = draw_info.SMALL_FONT.render(f"Speed of the Algorithm", 1,
                                                     draw_info.WHITE)
    window.blit(size_slider_label, (10, 5))
    window.blit(speed_slider_label, (10, 35))

    # cycles through all of our buttons and sliders and draws them
    for button in buttons:
        button.draw()
    for slider in sliders:
        slider.draw()

    # draws our array graph and updates our display
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    # Creates a rectangle to draw over the array area, effectively clearing the area
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, WIDTH - draw_info.SIDE_PAD,
                      HEIGHT - draw_info.TOP_PAD)
        pygame.draw.rect(window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Draws a rectangle to visualize each element in our list
    for i, val in enumerate(lst):
        # Starting x position for the rectangle. It will move to the right by block_width units
        x = draw_info.start_x + i * draw_info.block_width
        # Starting y position for the rectangle. It will move down by HEIGHT units, to the end of the page.
        y = HEIGHT - (val - draw_info.min_val) * draw_info.block_height

        # cycles through the GRADIENTS array to give each rectangle a different color than its neighbors
        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(window, color, (x, y, draw_info.block_width, HEIGHT))

    if clear_bg:
        pygame.display.update()


def create_starting_list(n, min_val, max_val):
    lst = []
    # adds n random values to an empty list, then returns that list
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    # loop through each element in the list and compare them
    for j in range(len(lst) - 1):
        for i in range(len(lst) - 1 - j):
            num1 = lst[i]
            num2 = lst[i + 1]
            # swap elements if not in order
            if num1 > num2 and ascending or (num1 < num2 and not ascending):
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, i + 1: draw_info.RED}, True)
                yield lst  # allows us to press other buttons to interrupt if need be (ex. for reset)


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for j in range(1, len(lst)):
        key = lst[j]
        i = j - 1
        # Compare key with element on the left, until a smaller (or larger for descending order) element is found,
        while i >= 0 and key < lst[i] and ascending or (i >= 0 and key > lst[i] and not ascending):
            lst[i + 1] = lst[i]
            i -= 1
        # place key after smaller element
        lst[i + 1] = key
        draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
        yield lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursive(start, end):
        if end - start > 1:
            middle = (start + end) // 2

            # Recursively calling this function to split the array in half
            yield from merge_sort_recursive(start, middle)
            yield from merge_sort_recursive(middle, end)

            # Setting our new arrays using our start, middle, and end values
            left = lst[start:middle]
            right = lst[middle:end]

            i = j = 0
            k = start

            # Pick the larger/smaller of the elements until we reach the end of the right or left array
            # and place them in the list in order
            while i < len(left) and j < len(right):
                if left[i] < right[j] and ascending or (left[i] > right[j] and not ascending):
                    lst[k] = left[i]
                    i += 1
                else:
                    lst[k] = right[j]
                    j += 1
                k += 1
                draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
                yield True

            # When we run out of elements in left or right, put remaining elements in list
            while i < len(left):
                lst[k] = left[i]
                i += 1
                k += 1
                draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
                yield True
            while j < len(right):
                lst[k] = right[j]
                j += 1
                k += 1
                draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)

    yield from merge_sort_recursive(0, len(lst))  # call inner function with start/end arguments


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # This function finds the partition position
    def partition(left, right):
        pivot = lst[right]

        i = left - 1

        # Compares each element with the pivot
        for j in range(left, right):
            # If we're sorting in ascending order and a smaller element is found,
            # or we're sorting in descending order and a larger element is found,
            # we swap that element with the i element.
            if lst[j] <= pivot and ascending or (lst[j] >= pivot and not ascending):
                i = i + 1
                # Swaps elements i and j, then draws their new positions
                (lst[i], lst[j]) = (lst[j], lst[i])
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        # Swaps the pivot and the right element, then draws their new positions
        (lst[i + 1], lst[right]) = (lst[right], lst[i + 1])
        draw_list(draw_info, {i + 1: draw_info.GREEN, right: draw_info.RED}, True)
        yield True

        return i + 1

    def quick_sort_recursive(left, right):
        if left < right:
            # Find the pivot element so that smaller elements are on the left
            # and larger elements are on the right
            pivot = yield from partition(left, right)

            # Recursively calls on the left and right of the pivot
            yield from quick_sort_recursive(left, pivot - 1)
            yield from quick_sort_recursive(pivot + 1, right)

    yield from quick_sort_recursive(0, len(lst) - 1)  # call inner function with start/end arguments


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for j in range(len(lst)):
        min_index = j
        for i in range(j + 1, len(lst)):
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            # If sorting in ascending order and the element in the i is smaller
            # Or if sorting in descending order and the element in the i is larger
            # set i to our new minimum
            if lst[i] < lst[min_index] and ascending or (lst[i] > lst[min_index] and not ascending):
                min_index = i
            # set i to our new minimum
        (lst[j], lst[min_index]) = (lst[min_index], lst[j])
        yield True


def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst
    length = len(lst)

    def heapify(arr, n, i):
        # Finding the largest among the root and children
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[i] < arr[l] and ascending or (l < n and arr[i] > arr[l] and not ascending):
            largest = l
            yield True

        if r < n and arr[largest] < arr[r] and ascending or (r < n and arr[largest] > arr[r] and not ascending):
            largest = r
            yield True

        # If the largest isn't the root, swap with the largest and heapify again
        if largest != i:
            (arr[i], arr[largest]) = (arr[largest], arr[i])
            draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
            yield from heapify(arr, n, largest)

    # Building our max heap
    for step in range(length // 2, -1, -1):
        yield from heapify(lst, length, step)

    for j in range(length - 1, 0, -1):
        # Heapify-ing the root element
        (lst[j], lst[0]) = (lst[0], lst[j])
        yield from heapify(lst, j, 0)


def main():
    run = True

    # Minimum and Maximum array sizes
    min_val = 0
    max_val = 100
    min_total_array = 5
    max_total_array = 50
    min_speed_val = 4000
    max_speed_val = 10000

    # These sliders control the speed of the sorts and the size of the array that they sort
    array_slider = Slider(window, 200, 10, 200, 10, min=min_total_array, max=max_total_array, step=1, initial=25)
    array_size = array_slider.getValue()
    speed_slider = Slider(window, 200, 45, 200, 10, min=min_speed_val, max=max_speed_val, step=1000, initial=1)
    array_speed = speed_slider.getValue()

    # creates our starting list and sends the list information to draw_info
    lst = create_starting_list(array_size, min_val, max_val)
    draw_info = DrawInfo(lst)

    # Bools to hold if we're sorting and what order we are sorting in
    sorting = False
    ascending = True

    # initializing the first sort as the bubble_sort
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    # Buttons to allow user to reset graph and change from ascending to descending sorts
    reset_button = Button(0, 60, 175, 35, draw_info.BUTTON_GREY, "Reset")
    ascending_button = Button(0, 95, 175, 35, draw_info.BUTTON_GREY, "Ascending")

    # Buttons to allow user to change between the kinds of sorts they would like to do
    bubble_button = Button(450, 0, 175, 35, draw_info.BUTTON_ACTIVE, "Bubble Sort")
    insertion_button = Button(625, 0, 175, 35, draw_info.BUTTON_GREY, "Insertion Sort")
    merge_button = Button(450, 35, 175, 35, draw_info.BUTTON_GREY, "Merge Sort")
    quick_button = Button(625, 35, 175, 35, draw_info.BUTTON_GREY, "Quick Sort")
    selection_button = Button(450, 70, 175, 35, draw_info.BUTTON_GREY, "Selection Sort")
    heap_button = Button(625, 70, 175, 35, draw_info.BUTTON_GREY, "Heap Sort")

    # Button to start sorting
    start_button = Button(625, 105, 175, 35, draw_info.GREEN, "Start")

    buttons = [bubble_button, insertion_button, merge_button, quick_button, selection_button, heap_button,
               ascending_button, reset_button, start_button]
    sliders = [array_slider, speed_slider]

    # This button will be turned grey when a new button is clicked
    last_button = bubble_button

    # value to hold when the next frame can run for the speed slider
    next_frame = 0

    while run:
        time_now = pygame.time.get_ticks()

        # if sorting is true and it's time to show another frame
        if sorting:
            try:
                if time_now > next_frame:
                    inverted_speed = max_speed_val - array_speed  # inverts our slider value so it works like speed and not a delay
                    frame_delay = inverted_speed // 60
                    next_frame = time_now + frame_delay  # setting the next_frame to a new higher number
                    next(
                        sorting_algorithm_generator)  # continue our sorting algorithm assuming there is no new inputs that interrupt
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, buttons,
                 sliders)  # if we're not sorting we can just clear the menu

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # if we click on the window
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get the position of where we clicked
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    # if the position we clicked is on a button
                    if button.is_clicked(pos):
                        # set the button clicked to the active color
                        # set the sorting algorithm for the generator to the correct generator
                        # set the previous button to grey
                        # set clicked button to last_button to keep track of which button we clicked last
                        if button.text == "Bubble Sort" and not sorting:
                            button.color = draw_info.BUTTON_ACTIVE
                            sorting_algorithm = bubble_sort
                            last_button.color = draw_info.BUTTON_GREY
                            last_button = bubble_button
                        elif button.text == "Insertion Sort" and not sorting:
                            button.color = draw_info.BUTTON_ACTIVE
                            sorting_algorithm = insertion_sort
                            last_button.color = draw_info.BUTTON_GREY
                            last_button = insertion_button
                        elif button.text == "Merge Sort" and not sorting:
                            button.color = draw_info.BUTTON_ACTIVE
                            sorting_algorithm = merge_sort
                            last_button.color = draw_info.BUTTON_GREY
                            last_button = merge_button
                        elif button.text == "Quick Sort" and not sorting:
                            button.color = draw_info.BUTTON_ACTIVE
                            sorting_algorithm = quick_sort
                            last_button.color = draw_info.BUTTON_GREY
                            last_button = quick_button
                        elif button.text == "Selection Sort" and not sorting:
                            button.color = draw_info.BUTTON_ACTIVE
                            sorting_algorithm = selection_sort
                            last_button.color = draw_info.BUTTON_GREY
                            last_button = selection_button
                        elif button.text == "Heap Sort" and not sorting:
                            button.color = draw_info.BUTTON_ACTIVE
                            sorting_algorithm = heap_sort
                            last_button.color = draw_info.BUTTON_GREY
                            last_button = heap_button
                        # Resets the visualizer and generators a new array to display. Sets sorting to False
                        elif button.text == "Reset":
                            lst = create_starting_list(array_size, min_val, max_val)  # creates a new list
                            draw_info.set_list(lst)  # sets our new list and redraws the window
                            sorting = False  # turns off sorting
                        # Sets sorting to true and runs the generator using the current sorting_algorithm
                        elif button.text == "Start":
                            sorting = True
                            sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                        # These switch the algorithms between Ascending and Descending modes
                        elif button.text == "Descending":
                            ascending = True
                            button.text = "Ascending"
                        elif button.text == "Ascending":
                            ascending = False
                            button.text = "Descending"

        pygame_widgets.update(events)
        # If list length slider value has been changed, set sorting to false and generate a new list
        if array_slider.getValue() != array_size:
            array_size = array_slider.getValue()
            lst = create_starting_list(array_size, min_val, max_val)
            draw_info.set_list(lst)
            sorting = False
        # If sort speed slider has changed, change the delay to the appropriate value and redraw the menu
        if speed_slider.getValue() != array_speed:
            array_speed = speed_slider.getValue()
            draw(draw_info, sorting_algo_name, ascending, buttons, sliders)

    pygame.quit()


if __name__ == "__main__":
    main()
